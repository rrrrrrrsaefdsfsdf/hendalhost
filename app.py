import os
from flask import Flask, request, render_template, url_for, redirect, send_from_directory
from PIL import Image
import uuid
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3

app = Flask(__name__)
UPLOAD_FOLDER = './data/uploads'
DB = './data/hendal.db'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS albums (id TEXT PRIMARY KEY, upload_date DATE, expiration_days INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS images (album_id TEXT, filename TEXT)''')
    conn.commit()
    conn.close()

init_db()

def clean_exif(file_path):
    image = Image.open(file_path)
    data = list(image.getdata())
    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(data)
    image_without_exif.save(file_path)

def delete_old():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT id, upload_date, expiration_days FROM albums')
    albums = c.fetchall()
    for album in albums:
        upload_date = datetime.date.fromisoformat(album[1])
        expiration_days = album[2]
        if (datetime.date.today() - upload_date).days > expiration_days:
            c.execute('SELECT filename FROM images WHERE album_id = ?', (album[0],))
            files = c.fetchall()
            for f in files:
                try:
                    os.remove(os.path.join(UPLOAD_FOLDER, f[0]))
                except:
                    pass
            c.execute('DELETE FROM images WHERE album_id = ?', (album[0],))
            c.execute('DELETE FROM albums WHERE id = ?', (album[0],))
    conn.commit()
    conn.close()

scheduler = BackgroundScheduler()
scheduler.add_job(func=delete_old, trigger="interval", days=1)
scheduler.start()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        files = request.files.getlist('files')
        expiration_days = int(request.form.get('expiration', 180))
        if files:
            album_id = str(uuid.uuid4())
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            today = datetime.date.today()
            c.execute('INSERT INTO albums (id, upload_date, expiration_days) VALUES (?, ?, ?)', (album_id, today, expiration_days))
            for file in files:
                if file.filename:
                    ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
                    filename = str(uuid.uuid4()) + '.' + ext
                    path = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(path)
                    clean_exif(path)
                    c.execute('INSERT INTO images (album_id, filename) VALUES (?, ?)', (album_id, filename))
            conn.commit()
            conn.close()
            return redirect(url_for('album', album_id=album_id))
    return render_template('index.html')

@app.route('/album/<album_id>')
def album(album_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT upload_date, expiration_days FROM albums WHERE id = ?', (album_id,))
    res = c.fetchone()
    if not res:
        conn.close()
        return render_template('error.html', error_code=404, error_message='Альбом не найден'), 404
    upload_date = datetime.date.fromisoformat(res[0])
    expiration_days = res[1]
    if (datetime.date.today() - upload_date).days > expiration_days:
        delete_old()
        conn.close()
        return render_template('error.html', error_code=404, error_message='Альбом истек'), 404
    c.execute('SELECT filename FROM images WHERE album_id = ?', (album_id,))
    images = [url_for('uploaded_file', filename=f[0], _external=True) for f in c.fetchall()]
    conn.close()
    if not images:
        return render_template('error.html', error_code=404, error_message='Изображения не найдены'), 404
    return render_template('album.html', images=images)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', error_code=404, error_message='Страница не найдена'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', error_code=500, error_message='Внутренняя ошибка сервера'), 500
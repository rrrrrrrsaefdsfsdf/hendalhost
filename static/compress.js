// document.getElementById('upload-form').addEventListener('submit', async function (event) {
//     event.preventDefault();
//     const input = document.getElementById('files');
//     const files = input.files;
//     const formData = new FormData();
//     const expiration = document.getElementById('expiration').value;

//     async function compressImage(file) {
//         const img = new Image();
//         const canvas = document.createElement('canvas');
//         const ctx = canvas.getContext('2d');
//         const bitmap = await window.createImageBitmap(file);
//         let { width, height } = bitmap;
//         const maxWidth = 1024;
//         const maxHeight = 1024;

//         if (width > height) {
//             if (width > maxWidth) {
//                 height *= maxWidth / width;
//                 width = maxWidth;
//             }
//         } else {
//             if (height > maxHeight) {
//                 width *= maxHeight / height;
//                 height = maxHeight;
//             }
//         }

//         canvas.width = width;
//         canvas.height = height;
//         ctx.drawImage(bitmap, 0, 0, width, height);
//         return new Promise((resolve) => {
//             canvas.toBlob((blob) => {
//                 resolve(new File([blob], file.name, { type: 'image/jpeg' }));
//             }, 'image/jpeg', 0.7);
//         });
//     }

//     for (const file of files) {
//         if (file.type.startsWith('image/')) {
//             const compressedFile = await compressImage(file);
//             formData.append('files', compressedFile);
//         }
//     }
//     formData.append('expiration', expiration);

//     fetch('/', {
//         method: 'POST',
//         body: formData
//     }).then(response => {
//         if (response.redirected) {
//             window.location.href = response.url;
//         } else {
//             alert('Ошибка при загрузке');
//         }
//     });
// });
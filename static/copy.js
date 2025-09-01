function copyLink(elementId) {
    const link = document.getElementById(elementId).href;
    navigator.clipboard.writeText(link).then(() => {
        alert('Ссылка скопирована!');
    }).catch(() => {
        alert('Ошибка при копировании');
    });
}
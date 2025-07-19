// Простой скрипт для мобильного меню
document.querySelector('.mobile-menu-btn').addEventListener('click', function() {
    const menu = document.querySelector('nav ul');
    menu.style.display = menu.style.display === 'flex' ? 'none' : 'flex';
    
    // Для мобильных устройств добавляем стиль
    if (window.innerWidth <= 768) {
        if (menu.style.display === 'flex') {
            menu.style.flexDirection = 'column';
            menu.style.position = 'absolute';
            menu.style.top = '100%';
            menu.style.left = '0';
            menu.style.width = '100%';
            menu.style.background = 'white';
            menu.style.padding = '20px';
            menu.style.boxShadow = '0 5px 10px rgba(0,0,0,0.1)';
        }
    }
});

// Закрытие меню при клике на пункт
document.querySelectorAll('nav a').forEach(item => {
    item.addEventListener('click', function() {
        if (window.innerWidth <= 768) {
            document.querySelector('nav ul').style.display = 'none';
        }
    });
});

// Плавная прокрутка для якорных ссылок
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

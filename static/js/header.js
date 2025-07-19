// Простой скрипт для мобильного меню
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const menu = document.querySelector('nav ul');
    
    // Проверяем наличие элементов
    if (!mobileMenuBtn || !menu) {
        console.warn('Элементы мобильного меню не найдены');
        return;
    }
    
    // Обработчик клика по кнопке мобильного меню
    mobileMenuBtn.addEventListener('click', function() {
        menu.classList.toggle('mobile-menu-open');
    });
    
    // Закрытие меню при клике на пункт меню
    document.querySelectorAll('nav a').forEach(item => {
        item.addEventListener('click', function() {
            if (window.innerWidth <= 768) {
                menu.classList.remove('mobile-menu-open');
            }
        });
    });
    
    // Функция для сброса мобильного меню при изменении размера экрана
    function handleResize() {
        if (window.innerWidth > 768) {
            menu.classList.remove('mobile-menu-open');
        }
    }
    
    // Обработчик изменения размера окна
    window.addEventListener('resize', handleResize);
    
    // Плавная прокрутка для якорных ссылок с учетом высоты header'а
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                // Получаем высоту header'а
                const header = document.querySelector('header') || document.querySelector('.header');
                const headerHeight = header ? header.offsetHeight : 80;
                
                // Вычисляем позицию с учетом header'а
                const targetPosition = targetElement.offsetTop - headerHeight;
                
                // Плавная прокрутка
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
});

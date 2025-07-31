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
  
  // Закрытие меню при клике на пункт меню (исключая выпадающие списки)
  document.querySelectorAll('nav a').forEach(item => {
    item.addEventListener('click', function(e) {
      // Не закрываем мобильное меню для выпадающих списков
      if (this.closest('.services-dropdown') || this.closest('.user-menu-item')) {
        return;
      }
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
      const targetId = this.getAttribute('href');
      
      // Пропускаем пустые якоря
      if (targetId === '#' || targetId === '') {
        return;
      }
      
      e.preventDefault();
      
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

function toggleUserDropdown() {
  const dropdown = document.getElementById('userDropdown');
  dropdown.classList.toggle('show');
}

// Функция для переключения выпадающего списка услуг
function toggleServicesDropdown(event) {
  console.log('toggleServicesDropdown вызвана');
  event.preventDefault();
  event.stopPropagation();
  
  const dropdown = event.target.closest('.services-dropdown');
  console.log('dropdown найден:', dropdown);
  
  if (!dropdown) return;
  
  const menu = dropdown.querySelector('.services-dropdown-menu');
  console.log('menu найдено:', menu);
  
  if (!menu) return;
  
  menu.classList.toggle('show');
  console.log('класс show переключен, текущие классы:', menu.className);
}

// Закрытие при клике вне меню
document.addEventListener('click', function(event) {
  const userMenu = document.querySelector('.user-menu-item');
  if (userMenu && !userMenu.contains(event.target)) {
    document.getElementById('userDropdown').classList.remove('show');
  }
  
  // Закрытие выпадающего списка услуг при клике вне меню
  const servicesMenu = document.querySelector('.services-dropdown');
  if (servicesMenu && !servicesMenu.contains(event.target)) {
    const servicesDropdown = servicesMenu.querySelector('.services-dropdown-menu');
    if (servicesDropdown) {
      servicesDropdown.classList.remove('show');
    }
  }
});

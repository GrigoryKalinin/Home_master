document.addEventListener('DOMContentLoaded', function() {
    // Получаем элементы DOM
    const orderForm = document.getElementById('orderForm');
    const submitBtn = document.getElementById('submitOrderBtn');
    const spinner = submitBtn.querySelector('.spinner-border');
    const messagesDiv = document.getElementById('form-messages');
    const modalElement = document.getElementById('orderModal');
    const modal = new bootstrap.Modal(modalElement);
    const modalTitle = document.getElementById('orderModalLabel');

    // ===== 1. Обработчик для динамического изменения заголовка модального окна =====
    // Находим все кнопки, которые открывают это модальное окно
    const modalButtons = document.querySelectorAll('[data-bs-toggle="modal"][data-bs-target="#orderModal"]');
    
    // Для каждой кнопки добавляем обработчик клика
    modalButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Получаем название услуги из data-атрибута или текст кнопки
            const serviceName = this.dataset.serviceName || this.textContent.trim();
            
            // Устанавливаем заголовок модального окна
            modalTitle.textContent = serviceName;
            
        });
    });

    // ===== 2. Обработчик отправки формы =====
    orderForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Показываем спиннер загрузки и блокируем кнопку
        spinner.classList.remove('d-none');
        submitBtn.disabled = true;
        messagesDiv.innerHTML = '';

        // Собираем данные формы
        const formData = new FormData(orderForm);

        // Отправляем AJAX-запрос
        fetch(orderForm.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest', // Для определения AJAX-запроса на сервере
                'X-CSRFToken': formData.get('csrfmiddlewaretoken') // Защита от CSRF
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Успешная отправка - показываем сообщение и сбрасываем форму
                messagesDiv.innerHTML = `
                    <div class="alert alert-success">
                        ${data.message}
                    </div>
                `;
                orderForm.reset();
                
                // Закрываем модальное окно через 2 секунды
                setTimeout(() => {
                    modal.hide();
                    messagesDiv.innerHTML = '';
                }, 2000);
            } else {
                // Ошибки валидации - показываем их пользователю
                let errorHtml = '<div class="alert alert-danger"><ul class="mb-0">';
                for (const [field, errors] of Object.entries(data.errors)) {
                    errors.forEach(error => {
                        errorHtml += `<li>${error}</li>`;
                    });
                }
                errorHtml += '</ul></div>';
                messagesDiv.innerHTML = errorHtml;
            }
        })
        .catch(error => {
            // Обработка ошибок сети/сервера
            console.error('Error:', error);
            messagesDiv.innerHTML = `
                <div class="alert alert-danger">
                    Произошла ошибка при отправке заявки. Попробуйте еще раз.
                </div>
            `;
        })
        .finally(() => {
            // В любом случае скрываем спиннер и разблокируем кнопку
            spinner.classList.add('d-none');
            submitBtn.disabled = false;
        });
    });

    // ===== 3. Очистка формы при закрытии модального окна =====
    modalElement.addEventListener('hidden.bs.modal', function() {
        orderForm.reset();
        messagesDiv.innerHTML = '';
        spinner.classList.add('d-none');
        submitBtn.disabled = false;
        
        // Можно также сбросить заголовок к значению по умолчанию
        modalTitle.textContent = 'Заказать услугу';
    });
});
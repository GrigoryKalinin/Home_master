document.addEventListener('DOMContentLoaded', function() {
    const orderForm = document.getElementById('orderForm');
    const submitBtn = document.getElementById('submitOrderBtn');
    const spinner = submitBtn.querySelector('.spinner-border');
    const messagesDiv = document.getElementById('form-messages');
    const modal = new bootstrap.Modal(document.getElementById('orderModal'));

    orderForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Показываем спиннер
        spinner.classList.remove('d-none');
        submitBtn.disabled = true;
        messagesDiv.innerHTML = '';

        const formData = new FormData(orderForm);

        fetch(orderForm.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Успешная отправка
                messagesDiv.innerHTML = `
                    <div class="alert alert-success">
                        ${data.message}
                    </div>
                `;
                orderForm.reset();
                setTimeout(() => {
                    modal.hide();
                    messagesDiv.innerHTML = '';
                }, 2000);
            } else {
                // Ошибки валидации
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
            console.error('Error:', error);
            messagesDiv.innerHTML = `
                <div class="alert alert-danger">
                    Произошла ошибка при отправке заявки. Попробуйте еще раз.
                </div>
            `;
        })
        .finally(() => {
            // Скрываем спиннер
            spinner.classList.add('d-none');
            submitBtn.disabled = false;
        });
    });

    // Очистка формы при закрытии модального окна
    document.getElementById('orderModal').addEventListener('hidden.bs.modal', function() {
        orderForm.reset();
        messagesDiv.innerHTML = '';
        spinner.classList.add('d-none');
        submitBtn.disabled = false;
    });
});
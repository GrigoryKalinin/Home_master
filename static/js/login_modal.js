document.addEventListener("DOMContentLoaded", function () {
  const loginModal = new bootstrap.Modal(document.getElementById('loginModal'));
  const loginForm = document.getElementById('loginForm');

  // Функция для показа модального окна
  window.showLoginModal = function() {
    loginModal.show();
  };

  // Обработчик формы входа
  if (loginForm) {
    loginForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const submitBtn = document.getElementById('loginSubmitBtn');
      const spinner = submitBtn.querySelector('.spinner-border');
      const messagesDiv = document.getElementById('login-messages');

      // Показываем спиннер
      spinner.classList.remove('d-none');
      submitBtn.disabled = true;
      messagesDiv.innerHTML = '';
      clearErrors();

      // Отправляем форму
      const formData = new FormData(loginForm);
      
      fetch(loginForm.action, {
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
          messagesDiv.innerHTML = `<div class="alert alert-success">${data.message}</div>`;
          loginForm.reset();
          setTimeout(() => {
            loginModal.hide();
            if (data.redirect_url) {
              window.location.href = data.redirect_url;
            } else {
              location.reload();
            }
          }, 1000);
        } else {
          showErrors(data.errors);
        }
      })
      .catch(error => {
        console.error('Error:', error);
        messagesDiv.innerHTML = '<div class="alert alert-danger">Произошла ошибка. Попробуйте еще раз.</div>';
      })
      .finally(() => {
        spinner.classList.add('d-none');
        submitBtn.disabled = false;
      });
    });
  }

  // Функция для отображения ошибок
  function showErrors(errors) {
    for (const [field, fieldErrors] of Object.entries(errors)) {
      const errorDiv = document.getElementById(`${field}-error`);
      if (errorDiv) {
        errorDiv.textContent = fieldErrors[0];
      }
    }
    
    if (errors.__all__) {
      const messagesDiv = document.getElementById('login-messages');
      messagesDiv.innerHTML = `<div class="alert alert-danger">${errors.__all__[0]}</div>`;
    }
  }

  // Функция для очистки ошибок
  function clearErrors() {
    const errorDivs = loginForm.querySelectorAll('.text-danger');
    errorDivs.forEach(div => div.textContent = '');
  }

  // Очистка формы при закрытии модального окна
  document.getElementById('loginModal').addEventListener('hidden.bs.modal', function() {
    loginForm.reset();
    clearErrors();
    document.getElementById('login-messages').innerHTML = '';
    const spinner = document.querySelector('#loginSubmitBtn .spinner-border');
    if (spinner) spinner.classList.add('d-none');
    document.getElementById('loginSubmitBtn').disabled = false;
  });
});
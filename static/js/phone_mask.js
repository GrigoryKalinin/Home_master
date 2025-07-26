$(function() {
  // Инициализация маски без валидации
  $('#id_phone').inputmask({
    mask: "+7 (999) 999-99-99",
    placeholder: "_",
    clearMaskOnLostFocus: false,
    showMaskOnHover: false
  });

  // Валидация при отправке формы
  $('form').on('submit', function(e) {
    const $phoneInput = $('#id_phone');
    const unmaskedValue = $phoneInput.inputmask('unmaskedvalue');
    
    // Очищаем предыдущие ошибки
    $phoneInput.removeClass('is-invalid');
    $phoneInput.next('.invalid-feedback').remove();
    
    // Проверка на 10 цифр (без +7)
    if (unmaskedValue.length !== 10) {
      $phoneInput.addClass('is-invalid');
      $('<div class="invalid-feedback">Номер должен содержать 10 цифр (без +7)</div>')
        .insertAfter($phoneInput);
      e.preventDefault();
      return false;
    }
    
    return true;
  });
});
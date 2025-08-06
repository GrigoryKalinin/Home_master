$(function() {
  // Инициализация маски для всех полей телефона
  $('.phone-mask, #id_phone').inputmask({
    mask: "+7 (999) 999-99-99",
    placeholder: "_",
    clearMaskOnLostFocus: false,
    showMaskOnHover: false
  });

  // Валидация при отправке формы
  $('form').on('submit', function(e) {
    const $phoneInput = $('.phone-mask, #id_phone');
    
    $phoneInput.each(function() {
      const $input = $(this);
      const unmaskedValue = $input.inputmask('unmaskedvalue');
      
      // Очищаем предыдущие ошибки
      $input.removeClass('is-invalid');
      $input.next('.invalid-feedback').remove();
      
      // Проверка только если поле заполнено
      if ($input.val() && unmaskedValue.length !== 10) {
        $input.addClass('is-invalid');
        $('<div class="invalid-feedback">Номер должен содержать 10 цифр (без +7)</div>')
          .insertAfter($input);
        e.preventDefault();
        return false;
      }
    });
    
    return true;
  });
});
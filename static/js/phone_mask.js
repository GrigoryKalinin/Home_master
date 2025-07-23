$(function() {
    $('#id_phone').inputmask({
        mask: "+7 (999) 999-99-99",
        placeholder: "_",
        clearMaskOnLostFocus: false,
        showMaskOnHover: false,
        oncomplete: function() {
            // Очистка ошибок при успешном заполнении
            $(this).removeClass('is-invalid');
            $(this).parent().find('.invalid-feedback').remove();
        },
        onincomplete: function() {
            // Показываем ошибку, если номер не заполнен
            $(this).addClass('is-invalid');
            $(this).parent().append(
                '<div class="invalid-feedback">Введите номер полностью</div>'
            );
        }
    });

    // Дополнительная проверка перед отправкой формы
    $('form').on('submit', function(e) {
        const phoneInput = $('#id_phone');
        const unmaskedValue = phoneInput.inputmask('unmaskedvalue');
        
        if (unmaskedValue.length !== 10) {  // 10 цифр без +7
            phoneInput.addClass('is-invalid');
            phoneInput.parent().find('.invalid-feedback').remove();
            phoneInput.parent().append(
                '<div class="invalid-feedback">Номер должен содержать 10 цифр (без +7)</div>'
            );
            e.preventDefault();
        }
    });
});
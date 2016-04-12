/**
 * Created by Tanjid Islam on 19/03/2016.
 */

$('#form-repeat-password').keyup(function() {
    if($('#form-password').val() == $('#form-repeat-password').val()) {
        $('#error-red').remove();
        $('#error-green').text('Passwords match.');
        $('#signup').removeAttr('disabled');
    } else {
        $('#error-red').text("Passwords don't match.");
        $('#signup').attr('disabled', true);
    }
});


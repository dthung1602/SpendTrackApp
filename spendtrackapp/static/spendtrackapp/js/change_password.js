
function changePasswordSuccess() {
    $('.password-change input').val('');
    $('.password-change .input-error').hide().html('');
    $('#password-change-success')
        .show()
        .html('Password has been changed successfully at ' + new Date());
    enableChangePasswordButton();
}

function changePasswordFail(response, status, error) {
    enableChangePasswordButton();
    $('#password-change-success').addClass('hidden');
    switch (error) {
        case 'Bad Request':
            response = response.responseJSON;
            for (let e in response)
                if (response.hasOwnProperty(e))
                    $('#' + e + '_error').show().html(response[e].join('<br>'));
            break;
        case 'Internal Server Error':
            alert("Internal Server Error\nPlease try again later");
            break;
        default :
            alert("Unknown error\nPlease try again later");
    }
}

function submitChangePasswordForm() {
    let accountPassword = {
        csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val(),
        old_password: $('#old_password').val(),
        new_password1: $('#new_password1').val(),
        new_password2: $('#new_password2').val(),
    };

    disableChangePasswordButton();
    $('#password-change-success').hide();

    // send ajax request
    $.ajax({
        url: '/account/password_change/',
        type: 'POST',
        dataType: 'json',
        data: accountPassword,
        success: changePasswordSuccess,
        error: changePasswordFail
    });

    // hide error
    $('.input-error').hide();
}

function disableChangePasswordButton() {
    $('#change-password-button')
        .html('CHANGING...')
        .addClass('disable')
        .off('click');
}

function enableChangePasswordButton() {
    $('#change-password-button')
        .html('CHANGE MY PASSWORD')
        .removeClass('disable')
        .click(submitChangePasswordForm);
}

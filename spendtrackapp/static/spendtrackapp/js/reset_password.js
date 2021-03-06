const COUNT_DOWN_TIME = 120;

$(document).ready(function () {
    $("#resend-email-button").hide().click(resendEmail);
    countDown(COUNT_DOWN_TIME);
});

function countDown(count) {
    if (count === -1) {
        $("#resend-email-button").show();
        return;
    }

    $("#send-email-countdown").html(count);

    setTimeout(function () {
            countDown(count - 1)
        },
        1000);
}

function resendEmail() {
    let resendButton = $("#resend-email-button");
    resendButton
        .html("Sending...")
        .addClass('disable')
        .off('click');

    $.ajax({
        url: '/account/password_reset/',
        type: 'POST',
        data: {
            email: $("#email").val(),
            csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val()
        },
        success: function () {
            resendButton
                .html("Resend")
                .removeClass('disable')
                .click(resendEmail)
                .hide();
            countDown(COUNT_DOWN_TIME);
        },
        error: function (response, status, error) {
            displayError(response, status, error);
            resendButton
                .html("Resend")
                .removeClass('disable')
                .click(resendEmail);
        }
    });
}

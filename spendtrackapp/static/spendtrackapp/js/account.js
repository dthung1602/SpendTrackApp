$(document).ready(function () {
    $('#edit-account-button').click(editAccount);
    $('#delete-account-button').click(deleteAccountForm);
    $('#save-account-button').click(submitEditAccountForm).hide();
    $('#cancel-edit-account-button').click(cancelEditAccount).hide();
    $('#change-password-button').click(submitChangePasswordForm);
    $('.input-error').hide();
    $('#password-change-success').hide();
    $('#account-change-success').hide();
});

class Account {
    constructor(data) {
        this.username = data.username;
        this.email = data.email;
        this.first_name = data.first_name;
        this.last_name = data.last_name;

        this.errors = {};

        this.clean()
    }

    clean() {
        // validate username
        const usernameRegex = /^[a-zA-Z0-9_@+.\-]{1,150}$/;
        if (!this.username.match(usernameRegex))
            this.addError('username', 'Usernames must be from 1 to 150 characters long and can only contain alphanumeric, _, @, +, . and - characters.')

        // validate first name and last name
        if (this.first_name.length > 30)
            this.addError('first_name', 'First names are as most 30 characters long.');
        if (this.last_name.length > 150)
            this.addError('last_name', 'last names are as most 30 characters long.');

        // validate email
        const emailRegex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        if (this.email.length > 0 && !this.email.match(emailRegex))
            this.addError('email', 'Invalid email');
    }

    /**
     * Return an object with format:
     *      field1: ['error 1', 'error 2', ... ],
     *      field2: ['error 1', 'error 2', ... ],
     *      ...
     * @param field
     * @param errorMessage
     */
    addError(field, errorMessage) {
        if (this.errors[field] === undefined)
            this.errors[field] = [errorMessage];
        else
            this.errors[field].push(errorMessage);
    }

    /**
     * Whether the object data is valid
     * @returns {boolean}
     */
    isValid() {
        return isEmpty(this.errors);
    }

    getSubmitData() {
        let object = {
            csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val()
        };
        for (let i = 0; i < this.fields.length; i++) {
            let field = this.fields[i];
            object[field] = this[field];
        }
        return object;
    }
}

Account.fields = ['username', 'email', 'first_name', 'last_name'];

// ---------- ENABLE EDITING ---------------

function editAccount() {
    let rootNode = $('.account table');

    // backup old data
    storeData('account', 0, rootNode.html());

    // add input fields
    let tds = ['username', 'email', 'first_name', 'last_name'];
    for (let i = 0; i < tds.length; i++) {
        let td = $('#td_' + tds[i]);
        let inputField = $('<input type="text" id="account_' + tds[i] + '">').val(td.html());
        td.html('')
            .append(inputField)
            .append($('<div class="input-error" id="error_' + tds[i] + '">').hide())
    }

    // change buttons
    $('#edit-account-button').hide();
    $('#delete-account-button').hide();
    $('#save-account-button').show();
    $('#cancel-edit-account-button').show();
}

function cancelEditAccount() {
    $('.account table').html(retrieveData('account', 0));

    $('#edit-account-button').show();
    $('#delete-account-button').show();
    $('#save-account-button').hide();
    $('#cancel-edit-account-button').hide();
}

function getAccountInfo() {
    let data = {};
    let fields = Account.fields;
    for (let i = 0; i < fields.length; i++) {
        data[fields[i]] = $('#account_' + fields[i]).val();
    }
    return data;
}

// ---------- SUBMIT EDIT ---------------

function editAccountSuccessFunc(account) {
    return function () {
        cancelEditAccount();
        enableSaveAccountButton();

        let fields = ['username', 'email', 'first_name', 'last_name'];
        for (let i = 0; i < fields.length; i++) {
            $('#td_' + fields[i]).html(account[fields[i]])
        }

        $('#account-change-success').show()
            .text('Account updated successfully at ' + new Date());
    }
}

function editAccountFailFunc() {
    return function (response, status, error) {
        enableSaveAccountButton();
        displayError(response, status, error)
    }
}

function submitEditAccountForm() {
    let account = new Account(getAccountInfo());

    if (account.isValid()) {
        disableSaveAccountButton();

        // send ajax request
        $.ajax({
            url: '/account/edit/',
            type: 'POST',
            dataType: 'json',
            data: account.getSubmitData(),
            success: editAccountSuccessFunc(account),
            error: editAccountFailFunc()
        });
        // hide error
        $('.input-error').hide();

    } else {
        // display errors
        for (let i = 0; i < Account.fields.length; i++) {
            let f = Account.fields[i];
            if (account.errors.hasOwnProperty(f))
                $('#error_' + f)
                    .show()
                    .html(account.errors[f].join("<br>"))
        }
    }
}

function disableSaveAccountButton() {
    $('#save-account-button')
        .html('SAVING...')
        .addClass('disable')
        .off('click');
}

function enableSaveAccountButton() {
    $('#save-account-button')
        .html('SAVE')
        .removeClass('disable')
        .click(submitEditAccountForm);
}

// ---------- DELETE ---------------

function deleteAccountForm() {
    if (!confirm("Are you sure to delete this account?"))
        return;
    if (!confirm("Are you REALLY sure?"))
        return;
    if (!confirm("Are you REALLY REALLY sure?"))
        return;
    $.ajax({
        url: '/account/delete/',
        type: 'POST',
        dataType: 'json',
        data: {csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val()},
        success: deleteAccountSuccess,
        error: displayError
    });
}

function deleteAccountSuccess() {
    deleteAllCookies(); // logout
    window.location.replace("/");
}

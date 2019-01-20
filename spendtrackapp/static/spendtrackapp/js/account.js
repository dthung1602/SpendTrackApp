$(document).ready(function () {
    $('#edit-account-button').click(editAccount);
    $('#delete-account-button').click(deleteAccountForm);
    $('#save-account-button').click(submitEditAccountForm).hide();
    $('#cancel-edit-account-button').click(cancelEditAccount).hide();
    $('#change-password-button').click(submitChangePasswordForm);
});

class Account {
    constructor(data) {
        this.id = data.id;
        this.username = data.username;
        this.current_password = data.current_password;
        this.password1 = data.password1;
        this.password2 = data.password2;
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

        // validate password
        if (this.password1 !== undefined) {
            const passwordRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$/;
            if (this.password1 !== this.password2)
                this.addError('password2', 'Passwords do not match');
            if (!this.password1.match(passwordRegex))
                this.addError('password1', 'Password too week');
        }
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

Account.prototype.fields = ['id', 'username', 'current_password', 'password1', 'password2',
    'email', 'first_name', 'last_name'];

// ---------- EDIT ---------------

function editAccount() {
    let rootNode = $('.account table');

    // backup old data
    $('<div id="account-old-data">')
        .append(rootNode.clone())
        .appendTo($('body'))
        .hide();

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
    let oldData = $('#account-old-data');
    $('.account table')
        .html(oldData.html());
    oldData.remove();

    $('#edit-account-button').show();
    $('#delete-account-button').show();
    $('#save-account-button').hide();
    $('#cancel-edit-account-button').hide();
}

function getAccountInfo() {
    let data = {};
    let fields = Account.prototype.fields;
    for (let i = 0; i < fields.length; i++) {
        data[fields[i]] = $('#account_' + fields[i]).val();
    }
    return data;
}

function editAccountSuccessFunc(account) {
    return function () {
        cancelEditAccount();

        let fields = ['username', 'email', 'first_name', 'last_name'];
        for (let i = 0; i < fields.length; i++) {
            $('#td_' + fields[i]).html(account[fields[i]])
        }
    }
}

function editAccountFail() {
    return function (response, status, error) {
        enableSaveAccountButton();

        switch (error) {
            case 'Bad Request':
                let errorMessages = [];
                response = response.responseJSON;
                for (let e in response)
                    if (response.hasOwnProperty(e))
                        errorMessages.push(response[e].join(','));
                alert(errorMessages.join('\n'));
                break;
            case 'Internal Server Error':
                alert("Internal Server Error\nPlease try again later");
                break;
            default :
                alert("Unknown error\nPlease try again later");
        }
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
            error: editAccountFail
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
        .click(submitChangePasswordForm);
}

// ---------- DELETE ---------------

function deleteAccountForm() {

}

// ---------- CHANGE PASSWORD ---------------

function submitChangePasswordForm() {

}

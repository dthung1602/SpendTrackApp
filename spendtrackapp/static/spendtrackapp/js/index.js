const entryCatFieldId = 'entry-category';

$(document).ready(function () {
    $('#submit-entry-button').click(submitNewEntryForm);
    startTime();
    if ($(".no-data").length === 0)
        viewTablePage(1);

    // insert drop down button to the above div
    $('#category-dropdown-container').html(Category.toDropdownMenu(entryCatFieldId, false));
    // set category value to null
    Category.clearSelectCategoryField(entryCatFieldId);
});

// ------------------- CLOCK --------------------

/**
 * Make the clock in homepage click
 */
function startTime() {
    let now = new Date();

    let year = now.getFullYear();
    let month = (now.getMonth() + 1).fillZero();
    let day = now.getDate().fillZero();
    let dayInWeek = daysInWeekNamesS[now.getDay()];
    let hour = now.getHours().fillZero();
    let minute = now.getMinutes().fillZero();
    let second = now.getSeconds().fillZero();

    $("#clock").html(
        "<div>" + dayInWeek + " " + day + "/" + month + "/" + year + "</div>" +
        "<div>" + hour + ":" + minute + ":" + second + "</div>"
    );

    setTimeout(startTime, 1000)
}

// ------------------------ FORM -----------------------

/**
 * Set now to Date field
 */
function setNewEntryDatetimeNow() {
    let d = new Date();
    let datetime = [d.getFullYear(), (d.getMonth() + 1).fillZero(), d.getDate().fillZero()].join('-')
        + ' ' + [d.getHours().fillZero(), d.getMinutes().fillZero()].join(':');

    // Fire fox
    let datetimeField = $('#entry-date');
    datetimeField.val(datetime);

    // Other browsers
    if (datetimeField.val() !== datetime)
        datetimeField.val(datetime.replace(' ', 'T'))
}

/**
 * Clear all input fields in new entry form
 */
function clearNewEntryFields() {
    $('#new-entry [id^=entry]').val('');
    Category.clearSelectCategoryField(entryCatFieldId);
    $('#new-entry .input-error').hide();
}

// ------------- SUBMIT FORM ----------------

/**
 * Return an object contains all submit data
 */
function getNewEntryData() {
    return {
        csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val(),
        date: $('#entry-date').val().replace('T', ' '),
        content: $('#entry-content').val().trim(),
        leaf_category: $('#entry-category').val(),
        value: $('#entry-value').val(),
    }
}

/**
 * Display errors when submitting the form
 * @param response
 * @param status
 * @param error
 */
function addNewEntryFailFunc(response, status, error) {
    // enable submit button again
    enableAddEntryButton();

    // display error
    switch (error) {
        case 'Bad Request':
            let fields = ['date', 'content', 'leaf_category', 'value'];
            let causes = [];
            for (let i = 0; i < fields.length; i++) {
                let f = fields[i];
                if (response['responseJSON'].hasOwnProperty(f)) {
                    let r = response['responseJSON'][f];
                    for (let j = 0; j < r.length; j++) {
                        causes.push(r[j])
                    }
                }
            }
            alert("Bad request:\n- " + causes.join('\n- '));
            break;
        case 'Internal Server Error':
            alert("Internal Server Error\nPlease try again later");
            break;
        default:
            alert("Unknown error\nPlease try again later");
    }
}

/**
 * Create a function to call when new entry is added successfully
 * @param data: object contain submit data
 * @returns {Function} a function that update page content when a new entry is added successfully
 */
function addNewEntrySuccessFuncGenerator(data) {
    return function () {
        // get elements
        let categoryDisplay = $('#display-entry-category');
        let totalInWeek = $('#total-in-week');
        let totalInMonth = $('#total-in-month');
        let now = new Date();
        let submitDate = new Date(data.date);
        let wn = submitDate.getWeekNumber();
        let m = submitDate.getMonth();
        let y = submitDate.getFullYear();
        let value = parseFloat(data.value);

        // if item is not in this week, inform success
        if (now.getWeekNumber() !== wn || now.getFullYear() !== y) {
            $('#new-entry-success-panel').show().html('Item added to week ' + wn + ' of year ' + y);

        } else { // if item in this week, update page
            let row = $('<tr>').appendTo($('#entry-container'));
            $('#new-entry-success-panel').hide();

            // convert data to correct format
            data.date = daysInWeekNamesS[submitDate.getDay()].substr(0, 3) + " "
                + monthNames[submitDate.getMonth()].substr(0, 3) + " "
                + submitDate.getDate().fillZero() + ", "
                + (submitDate.getHours() % 12).fillZero() + " "
                + (submitDate.getHours() >= 12 ? 'PM' : 'AM');

            // add new row to table
            $('<td>').text(data.date).appendTo(row);
            $('<td>').text(data.content).appendTo(row);
            $('<td class="align-right">').text(value.toFixed(2)).appendTo(row);
            $('<td class="align-right">').text(categoryDisplay.text()).appendTo(row);

            // change total in week
            totalInWeek.text((parseFloat(totalInWeek.text()) + value).toFixed(2));
        }

        // change total in week
        if (now.getMonth() === m && now.getFullYear() === y)
            totalInMonth.text((parseFloat(totalInMonth.text()) + value).toFixed(2));

        // clear form
        $('#entry-container .no-data').remove();
        clearNewEntryFields();

        // enable submit button again
        enableAddEntryButton();
    }
}

/**
 * Validate form and display errors
 * @param data
 * @returns {boolean} whether form is valid
 */
function validateNewEntryForm(data) {
    let valid = true;
    $('#new-entry .input-error').hide();

    // valid date time
    if (isNaN(Date.parse(data.date))) {
        valid = false;
        $('#entry-date-error').show().html('Datetime must have format yyyy-mm-dd hh:mm');
    }

    // content must not be empty
    if (data.content === "") {
        valid = false;
        $('#entry-content-error').show().html('Content cannot be empty');
    }

    // category must not be empty
    if (data.leaf_category === "") {
        valid = false;
        $('#entry-category-error').show().html('A category must be selected');
    }

    // evaluate arithmetic expression in value fielD
    try {
        if (!data.value.match(/^[0-9 +\-*/().]+$/))
            throw "";
        data.value = eval(data.value).toFixed(2);
    } catch (err) {
        valid = false;
        $('#entry-value-error').show().html('Invalid arithmetic expression');
    }

    return valid;
}

/**
 *  Validate form, submit and handle result
 */
function submitNewEntryForm() {
    // get values to submit
    let data = getNewEntryData();

    // validate form
    if (!validateNewEntryForm(data)) return;

    // disable button until a response is received
    disableAddEntryButton();

    // send ajax request
    $.ajax({
        url: '/add/',
        type: 'POST',
        dataType: 'json',
        data: data,
        success: addNewEntrySuccessFuncGenerator(data),
        error: addNewEntryFailFunc,
    });
}

function disableAddEntryButton() {
    $('#submit-entry-button')
        .html('ADDING...')
        .addClass('disable')
        .off('click');
}

function enableAddEntryButton() {
    $('#submit-entry-button')
        .html('ADD')
        .removeClass('disable')
        .click(submitNewEntryForm);
}

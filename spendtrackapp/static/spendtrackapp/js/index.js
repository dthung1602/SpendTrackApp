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

// ------------- CATEGORY SELECT DROP DOWN----------------

/**
 * Display select category drop down
 */
function showDropDown() {
    $("#select-category").toggleClass('show');
}

/**
 * Hide select category drop down when click outside
 */
function hideDropDown(event) {
    if (!event.target.matches('.clickable')) {
        let dropDowns = document.getElementsByClassName("select-content");
        for (let i = 0; i < dropDowns.length; i++) {
            let openDropDown = dropDowns[i];
            if (openDropDown.classList.contains('show')) {
                openDropDown.classList.remove('show');
            }
        }
    }
}

window.onclick = hideDropDown;

/**
 * Select a category
 * @param categoryId
 */
function select(categoryId) {
    $('#category_id').val(categoryId);
    $('#category-display').text($('#cat-' + categoryId).text());
}

// ------------------------ FORM -----------------------

/**
 * Set now to Date field
 */
function setDatetimeNow() {
    let d = new Date();
    let datetime = [d.getFullYear(), (d.getMonth() + 1).fillZero(), d.getDate().fillZero()].join('-')
        + ' ' + [d.getHours().fillZero(), d.getMinutes().fillZero()].join(':');

    // Fire fox
    let datetimeField = $('#date');
    datetimeField.val(datetime);

    // Other browsers
    if (datetimeField.val() !== datetime)
        datetimeField.val(datetime.replace(' ', 'T'))
}

/**
 * Clear all input fields in new entry form
 */
function clearFields() {
    $('input[name!="csrfmiddlewaretoken"]').each(
        function (index, element) {
            element.value = ''
        }
    );
    $('#category-display').html('Select a category');
}

// ------------- SUBMIT FORM ----------------

/**
 * Return an object contains all submit data
 */
function getSubmitData() {
    return {
        csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val(),
        date: $('#date').val().replace('T', ' '),
        content: $('#content').val().trim(),
        category_id: $('#category_id').val(),
        value: $('#value').val(),
    }
}

/**
 * Display errors when submitting the form
 * @param response
 * @param status
 * @param error
 */
function addError(response, status, error) {
    switch (error) {
        case 'Bad Request':
            let fields = ['date', 'content', 'category_id', 'value'];
            let causes = [];
            for (let i = 0; i < fields.length; i++) {
                let f = fields[i];
                if (response.responseJSON.hasOwnProperty(f)) {
                    let r = response.responseJSON[f];
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
        default :
            alert("Unknown error\nPlease try again later");
    }
}

/**
 * Create a function to call when new entry is added successfully
 * @param data: object contain submit data
 * @returns {Function} a function that update page content when a new entry is added successfully
 */
function addSuccessFunc(data) {
    return function (response) {
        // get elements
        let row = $('<tr>').appendTo($('tbody'));
        let categoryDisplay = $('#category-display');
        let totalInWeek = $('#total-in-week');
        let currentBalance = $('#current-balance');

        // convert data to correct format
        data.value = parseFloat(data.value);
        data.date = new Date(data.date);
        data.date = daysInWeekNamesS[data.date.getDay()].substr(0, 3) + " "
            + monthNames[data.date.getMonth()].substr(0, 3) + " "
            + data.date.getDate().fillZero() + ", "
            + (data.date.getHours() % 12).fillZero() + " "
            + (data.date.getHours() >= 12 ? 'PM' : 'AM');

        // add new row to table
        $('<td>').text(data.date).appendTo(row);
        $('<td>').text(data.content).appendTo(row);
        $('<td class="align-right">').text(data.value.toFixed(2)).appendTo(row);
        $('<td class="align-right">').text(categoryDisplay.text()).appendTo(row);

        // change total in week and balance
        totalInWeek.text((parseFloat(totalInWeek.text()) + data.value).toFixed(2));
        currentBalance.text((parseFloat(currentBalance.text()) + data.value).toFixed(2));

        // clear form
        $('.input-error').hide();
        $('.no-data').remove();
        clearFields();
    }
}

/**
 * Validate form and display errors
 * @param data
 * @returns {boolean} whether form is valid
 */
function validateForm(data) {
    let valid = true;
    $('.input-error').hide();

    // valid date time
    if (isNaN(Date.parse(data.date))) {
        valid = false;
        $('#date-error').show().html('Datetime must have format yyyy-mm-dd hh:mm');
    }

    // content must not be empty
    if (data.content === "") {
        valid = false;
        $('#content-error').show().html('Content cannot be empty');
    }

    // category must not be empty
    if (data.category_id === "") {
        valid = false;
        $('#category-error').show().html('A category must be selected');
    }

    // evaluate arithmetic expression in value fielD
    try {
        if (!data.value.match('^[0-9 \\+\\-\\*\\/\\(\\)\\.]+$'))
            throw "";
        data.value = eval(data.value).toFixed(2);
    } catch (err) {
        valid = false;
        $('#value-error').show().html('Invalid arithmetic expression');
    }

    return valid;
}

/**
 *  Validate form, submit and handle result
 */
function submitForm() {
    // get values to submit
    let data = getSubmitData();

    // validate form
    if (!validateForm(data)) return;

    // send ajax request
    $.ajax({
        url: '/add/',
        type: 'POST',
        dataType: 'json',
        data: data,
        success: addSuccessFunc(data),
        error: addError,
    });
}

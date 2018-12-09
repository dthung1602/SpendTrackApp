let fields = [
    'year_year',
    'month_year', 'month_month',
    'week_year', 'week_week',
    'start_date', 'end_date'
];

/**
 * Fill default value for input fields
 */
function fillDefaultValues() {
    let now = new Date();
    let monthAbr = monthNamesAbr[now.getMonth()];
    let ISOCalendar = now.getISOCalendar();

    $('#year_year').val(now.getFullYear());
    $('#month_year').val(now.getFullYear());
    $('#month_month').val(monthAbr);
    $('#week_year').val(ISOCalendar[0]);
    $('#week_week').val(ISOCalendar[1]);
}

/**
 * Display correct input fields according to summarize type value
 */
function selectSummarizeType() {
    let type = $('#search_type').val();
    $('.summarize-group').hide();
    $('#summarize_' + type).show();
}

/**
 * Clear all input fields
 */
function clearFields() {
    for (let i = 0; i < fields.length; i++)
        $('#' + fields[i]).val('');
    $('.input-error').html('');
}

/**
 * Set now to end_date field
 */
function setEndDateNow() {
    let d = new Date();
    d = [d.getFullYear(), (d.getMonth() + 1).fillZero(), d.getDate().fillZero()].join('-');
    $('#end_date').val(d);
}

/**
 * Return an object contains all submit data
 */
function getSubmitData() {
    let f = fields.concat(['search_type']);
    let data = {
        csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val()
    };

    for (let i = 0; i < f.length; i++)
        data[f[i]] = $('#' + f[i]).val();

    return data;
}

/**
 * Validate form and display errors
 * @param data
 * @returns {boolean} whether form is valid
 */
function validateForm(data) {
    let errorField = $('.input-error');
    errorField.html('');

    switch (data.search_type) {
        // summarize year
        case 'year':
            if (data.year_year === '') { // check empty
                errorField.html('Please fill all the fields');
                return false;
            }
            return true;

        // summarize month
        case 'month':
            if (data.month_year === '' || data.month_month === '') { // check empty
                errorField.html('Please fill all the fields');
                return false;
            }
            return true;

        // summarize week
        case 'week':
            if (data.week_year === '' || data.week_week === '') { // check empty
                errorField.html('Please fill all the fields');
                return false;
            }
            return true;

        // summarize date range
        default:
            let errors = [];

            if (data.start_date === '' || data.end_date === '') // check empty
                errors.push('Please fill all the fields');

            else {
                let start_date = Date.parse(data.start_date);
                let end_date = Date.parse(data.end_date);
                // check start_date before end_date
                if (start_date > end_date)
                    errors.push('Start date must be before end date');
            }

            if (errors.length === 0) return true;
            errorField.html(errors.join('<br>'));
            return false;
    }
}

/**
 *  Validate form and redirect by a post request
 */
function submitForm() {
    let data = getSubmitData();

    if (!validateForm(data))
        return;

    redirectPost('/summarize/', data);
}
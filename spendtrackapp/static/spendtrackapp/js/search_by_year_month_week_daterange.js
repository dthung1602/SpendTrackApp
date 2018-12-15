let fields = [
    'search_by_year_year',
    'search_by_month_year', 'search_by_month_month',
    'search_by_week_year', 'search_by_week_week',
    'search_by_dr_start_date', 'search_by_dr_end_date'
];

/**
 * Fill default value for search input fields
 */
function fillDefaultValues() {
    let now = new Date();
    let ISOCalendar = now.getISOCalendar();

    $('#search-by-year-year').val(now.getFullYear());
    $('#search-by-month-year').val(now.getFullYear());
    $('#search-by-month-month').val(now.getMonth());
    $('#search-by-week-year').val(ISOCalendar[0]);
    $('#search-by-week-week').val(ISOCalendar[1]);
}

/**
 * Display correct input fields according to search type value
 */
function selectSearchType() {
    let type = $('#search-type').val().replace('_', '-');
    $('.search-group').hide();
    $('#summarize-' + type).show();
}

/**
 * Clear all search input fields
 */
function clearSearchFields() {
    $('[id^=search-by]').val('');
    $('#search-input-error').html('');
}

/**
 * Set now to end_date field
 */
function setSearchEndDateNow() {
    let d = new Date();
    let dd = [d.getFullYear(), (d.getMonth() + 1).fillZero(), d.getDate().fillZero()].join('-');
    $('#search-by-dr-end-date').val(dd);
}

/**
 * Return an object contains all submit data
 */
function getSearchData() {
    let searchType = $('#search-type').val();
    let data = {
        csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val(),
        search_type: searchType
    };

    switch (searchType) {
        case 'year':
            data.year = $('#search-by-year-year').val();
            break;
        case 'month':
            data.year = $('#search-by-month-year').val();
            data.month = $('#search-by-month-month').val();
            break;
        case 'week':
            data.year = $('#search-by-week-year').val();
            data.week = $('#search-by-week-week').val();
            break;
        case 'date_range':
            data.start_date = $('#search-by-dr-start-date').val();
            data.end_date = $('#search-by-dr-end-date').val();
            break;
    }

    return data;
}

/**
 * Validate form and display errors
 * @param data
 * @returns {boolean} whether form is valid
 */
function validateSearchForm(data) {
    let searchErrorField = $('#search-input-error');
    searchErrorField.html('');

    switch (data.search_type) {
        // summarize year
        case 'year':
            if (data.year === '') {
                searchErrorField.html('Please fill all the fields');
                return false;
            }
            if (!isValidYear(data.year)) {
                searchErrorField.html('Year must be in range 1000 - 9999');
                return false;
            }
            return true;

        // summarize month
        case 'month':
            if (data.month === '' || data.month === '') {
                searchErrorField.html('Please fill all the fields');
                return false;
            }
            if (!isValidYear(data.year)) {
                searchErrorField.html('Year must be in range 1000 - 9999');
                return false;
            }
            if (!isValidMonth(data.month)) {
                searchErrorField.html('Month must be in range 1 - 12');
                return false;
            }
            return true;

        // summarize week
        case 'week':
            if (data.week === '' || data.week === '') {
                searchErrorField.html('Please fill all the fields');
                return false;
            }
            if (!isValidYear(data.year)) {
                searchErrorField.html('Year must be in range 1000 - 9999');
                return false;
            }
            if (!isValidWeek(data.week)) {
                searchErrorField.html('Week must be in range 1 - 53');
                return false;
            }
            return true;

        // summarize date range
        case 'date_range':
            if (data.start_date === '' || data.end_date === '') {
                searchErrorField.html('Please fill all the fields');
                return false;
            } else {
                let startDate = Date.parse(data.start_date);
                let endDate = Date.parse(data.end_date);

                if (isNaN(startDate) || isNaN(endDate)) {
                    searchErrorField.html('Invalid date');
                    return false;
                }
                // check start_date before end_date
                if (startDate > endDate) {
                    searchErrorField.html('Start date must be before end date');
                    return false;
                }
            }
            return true;

        default:
            searchErrorField.html('Invalid search type');
            return false;
    }
}

/**
 *  Validate form and redirect by a post request
 */
function submitSearchFormRedirect(redirectPath) {
    let data = getSearchData();

    if (!validateSearchForm(data)) return;

    redirectPost(redirectPath, data);
}

function submitSearchFormAJAX(url, successFunc, failFunc) {
    let data = getSearchData();

    if (!validateSearchForm(data)) return;

    // send ajax request
    $.ajax({
        url: url,
        type: 'POST',
        dataType: 'json',
        data: data,
        success: successFunc,
        error: failFunc
    });
}

/**
 *  Validate year
 */
function isValidYear(year) {
    if (year.match(/^[0-9]{4}$/) !== null) {
        let y = parseInt(year);
        if (y >= 1000 && y <= 9999)
            return true;
    }
    return false
}

/**
 *  Validate month
 */
function isValidMonth(month) {
    if (month.match(/^[0-9]{1,2}$/) !== null) {
        let m = parseInt(month);
        if (m >= 1 && m <= 12)
            return true;
    }
    return false
}

/**
 *  Validate week
 */
function isValidWeek(week) {
    if (week.match(/^[0-9]{1,2}$/) !== null) {
        let w = parseInt(week);
        if (w >= 1 && w <= 53)
            return true;
    }
    return false
}

/**
 * Full name of days in week, start with Sunday
 */
daysInWeekNamesS = [
    "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"
];

/**
 * Full name of days in week, start with Monday
 */
daysInWeekNamesM = [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
];

monthNames = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
];

monthNamesAbr = [
    'jan', 'feb', 'mar', 'apr', 'may', 'jun',
    'jul', 'aug', 'sep', 'oct', 'nov', 'dec'
];

/**
 * Check if the object is empty
 * @returns {boolean}
 */
function isEmpty(obj) {
    for (let key in obj)
        if (obj.hasOwnProperty(key))
            return false;
    return true;
}

/**
 * Fill a leading zero if integer n < 9
 */
Number.prototype.fillZero = function () {
    let value = this.valueOf();
    if (Number.isInteger(value) && 0 <= value && value <= 9)
        return "0" + value;
    return "" + value;
};

/**
 * Return week number in year
 * @returns {number}
 */
Date.prototype.getWeekNumber = function () {
    let d = new Date(Date.UTC(this.getFullYear(), this.getMonth(), this.getDate()));
    let dayNum = d.getUTCDay() || 7;
    d.setUTCDate(d.getUTCDate() + 4 - dayNum);
    let yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
    return Math.ceil((((d - yearStart) / 86400000) + 1) / 7)
};
/**
 * Return week number in year
 * @returns {string}
 */
Date.prototype.toISODateString = function () {
    return this.toISOString().substr(0, 10);
};

function daysBetween(date1, date2) {
    return Math.round((date2.getTime() - date1.getTime()) / (1000 * 60 * 60 * 24));
}

/**
 * Send post request and redirect to that page
 *
 * Ref: https://stackoverflow.com/questions/19036684/jquery-redirect-with-post-data
 * @param location: redirect path
 * @param args: data to send
 */
function redirectPost(location, args) {
    let form = $('<form></form>');
    form.attr("method", "post");
    form.attr("action", location);

    $.each(args, function (key, value) {
        let field = $('<input>');

        field.attr("type", "hidden");
        field.attr("name", key);
        field.attr("value", value);

        form.append(field);
    });
    $(form).appendTo('body').submit();
}

/**
 * For a given date, get the ISO week number
 *
 * Ref: https://stackoverflow.com/questions/6117814/get-week-of-year-in-javascript-like-in-php
 *
 * e.g. 2014/12/29 is Monday in week  1 of 2015
 *      2012/1/1   is Sunday in week 52 of 2011
 */
Date.prototype.getISOCalendar = function () {
    let d = new Date(Date.UTC(this.getFullYear(), this.getMonth(), this.getDate()));
    d.setUTCDate(d.getUTCDate() + 4 - (d.getUTCDay() || 7));
    let yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
    let weekNo = Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
    return [d.getUTCFullYear(), weekNo];
};

/**
 * JS version of range in python
 */
function range() {
    switch (arguments.length) {
        case 2:
            let start = arguments[0];
            let end = arguments[1];
            return (new Array(end - start)).fill(undefined).map((_, i) => i + start);
        case 1:
            return [...Array(arguments[0])];
        default:
            throw "Invalid Arguments"
    }
}

/**
 * Scroll to page top
 */
function scrollToTop() {
    document.querySelector('.logo').scrollIntoView({
        behavior: 'smooth'
    });
}


/**
 * Switch between table pages
 */
function viewTablePage(page) {
    $('[class^="table-page-"]').hide();
    $('.table-page-' + page).show();
    $('.page-control .button').removeClass('selected');
    $('.page-control .button:nth-child(' + page + ')').addClass('selected');
}

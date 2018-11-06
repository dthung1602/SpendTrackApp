daysInWeekNames = [
    "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"
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
 * Fill a leading zero if integer n < 9
 */
Number.prototype.fillZero = function() {
    let value = this.valueOf();
    if (Number.isInteger(value) && 0<= value && value <= 9 )
        return "0" + value;
    return "" + value;
};

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
Date.prototype.getISOCalendar = function() {
    // Copy date so don't modify original
    let d = new Date(Date.UTC(this.getFullYear(), this.getMonth(), this.getDate()));
    // Set to nearest Thursday: current date + 4 - current day number
    // Make Sunday's day number 7
    d.setUTCDate(d.getUTCDate() + 4 - (d.getUTCDay()||7));
    // Get first day of year
    let yearStart = new Date(Date.UTC(d.getUTCFullYear(),0,1));
    // Calculate full weeks to nearest Thursday
    let weekNo = Math.ceil(( ( (d - yearStart) / 86400000) + 1)/7);
    // Return array of year and week number
    return [d.getUTCFullYear(), weekNo];
};
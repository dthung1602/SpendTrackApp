//
// Matt Kruse, http://www.javascripttoolbox.com/lib/date/source.php
// MIT licence
//

// Utility function to append a 0 to single-digit numbers
Date.LZ = function (x) {
    // noinspection JSConstructorReturnsPrimitive
    return (x < 0 || x > 9 ? "" : "0") + x
};

// Full month names. Change this for local month names
Date.monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
];

// Month abbreviations. Change this for local month names
Date.monthAbbreviations = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

// Full day names. Change this for local month names
Date.dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

// Day abbreviations. Change this for local month names
Date.dayAbbreviations = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

// Used for parsing ambiguous dates like 1/2/2000 - default to preferring 'American' format meaning Jan 2.
// Set to false to prefer 'European' format meaning Feb 1
Date.preferAmericanFormat = false;

// Parse a string and convert it to a Date object.
// If no format is passed, try a list of common formats.
// If string cannot be parsed, return null.
// Avoids regular expressions to be more portable.
Date.parseString = function (val, format) {
    // If no format is specified, try a few common formats
    if (typeof (format) == "undefined" || format == null || format === "") {
        let generalFormats = ['y-M-d', 'MMM d, y', 'MMM d,y', 'y-MMM-d', 'd-MMM-y', 'MMM d', 'MMM-d', 'd-MMM'];
        let monthFirst = ['M/d/y', 'M-d-y', 'M.d.y', 'M/d', 'M-d'];
        let dateFirst = ['d/M/y', 'd-M-y', 'd.M.y', 'd/M', 'd-M'];
        let checkList = [generalFormats, Date.preferAmericanFormat ? monthFirst : dateFirst, Date.preferAmericanFormat ? dateFirst : monthFirst];
        for (let i = 0; i < checkList.length; i++) {
            let l = checkList[i];
            for (let j = 0; j < l.length; j++) {
                let d = Date.parseString(val, l[j]);
                if (d !== null) {
                    return d;
                }
            }
        }
        return null;
    }

    this.isInteger = function (val) {
        for (let i = 0; i < val.length; i++) {
            if ("1234567890".indexOf(val.charAt(i)) === -1) {
                return false;
            }
        }
        return true;
    };

    this.getInt = function (str, i, minlength, maxlength) {
        for (let x = maxlength; x >= minlength; x--) {
            let token = str.substring(i, i + x);
            if (token.length < minlength) {
                return null;
            }
            if (this.isInteger(token)) {
                return token;
            }
        }
        return null;
    };
    val = val + "";
    format = format + "";
    let i_val = 0;
    let i_format = 0;
    let c = "";
    let token = "";
    let x, y;
    let year = new Date().getFullYear();
    let month = 1;
    let date = 1;
    let hh = 0;
    let mm = 0;
    let ss = 0;
    let ampm = "";
    while (i_format < format.length) {
        // Get next token from format string
        c = format.charAt(i_format);
        token = "";
        while ((format.charAt(i_format) === c) && (i_format < format.length)) {
            token += format.charAt(i_format++);
        }
        // Extract contents of value based on format token
        if (token === "yyyy" || token === "yy" || token === "y") {
            if (token === "yyyy") {
                x = 4;
                y = 4;
            }
            if (token === "yy") {
                x = 2;
                y = 2;
            }
            if (token === "y") {
                x = 2;
                y = 4;
            }
            year = this.getInt(val, i_val, x, y);
            if (year == null) {
                return null;
            }
            i_val += year.length;
            if (year.length === 2) {
                if (year > 70) {
                    year = 1900 + (year - 0);
                } else {
                    year = 2000 + (year - 0);
                }
            }
        } else if (token === "MMM" || token === "NNN") {
            month = 0;
            let names = (token === "MMM" ? (Date.monthNames.concat(Date.monthAbbreviations)) : Date.monthAbbreviations);
            for (let i = 0; i < names.length; i++) {
                let month_name = names[i];
                if (val.substring(i_val, i_val + month_name.length).toLowerCase() === month_name.toLowerCase()) {
                    month = (i % 12) + 1;
                    i_val += month_name.length;
                    break;
                }
            }
            if ((month < 1) || (month > 12)) {
                return null;
            }
        } else if (token === "EE" || token === "E") {
            let names = (token === "EE" ? Date.dayNames : Date.dayAbbreviations);
            for (let i = 0; i < names.length; i++) {
                let day_name = names[i];
                if (val.substring(i_val, i_val + day_name.length).toLowerCase() === day_name.toLowerCase()) {
                    i_val += day_name.length;
                    break;
                }
            }
        } else if (token === "MM" || token === "M") {
            month = this.getInt(val, i_val, token.length, 2);
            if (month == null || (month < 1) || (month > 12)) {
                return null;
            }
            i_val += month.length;
        } else if (token === "dd" || token === "d") {
            date = this.getInt(val, i_val, token.length, 2);
            if (date == null || (date < 1) || (date > 31)) {
                return null;
            }
            i_val += date.length;
        } else if (token === "hh" || token === "h") {
            hh = this.getInt(val, i_val, token.length, 2);
            if (hh == null || (hh < 1) || (hh > 12)) {
                return null;
            }
            i_val += hh.length;
        } else if (token === "HH" || token === "H") {
            hh = this.getInt(val, i_val, token.length, 2);
            if (hh == null || (hh < 0) || (hh > 23)) {
                return null;
            }
            i_val += hh.length;
        } else if (token === "KK" || token === "K") {
            hh = this.getInt(val, i_val, token.length, 2);
            if (hh == null || (hh < 0) || (hh > 11)) {
                return null;
            }
            i_val += hh.length;
            hh++;
        } else if (token === "kk" || token === "k") {
            hh = this.getInt(val, i_val, token.length, 2);
            if (hh == null || (hh < 1) || (hh > 24)) {
                return null;
            }
            i_val += hh.length;
            hh--;
        } else if (token === "mm" || token === "m") {
            mm = this.getInt(val, i_val, token.length, 2);
            if (mm == null || (mm < 0) || (mm > 59)) {
                return null;
            }
            i_val += mm.length;
        } else if (token === "ss" || token === "s") {
            ss = this.getInt(val, i_val, token.length, 2);
            if (ss == null || (ss < 0) || (ss > 59)) {
                return null;
            }
            i_val += ss.length;
        } else if (token === "a") {
            if (val.substring(i_val, i_val + 2).toLowerCase() === "am") {
                ampm = "AM";
            } else if (val.substring(i_val, i_val + 2).toLowerCase() === "pm") {
                ampm = "PM";
            } else {
                return null;
            }
            i_val += 2;
        } else {
            if (val.substring(i_val, i_val + token.length) !== token) {
                return null;
            } else {
                i_val += token.length;
            }
        }
    }
    // If there are any trailing characters left in the value, it doesn't match
    if (i_val !== val.length) {
        return null;
    }
    // Is date valid for month?
    if (month === 2) {
        // Check for leap year
        if (((year % 4 === 0) && (year % 100 !== 0)) || (year % 400 === 0)) { // leap year
            if (date > 29) {
                return null;
            }
        } else {
            if (date > 28) {
                return null;
            }
        }
    }
    if ((month === 4) || (month === 6) || (month === 9) || (month === 11)) {
        if (date > 30) {
            return null;
        }
    }
    // Correct hours value
    if (hh < 12 && ampm === "PM") {
        hh = hh - 0 + 12;
    } else if (hh > 11 && ampm === "AM") {
        hh -= 12;
    }
    return new Date(year, month - 1, date, hh, mm, ss);
};

// Check if a date string is valid
Date.isValid = function (val, format) {
    return (Date.parseString(val, format) !== null);
};

// Check if a date object is before another date object
Date.prototype.isBefore = function (date2) {
    if (date2 == null) {
        return false;
    }
    return (this.getTime() < date2.getTime());
};

// Check if a date object is after another date object
Date.prototype.isAfter = function (date2) {
    if (date2 == null) {
        return false;
    }
    return (this.getTime() > date2.getTime());
};

// Check if two date objects have equal dates and times
Date.prototype.equals = function (date2) {
    if (date2 == null) {
        return false;
    }
    return (this.getTime() === date2.getTime());
};

// Check if two date objects have equal dates, disregarding times
Date.prototype.equalsIgnoreTime = function (date2) {
    if (date2 == null) {
        return false;
    }
    let d1 = new Date(this.getTime()).clearTime();
    let d2 = new Date(date2.getTime()).clearTime();
    return (d1.getTime() === d2.getTime());
};

// Format a date into a string using a given format string
Date.prototype.format = function (format) {
    format = format + "";
    let result = "";
    let i_format = 0;
    let c = "";
    let token = "";
    let y = this.getYear() + "";
    let M = this.getMonth() + 1;
    let d = this.getDate();
    let E = this.getDay();
    let H = this.getHours();
    let m = this.getMinutes();
    let s = this.getSeconds();
    // Convert real date parts into formatted versions
    let value = {};
    if (y.length < 4) {
        y = "" + (+y + 1900);
    }
    value["y"] = "" + y;
    value["yyyy"] = y;
    value["yy"] = y.substring(2, 4);
    value["M"] = M;
    value["MM"] = Date.LZ(M);
    value["MMM"] = Date.monthNames[M - 1];
    value["NNN"] = Date.monthAbbreviations[M - 1];
    value["d"] = d;
    value["dd"] = Date.LZ(d);
    value["E"] = Date.dayAbbreviations[E];
    value["EE"] = Date.dayNames[E];
    value["H"] = H;
    value["HH"] = Date.LZ(H);
    if (H === 0) {
        value["h"] = 12;
    } else if (H > 12) {
        value["h"] = H - 12;
    } else {
        value["h"] = H;
    }
    value["hh"] = Date.LZ(value["h"]);
    value["K"] = value["h"] - 1;
    value["k"] = value["H"] + 1;
    value["KK"] = Date.LZ(value["K"]);
    value["kk"] = Date.LZ(value["k"]);
    if (H > 11) {
        value["a"] = "PM";
    } else {
        value["a"] = "AM";
    }
    value["m"] = m;
    value["mm"] = Date.LZ(m);
    value["s"] = s;
    value["ss"] = Date.LZ(s);
    while (i_format < format.length) {
        c = format.charAt(i_format);
        token = "";
        while ((format.charAt(i_format) === c) && (i_format < format.length)) {
            token += format.charAt(i_format++);
        }
        if (typeof (value[token]) !== "undefined") {
            result = result + value[token];
        } else {
            result = result + token;
        }
    }
    return result;
};

// Get the full name of the day for a date
Date.prototype.getDayName = function () {
    return Date.dayNames[this.getDay()];
};

// Get the abbreviation of the day for a date
Date.prototype.getDayAbbreviation = function () {
    return Date.dayAbbreviations[this.getDay()];
};

// Get the full name of the month for a date
Date.prototype.getMonthName = function () {
    return Date.monthNames[this.getMonth()];
};

// Get the abbreviation of the month for a date
Date.prototype.getMonthAbbreviation = function () {
    return Date.monthAbbreviations[this.getMonth()];
};

// Get the ISO week number
Date.prototype.getISOCalendar = function () {
    let d = new Date(Date.UTC(this.getFullYear(), this.getMonth(), this.getDate()));
    d.setUTCDate(d.getUTCDate() + 4 - (d.getUTCDay() || 7));
    let yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
    let weekNo = Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
    return [d.getUTCFullYear(), weekNo];
};

// Clear all time information in a date object
Date.prototype.clearTime = function () {
    this.setHours(0);
    this.setMinutes(0);
    this.setSeconds(0);
    this.setMilliseconds(0);
    return this;
};

// Add an amount of time to a date. Negative numbers can be passed to subtract time.
Date.prototype.add = function (interval, number) {
    if (typeof (interval) == "undefined" || interval === null || typeof (number) == "undefined" || number == null) {
        return this;
    }
    number = +number;
    if (interval === 'y') { // year
        this.setFullYear(this.getFullYear() + number);
    } else if (interval === 'M') { // Month
        this.setMonth(this.getMonth() + number);
    } else if (interval === 'd') { // Day
        this.setDate(this.getDate() + number);
    } else if (interval === 'w') { // Weekday
        let step = (number > 0) ? 1 : -1;
        while (number !== 0) {
            this.add('d', step);
            while (this.getDay() === 0 || this.getDay() === 6) {
                this.add('d', step);
            }
            number -= step;
        }
    } else if (interval === 'h') { // Hour
        this.setHours(this.getHours() + number);
    } else if (interval === 'm') { // Minute
        this.setMinutes(this.getMinutes() + number);
    } else if (interval === 's') { // Second
        this.setSeconds(this.getSeconds() + number);
    }
    return this;
};

// Get the week number in year
Date.prototype.getWeekNumber = function () {
    let d = new Date(Date.UTC(this.getFullYear(), this.getMonth(), this.getDate()));
    let dayNum = d.getUTCDay() || 7;
    d.setUTCDate(d.getUTCDate() + 4 - dayNum);
    let yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
    return Math.ceil((((d - yearStart) / 86400000) + 1) / 7)
};

// Return week number in year
Date.prototype.toISODateString = function () {
    return this.toISOString().substr(0, 10);
};

// Return number of days between date1 and date2
Date.daysBetween = function (date1, date2) {
    return Math.floor((date2.getTime() - date1.getTime()) / (1000 * 60 * 60 * 24)) + 1;
};

// Return a string accepted as value of input datetime local
// useSpace: whether to use space instead of T
Date.prototype.toDatetimeLocal = function (useSpace = false) {
    let s = this.format('yyyy-MM-ddTHH:mm:ss');
    return useSpace ? s.replace('T', ' ') : s;
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

/**
 * Delete all cookies
 * Exception:
 *      - Cookies with HttpOnly flag set
 *      - Cookies that have been set with a Path value
 */
function deleteAllCookies() {
    let cookies = document.cookie.split(";");

    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i];
        const eqPos = cookie.indexOf("=");
        const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
        document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT";
    }
}

/**
 * Display ajax request errors
 * @param response
 * @param status
 * @param error
 */
function displayError(response, status, error) {
    switch (error) {
        case 'Bad Request':
            let errorMessages = [];
            response = response.responseJSON;
            for (let e in response)
                if (response.hasOwnProperty(e))
                    errorMessages.push(e + ': ' + response[e].join(','));
            alert(errorMessages.join('\n'));
            break;
        case 'Internal Server Error':
            alert("Internal Server Error\nPlease try again later");
            break;
        default :
            alert("Unknown error\nPlease try again later");
    }
}

function setDateNow(element) {
    $(element).val(new Date().format('yyyy-MM-dd'));
}

function setDateTime(element, datetime = null) {
    if (datetime === null)
        datetime = new Date();
    if (datetime instanceof Date)
        datetime = datetime.format('yyyy-MM-ddTHH:mm');
    if (checkBrowser() === "Firefox")
        datetime = datetime.replace('T', ' ');
    $(element).val(datetime);
}

function storeData(name, key, value) {
    name = '__' + name + '__';
    if (!window.hasOwnProperty(name))
        window[name] = {};
    let oldValue = window[name][key];
    window[name][key] = value;
    return oldValue;
}

function retrieveData(name, key, deleteOldData = false) {
    name = '__' + name + '__';
    if (!window.hasOwnProperty(name))
        return;
    let result = window[name][key];
    if (deleteOldData)
        delete window[name][key];
    return result;
}

function checkBrowser() {
    const c = navigator.userAgent.search("Chrome");
    const f = navigator.userAgent.search("Firefox");
    const m8 = navigator.userAgent.search("MSIE 8.0");
    const m9 = navigator.userAgent.search("MSIE 9.0");
    let browser;
    if (c > -1) {
        browser = "Chrome";
    } else if (f > -1) {
        browser = "Firefox";
    } else if (m9 > -1) {
        browser = "IE9";
    } else if (m8 > -1) {
        browser = "IE8";
    } else {
        browser = "Unknown"
    }
    return browser;
}

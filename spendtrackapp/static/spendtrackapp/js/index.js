daysInWeekNames = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
monthNames = ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"];

function fillZero(n) {
    if (n < 10) n = "0" + n;
    return n;
}

function startTime() {
    let now = new Date();

    let year = now.getFullYear();
    let month = fillZero(now.getMonth() + 1);
    let day = fillZero(now.getDate());
    let dayInWeek = daysInWeekNames[now.getDay()];
    let hour = fillZero(now.getHours());
    let minute = fillZero(now.getMinutes());
    let second = fillZero(now.getSeconds());

    let clock = document.getElementById("clock");
    clock.innerHTML = "<div>" + dayInWeek + " " + day + "/" + month + "/" + year
        + "</div><div>" + hour + ":" + minute + ":" + second + "</div>";

    setTimeout(startTime, 1000)
}

function showDropDown(id) {
    document.getElementById(id).classList.toggle('show')
}

function select(categoryId) {
    document.getElementById('category_id').value = categoryId;
    document.getElementById('category-display').innerText = document.getElementById('cat-' + categoryId).innerText;
}

function setDatetimeNow() {
    let d = new Date();
    let datetime = [d.getFullYear(), fillZero(d.getMonth() + 1), fillZero(d.getDate())].join('-')
        + ' ' + [fillZero(d.getHours()), fillZero(d.getMinutes())].join(':');
    let datetimeField = document.getElementById('date');
    datetimeField.value = datetime;
    if (datetimeField.value !== datetime)
        datetimeField.value = datetime.replace(' ', 'T')
}

function clearFields() {
    $('input[name!="csrfmiddlewaretoken"]').each(function (index, element) {
        element.value = ''
    });
    $('#category-display').html('Select a category');
}


function submitForm() {
    let csrfToken = $('[name="csrfmiddlewaretoken"]').val();
    let date = $('#date').val().replace('T', ' ');
    let content = $('#content').val().trim();
    let categoryId = $('#category_id').val();
    let value = $('#value').val();

    let addSuccess = function (response) {
        let row = $('<tr>').appendTo($('tbody'));
        let categoryDisplay = $('#category-display');
        let totalInWeek = $('#total-in-week');

        value = parseFloat(value);
        date = new Date(date);
        date = daysInWeekNames[date.getDay()].substr(0, 3) + " "
            + monthNames[date.getMonth()].substr(0, 3) + " "
            + fillZero(date.getDate()) + ", "
            + fillZero(date.getHours() % 12) + " "
            + (date.getHours() >= 12 ? 'PM' : 'AM');

        $('<td>').text(date).appendTo(row);
        $('<td>').text(content).appendTo(row);
        $('<td class="right-align">').text(value.toFixed(2)).appendTo(row);
        $('<td class="right-align">').text(categoryDisplay.html()).appendTo(row);

        value = parseFloat(totalInWeek.text()) + value;
        totalInWeek.text(value.toFixed(2));
        $('.input-error').hide();
        clearFields();
    };

    let addError = function (response, status, error) {
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
    };

    let error = false;
    $('.input-error').hide();

    if (isNaN(Date.parse(date))) {
        error = true;
        $('#date-error').show().html('Datetime must have format yyyy-mm-ddThh:mm');
    }

    if (content === "") {
        error = true;
        $('#content-error').show().html('Content cannot be empty');
    }

    if (categoryId === "") {
        error = true;
        $('#category-error').show().html('A category must be selected');
    }

    try {
        if (!value.match('^[0-9 \\+\\-\\*\\/\\(\\)\\.]+$'))
            throw "";
        value = eval(value).toFixed(2);
    } catch (err) {
        error = true;
        $('#value-error').show().html('Invalid arithmetic expression');
    }

    if (error) return;

    let data = {
        csrfmiddlewaretoken: csrfToken,
        date: date,
        content: content,
        category_id: categoryId,
        value: value
    };

    $.ajax({
        url: '/add/',
        type: 'POST',
        dataType: 'json',
        data: data,
        success: addSuccess,
        error: addError,
    });
}

window.onclick = function (event) {
    if (!event.target.matches('.clickable')) {
        let dropDowns = document.getElementsByClassName("select-content");
        for (let i = 0; i < dropDowns.length; i++) {
            let openDropDown = dropDowns[i];
            if (openDropDown.classList.contains('show')) {
                openDropDown.classList.remove('show');
            }
        }
    }
};
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

    $("#clock")
        .html('')
        .append($('<div>').html(now.format('EE dd/MM/yyyy')))
        .append($('<div>').html(now.format('HH:mm:ss')));

    setTimeout(startTime, 1000)
}

// ------------------------ FORM -----------------------

class Entry {
    constructor(data) {
        this.id = data.id;
        this.date = data.date;
        this.content = data.content;
        this.leaf_category = data.leaf_category;
        this.value = data.value;

        this.errors = {};
        this.clean()
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

    clean() {
        // validate date
        let d = Date.parse(this.date);
        if (isNaN(d))
            this.addError('date', 'Invalid date format');
        else
            this.date = new Date(d);

        // validate content
        this.content = this.content.trim();
        if (this.content.length === 0)
            this.addError('content', 'Content cannot be empty');
        if (this.content.length > 200)
            this.addError('content', 'Content is too long');

        // validate category
        if (this.leaf_category === "empty" || categoryHiddenData.id.indexOf(this.leaf_category) === -1)
            this.addError('leaf_category', 'Invalid category id');

        // validate value
        try {
            if (!this.value.match(/^[0-9 +\-*/().]+$/)) { // noinspection ExceptionCaughtLocallyJS
                throw "";
            }
            this.value = eval(this.value);
        } catch (err) {
            this.addError('value', 'Invalid arithmetic expression');
        }
    }

    getSubmitData() {
        let object = {
            csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val()
        };
        for (let i = 0; i < Entry.fields.length; i++) {
            let field = Entry.fields[i];
            object[field] = this[field];
        }
        object.date = this.date.format('yyyy-MM-dd HH:mm:ss');
        return object;
    }

    getCategoryName() {
        return categoryHiddenData.name[categoryHiddenData.id.indexOf(this.leaf_category)]
    }

    getDescription() {
        return '[' + this.date.toISODateString() + '] ' + this.content;
    }

    toRow() {
        const prefix = 'entry-' + this.id + '-';
        let pageCount = Math.max($('.page-control div').length, 1);
        let row = $('<tr>')
            .attr('id', 'entry-row-' + this.id)
            .addClass('table-page-' + pageCount);

        $('<td id="' + prefix + 'date">').text(this.date.format('E NNN d, h a')).appendTo(row);
        $('<td id="' + prefix + 'content">').text(this.content).appendTo(row);
        $('<td id="' + prefix + 'value" class="align-right">').text(this.value.toFixed(2)).appendTo(row);
        $('<td id="' + prefix + 'category" class="align-right">').text(this.getCategoryName()).appendTo(row);
        $('<td class="entry-edit">').appendTo(row)
            .append($('<img src="/static/spendtrackapp/img/edit-icon.png" alt="edit" onclick="editEntry(' + this.id + ')">'));


        if (pageCount > 1) {
            let visible = $('.table-page-' + pageCount).is(':visible');
            if (!visible) row.hide();
        }

        return row;
    }
}

Entry.fields = ['date', 'content', 'leaf_category', 'value'];

/**
 * Clear all input fields in new entry form
 */
function clearNewEntryFields() {
    $('#new-entry [id^=entry]').val('');
    Category.clearSelectCategoryField(entryCatFieldId);
    $('#new-entry .input-error').hide();
}

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
function addNewEntryFail(response, status, error) {
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
                        causes.push(f + ": " + r[j])
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
 * @param entry: object contain submit data
 * @returns {Function} a function that update page content when a new entry is added successfully
 */
function addNewEntrySuccessFuncGenerator(entry) {
    return function (response) {
        entry.id = response.id;

        // get elements
        let totalInWeek = $('#total-in-week');
        let totalInMonth = $('#total-in-month');
        let now = new Date();
        let submitDate = new Date(entry.date);
        let wn = submitDate.getWeekNumber();
        let m = submitDate.getMonth();
        let y = submitDate.getFullYear();

        // inform success
        $('#new-entry-success-panel').show().html('Item added to week ' + wn + ' of year ' + y);

        // add item to table if the item belongs to this week
        if (now.getWeekNumber() === wn || now.getFullYear() === y) {
            $('#entry-container').append(entry.toRow());
            totalInWeek.text((parseFloat(totalInWeek.text()) + entry.value).toFixed(2));
        }

        // change total in week
        if (now.getMonth() === m && now.getFullYear() === y)
            totalInMonth.text((parseFloat(totalInMonth.text()) + entry.value).toFixed(2));

        // clear form
        $('#entry-container .no-data').remove();
        clearNewEntryFields();

        // enable submit button again
        enableAddEntryButton();
    }
}

/**
 *  Validate form, submit and handle result
 */
function submitNewEntryForm() {
    // get values to submit
    let entry = new Entry(getNewEntryData());

    $('#new-entry .input-error').hide();

    if (entry.isValid()) {
        // disable button until a response is received
        disableAddEntryButton();

        // send ajax request
        $.ajax({
            url: '/entry/add/',
            type: 'POST',
            dataType: 'json',
            data: entry.getSubmitData(),
            success: addNewEntrySuccessFuncGenerator(entry),
            error: addNewEntryFail,
        });
    } else {
        for (let i = 0; i < Entry.fields.length; i++) {
            let field = Entry.fields[i];
            if (entry.errors.hasOwnProperty(field)) {
                let errorHTML = entry.errors[field].join('<br>');
                $('#entry-' + field.replace('_', '-') + '-error').html(errorHTML).show();
            }
        }
    }
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

// ------------- EDIT ENTRY ----------------

function getEditEntryData(entryId) {
    const prefix = '#edit-entry-' + entryId + '-';
    return {
        'id': entryId,
        'date': $(prefix + 'date'),
        'content': $(prefix + 'content'),
        'value': $(prefix + 'value'),
        'leaf_category': $(prefix + 'category'),
    }
}

function editEntrySuccessFunc(entry) {
    return function (response) {
        $('#entry-row-' + entry.id)
            .removeClass('editing')
            .html(entry.toRow().html());
    }
}

function saveEntryFuncGenerator(entryId) {
    return function () {
        let entry = new Entry(getEditEntryData(entryId));

        if (entry.isValid()) {
            $.ajax({
                url: '/entry/edit/',
                type: 'POST',
                dataType: 'json',
                data: entry,
                success: editEntrySuccessFunc(entry),
                error: displayError,
            })
        } else {
            for (let i = 0; i < Entry.fields.length; i++) {
                let f = Entry.fields[i];
                if (entry.errors.hasOwnProperty(f)) {
                    $('#edit-entry-' + entryId + '-' + f)
                        .parent().find('.input-error')
                        .html(entry.errors[f].join('<br>'))
                }
            }
        }
    }
}

function deleteEntryFuncGenerator(entryId) {
    return function () {
        if (!confirm("Are you sure to delete this entry?")) return;

        let data = {
            csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val(),
            id: entryId
        };
        $.ajax({
            url: '/entry/delete/',
            type: 'POST',
            dataType: 'json',
            data: data,
            success: () => {
                $('#entry-row-' + entryId).remove();
                alert("Entry deleted successfully!");
            },
            error: displayError,
        })
    }
}

function cancelEditEntry(entryId) {
    $('#entry-row-' + entryId)
        .removeClass('editing')
        .html(retrieveData('entry', entryId));
}

function editEntry(entryId) {
    let row = $('#entry-row-' + entryId).addClass('editing');
    const idPrefix = 'entry-' + entryId + '-';
    const selectorPrefix = '#' + idPrefix;

    // ---- backup old data ----
    storeData('entry', entryId, row.html());

    // ---- get old data ----
    let dateValue = Date.parseString($(selectorPrefix + 'date').text(), 'E NNN dd, H a').toDatetimeLocal();
    let content = $(selectorPrefix + 'content').text();
    let value = $(selectorPrefix + 'value').text();
    let categoryName = $(selectorPrefix + 'category').text();
    let categoryId = categoryHiddenData.id[categoryHiddenData.name.indexOf(categoryName)];
    let categoryData = {id: categoryId, name: categoryName};

    let dateFieldId = 'edit-' + idPrefix + 'date';
    let categoryFieldId = 'edit-' + idPrefix + 'category';
    let contentFieldId = 'edit-' + idPrefix + 'content';
    let valueFieldId = 'edit-' + idPrefix + 'value';

    row.html(
        '<td colspan="5">' +
        '    <div class="row">' +
        '        <div class="five columns">' +
        '            <input type="datetime-local" id="' + dateFieldId + '" placeholder="yyyy-mm-dd hh:mm" autocomplete="off">' +
        '            <button>NOW</button>' +
        '            <div class="input-error"></div>' +
        '        </div>' +
        '        <div class="seven columns">' +
        '            <input type="text" id="' + contentFieldId + '" placeholder="A carrot and an apple" maxlength="200">' +
        '            <div class="input-error"></div>' +
        '        </div>' +
        '    </div>' +
        '    <div class="row">' +
        '        <div class="five columns">' +
        '            <div id="' + categoryFieldId + '"></div>' +
        '            <div class="input-error"></div>' +
        '        </div>' +
        '        <div class="seven columns">' +
        '            <input type="text" id="' + valueFieldId + '" placeholder="1.25 + 2.3 * 5" ' +
        '                   pattern="^[0-9 \\+\\-\\*\\/\\(\\)\\.]+$">' +
        '            <div class="input-error"></div>' +
        '        </div>' +
        '    </div>' +
        '    <div class="row submit-row align-right">' +
        '        <button class="button-primary">SAVE</button>' +
        '        <button>CANCEL</button>' +
        '        <button class="button-danger">DELETE</button>' +
        '    </div>' +
        '</td>'
    );

    $('#' + dateFieldId).val(dateValue);
    $('#' + contentFieldId).val(content);
    $('#' + valueFieldId).val(value);
    $('#' + categoryFieldId).html(Category.toDropdownMenu(categoryFieldId, false));
    Category.generateSelectCategoryFunc(categoryFieldId, categoryData)();

    row.find('button:contains("SAVE")').click(saveEntryFuncGenerator(entryId));
    row.find('button:contains("DELETE")').click(deleteEntryFuncGenerator(entryId));
    row.find('button:contains("NOW")').click(() => {
        setDateTimeNow("#" + dateFieldId)
    });
    row.find('button:contains("CANCEL")').click(() => {
        cancelEditEntry(entryId)
    });
}

// ------------- PLAN OBJECT ----------------

class Plan {
    constructor(data) {
        this.id = data.id;
        this.name = data.name;
        this.start_date = data.start_date;
        this.end_date = data.end_date;
        this.category = data.category;
        this.compare = data.compare;
        this.planned_total = data.planned_total;
        this.total = data.total;
        this.category_name = categoryHiddenData.name[categoryHiddenData.id.indexOf(this.category)];

        this.errors = {};
        this.clean();
    }

    /**
     * A string describes the plan
     * @returns {string}
     */
    getTarget() {
        let compare = {"<": "less than", ">": "greater than", "=": "equal to"}[this.compare];
        let catName = (this.category === "") ? "all category" : "\"" + this.category_name + "\"";
        return "Total in " + catName + " is " + compare + " " + this.planned_total;
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

    /**
     * Validate all fields
     */
    clean() {
        // validate start date and end date
        if (isNaN(Date.parse(this.start_date)))
            this.addError('start_date', 'Invalid date format');
        if (isNaN(Date.parse(this.end_date)))
            this.addError('end_date', 'Invalid date format');

        if (this.isValid()) {
            let today = (new Date()).toISODateString();
            if (this.start_date > this.end_date)
                this.addError('end_date', 'End date must come after start date');
            // if (this.start_date < today)
            //     this.addError('start_date', 'Start date must not in the past');
        }

        // content must not be empty
        if (this.name === "")
            this.addError('name', 'Name cannot be empty');

        // category must not be empty
        if (this.category === "empty")
            this.addError('category', 'A category must be selected');

        // compare must be <, > or =
        if (['<', '>', '='].indexOf(this.compare) === -1)
            this.addError('compare', 'Compare must be <, > or =');

        // evaluate arithmetic expression in planned total field
        try {
            if (!this.planned_total.match(/^[0-9 +\-*/().]+$/))
                throw "";
            this.planned_total = eval(this.planned_total).toFixed(2);
        } catch (err) {
            this.addError('planned_total', 'Invalid arithmetic expression');
        }
    }

    /**
     * Evaluate plan as good, warning or fail
     * @param timeRatio: time elapsed since start date / time of plan
     * @param planRatio: total spent / planned
     * @param compare: <, > or =
     * @returns {string} "good", "warning" or "fail"
     */
    static evaluatePlan(timeRatio, planRatio, compare) {
        let planEvaluate = '';

        switch (compare) {
            case '>':
                if (planRatio >= timeRatio)
                    planEvaluate = 'good';
                else
                    planEvaluate = 'warning';
                break;
            case '<':
                if (planRatio <= timeRatio)
                    planEvaluate = 'good';
                else if (planRatio <= 1)
                    planEvaluate = 'warning';
                else
                    planEvaluate = 'fail';
                break;
            default:
                let ratio = planRatio / timeRatio;
                if (ratio < 0.9)
                    planEvaluate = 'warning';
                else if (ratio > 1.1) {
                    if (planRatio > 1.1)
                        planEvaluate = 'fail';
                    else
                        planEvaluate = 'warning'
                } else
                    planEvaluate = 'good';
        }

        return planEvaluate;
    }

    /**
     * Create and return a progress bars for a plan
     */
    createProgressBars() {
        let startDate = new Date(this.start_date);
        let endDate = new Date(this.end_date);
        let today = new Date();
        let totalDaysInPlan = daysBetween(startDate, endDate);
        let daysElapsed = daysBetween(startDate, today);
        let timeRatio = daysElapsed / totalDaysInPlan * 100;
        let planRatio = this.total / this.planned_total * 100;

        // choose color for plan bar
        let planEvaluation = Plan.evaluatePlan(timeRatio, planRatio, this.compare);
        let backgroundColor = '';
        let foregroundColor = '';

        switch (planEvaluation) {
            case 'good':
                backgroundColor = '#00ad17';
                foregroundColor = 'green';
                break;
            case 'warning':
                backgroundColor = '#ffbd5a';
                foregroundColor = '#e28d07';
                break;
            default:
                backgroundColor = '#e28986';
                foregroundColor = 'red';
        }

        // create progress bars container
        let timeProgress = $('<div id="time-progress-' + this.id + '">');
        let planProgress = $('<div id="plan-progress-' + this.id + '">');
        let container = $('<div class="progress-bar-group">')
            .append(timeProgress).append(planProgress);

        // create time bar
        new ProgressBar(timeProgress, timeRatio, {
            backgroundColor: '#296a84',
            foregroundColor: '#183f62',
            type: 'line'
        });

        // create plan bar
        new ProgressBar(planProgress, planRatio, {
            backgroundColor: backgroundColor,
            foregroundColor: foregroundColor,
            type: 'line'
        });

        return container;
    }

    /**
     * Create and return a row that contains the plan
     * @returns {jQuery.fn.init|jQuery|HTMLElement}
     */
    createPlanRow() {
        // --- create row ---
        let rootPane = $('<div id="plan-row-' + this.id + '" class="plan">');
        let headPane = $('<div>').appendTo(rootPane);
        let bodyPane = $('<div class="row">').appendTo(rootPane);

        // --- head pane ---
        $('<span class="plan-name">').text(this.name).appendTo(headPane);
        $('<span class="align-right plan-edit-icon">')
            .html('<img src="/static/spendtrackapp/img/edit-icon.png" alt="edit" ' +
                'onclick="editPlan(' + this.id + ')">')
            .appendTo(headPane);

        // --- left pane ---
        let leftPane = $('<div class="five columns">').appendTo(bodyPane);
        let table = $('<table>').appendTo(leftPane);
        let tableBody = $('<tbody>').appendTo(table);
        // start date
        $('<tr>').appendTo(tableBody)
            .append($('<td>').text('From'))
            .append($('<td>').text(this.start_date));
        // end date
        $('<tr>').appendTo(tableBody)
            .append($('<td>').text('To'))
            .append($('<td>').text(this.end_date));
        // target
        $('<tr>').appendTo(tableBody)
            .append($('<td>').text('Target'))
            .append($('<td>').text(this.getTarget()));
        // total
        $('<tr>').appendTo(tableBody)
            .append($('<td>').text('Total'))
            .append($('<td>').text(this.total));

        // --- right pane ---
        let rightPane = $('<div class="seven columns">').appendTo(bodyPane);

        // plan hidden inputs fields
        for (let i = 0; i < this.fields.length; i++) {
            let f = this.fields[i];
            $('<input type="hidden" id="plan-data-' + this.id + '-' + f.replace('_', '-') + '">')
                .appendTo(rightPane).val(this[f]);
        }

        // progress bars
        rightPane.append(this.createProgressBars(this.id));

        return rootPane;
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

Plan.prototype.fields = [
    'id', 'name', 'start_date', 'end_date', 'category', 'category_name',
    'compare', 'planned_total', 'total'
];

/**
 * Create and return an object contains plan data from hidden input
 *
 * @param planId: a number indicates the order the plan
 */
function getPlanDataFromHiddenInput(planId) {
    let rootNode = $('#plan-row-' + planId);
    let prefix = '#plan-data-' + planId + '-';
    let fields = Plan.prototype.fields;
    let data = {};
    for (let i = 0; i < fields.length; i++) {
        let fieldId = prefix + fields[i].replace('_', '-');
        data[fields[i]] = rootNode.find(fieldId).val()
    }
    return data;
}

/**
 * Create Progress bars when page finish loading
 * @param n: number of plans
 */
function createAllProgressBars(n) {
    $('[id^="plan-row-"]').each(
        function () {
            let id = this.id.substring(9);
            let plan = new Plan(getPlanDataFromHiddenInput(id));
            $('#plan-row-' + id + ' .seven')
                .append(plan.createProgressBars(id))
        }
    )
}

// ------------- NEW PLAN FORM ----------------

/**
 * Set today to start date field in new plan form
 */
function setNewPlanStartDateToday() {
    let d = new Date();
    let today = [d.getFullYear(), (d.getMonth() + 1).fillZero(), d.getDate().fillZero()].join('-');
    $('#plan-start-date').val(today);
}

/**
 * Clear all input fields in new plan form
 */
function clearNewPlanFields() {
    $('#new-plan [id^=plan]').val('');
    Category.clearSelectCategoryField(planCatFieldId);
    $('#new-plan .input-error').hide();
}

/**
 * Return an object contains all fields in new plan form
 */
function getNewPlanData() {
    return {
        name: $('#plan-name').val().trim(),
        start_date: $('#plan-start-date').val(),
        end_date: $('#plan-end-date').val(),
        category: $('#plan-category').val(),
        compare: $('#plan-compare').val(),
        planned_total: $('#plan-planned-total').val()
    }
}

/**
 * Display errors when submitting new plan form
 * @param response
 * @param status
 * @param error
 */
function addNewPlanError(response, status, error) {
    switch (error) {
        case 'Bad Request':
            let fields = ['name', 'start_date', 'end_date', 'category', 'compare', 'planned_total'];
            for (let i = 0; i < fields.length; i++) {
                let field = fields[i];
                if (response['responseJSON'].hasOwnProperty(field)) {
                    let errors = response['responseJSON'][field];
                    let errorField = $('#plan-' + field.replace('_', '-') + '-error');
                    errorField.html(errors.join('<br>')).show();
                }
            }
            break;
        case 'Internal Server Error':
            alert("Internal Server Error\nPlease try again later");
            break;
        default :
            alert("Unknown error\nPlease try again later");
    }
}

/**
 * Create a function to call when new plan is added successfully
 * @param plan: object contain submit data
 * @returns {Function} a function that update page content when a new entry is added successfully
 */
function addNewPlanSuccessFunc(plan) {
    return function (response) {
        // update plan
        plan.id = response.id;
        plan.total = response.total;

        // if today is in plan's time period add new row
        let today = new Date().toISODateString();
        if (plan.start_date <= today && today <= plan.end_date) {
            let currentPlansContainer = $('#plan-list');

            // clear 'no-data' div
            currentPlansContainer.find('.no-data').parent().remove();

            // hide add success panel
            $('#plan-add-success-panel').hide();

            // add new plan container
            currentPlansContainer.append(plan.createPlanRow());

        } else { // else just announce success
            $('#plan-add-success-panel').show().html('Plan "' + plan.name + '" has been added.');
        }

        // clear form
        clearNewPlanFields();
    }
}


/**
 *  Validate new plan form, submit and handle result
 */
function submitNewPlanForm() {
    let plan = new Plan(getNewPlanData());

    // clear error fields
    $('[id^="plan-"][id$="-error"]').html('');

    if (plan.isValid()) {
        // valid -> send AJAX
        $.ajax({
            url: '/plan/add/',
            type: 'POST',
            dataType: 'json',
            data: plan.getSubmitData(),
            success: addNewPlanSuccessFunc(plan),
            error: addNewPlanError,
        });

    } else {
        // invalid -> display error
        for (let i = 1; i < plan.fields.length; i++) { // skip id -> i = 1
            let field = plan.fields[i];
            if (plan.errors.hasOwnProperty(field)) {
                let errorHTML = plan.errors[field].join('<br>');
                $('#plan-' + field.replace('_', '-') + '-error').show().html(errorHTML);
            }
        }
    }
}

// ------------- SEARCH PLAN FORM ----------------

/**
 * Display found plans, if any, after a search query is performed successfully
 * @param response
 */
function successSearchPlanFunc(response) {
    // get elements
    let foundPlansContainer = $('#plan-list').html('').show();
    let plans = response['plans'];

    // display found plans
    if (plans.length > 0) {
        for (let i = 0; i < plans.length; i++) {
            let plan = new Plan(plans[i]);
            foundPlansContainer.append(plan.createPlanRow());
        }
        return
    }

    // nothing found
    foundPlansContainer
        .append($('<div class="row box">')
            .append($('<div class="no-data twelve columns">').text('No plan is found!')));
}

/**
 * Inform user that the search query has failed
 * @param response
 * @param status
 * @param error
 */
function failSearchPlanFunc(response, status, error) {
    let errorField = $('#search-input-error').show();
    switch (error) {
        case 'Bad Request':
            let errorContent = "";
            let keys = Object.keys(response['responseJSON']);
            for (let i = 0; i < keys.length; i++) {
                errorContent += keys[i] + ": " + response['responseJSON'][keys[i]].join('; ') + '<br>';
            }
            errorField.html(errorContent);
            break;
        case 'Internal Server Error':
            errorField.html("Internal Server Error. Please try again later");
            break;
        default :
            errorField.html("Unknown error. Please try again later");
    }
}

/**
 * Validate and submit search plan form
 * @param url
 */
function submitSearchPlanForm(url) {
    submitSearchFormAJAX(
        url,
        successSearchPlanFunc,
        failSearchPlanFunc
    )
}

// ------------- EDIT PLAN FORM ----------------

function editPlan(planId) {
    // --- get containers ---
    let rootNode = $('#plan-row-' + planId).addClass('editing');
    let leftPane = rootNode.find('.five');
    let rightPane = rootNode.find('.seven');

    // --- store old data ---
    $('<div id="plan-' + planId + '-old-data">')
        .append(rootNode.clone())
        .appendTo($('body'))
        .hide();

    // --- get plan info specified in #plan-list ---
    let prefix = '#plan-data-' + planId + '-';
    let name = $(prefix + 'name').val();
    let categoryId = $(prefix + 'category').val();
    let categoryName = $(prefix + 'category-name').val();
    let startDate = $(prefix + 'start-date').val();
    let endDate = $(prefix + 'end-date').val();
    let plannedTotal = parseInt($(prefix + 'planned-total').val());
    let compare = $(prefix + 'compare').val();

    // --- add input fields ---

    // name
    rootNode.find('.plan-name')
        .html($('<input type="text" name="name">').val(name));

    // start date
    leftPane.find('tr:nth-child(1) td:last-child')
        .html($('<input type="date" name="start-date">').val(startDate));

    // end date
    leftPane.find('tr:nth-child(2) td:last-child')
        .html($('<input type="date" name="end-date">').val(endDate));

    // category
    let editCatId = 'edit-category-' + planId;
    let categoryField = $('<div id="' + editCatId + '">')
        .html(Category.toDropdownMenu(editCatId, true));

    // compare
    let compareField = $('<select name="compare">')
        .append($('<option value="<">').text('less than'))
        .append($('<option value=">">').text('greater than'))
        .append($('<option value="=">').text('equal to'))
        .val(compare);

    // planned total
    let plannedTotalField = $('<input type="text" name="planned-total">').val(plannedTotal);

    // target
    leftPane.find('tr:nth-child(3) td:last-child')
        .text('')
        .append(categoryField)
        .append(compareField)
        .append(plannedTotalField);

    // select the old category
    let data = {
        id: categoryId,
        name: categoryName
    };
    Category.generateSelectCategoryFunc(editCatId, data)();

    // add input error field
    $('<div class="input-error">').appendTo(rightPane).hide();

    // add save, cancel, delete buttons
    $('<div class="align-right edit-button-group">')
        .appendTo(rightPane)
        .append($('<button class="button-primary" onclick="savePlan(' + planId + ')">').text('SAVE'))
        .append($('<button onclick="cancelPlanEdit(' + planId + ')">').text('CANCEL'))
        .append($('<button onclick="deletePlan(' + planId + ')">').text('DELETE'));

    // remove edit button
    rootNode.find('.plan-edit-icon').remove();
}

/**
 * Return an object contains all submit data
 */
function getEditPlanData(planId) {
    let rootNode = $('#plan-row-' + planId);
    let fields = Plan.prototype.fields;
    let data = {};
    for (let i = 0; i < fields.length; i++) {
        let f = fields[i].replace('_', '-');
        data[fields[i]] = rootNode.find('[name="' + f + '"]').val()
    }
    data['category'] = $('#edit-category-' + planId).val();
    data['id'] = planId;
    return data;
}

function savePlan(planId) {
    let plan = new Plan(getEditPlanData(planId));

    if (plan.isValid()) {
        // send ajax request
        $.ajax({
            url: '/plan/edit/',
            type: 'POST',
            dataType: 'json',
            data: plan.getSubmitData(),
            success: editPlanSuccessFunc(plan),
            error: editPlanError,
        });
        // hide error
        $('#plan-row-' + planId + ' .input-error').hide();

    } else {
        // display errors
        let errors = [];
        for (let i = 0; i < plan.fields.length; i++) {
            let f = plan.fields[i];
            if (plan.errors.hasOwnProperty(f))
                errors = errors.concat(plan.errors[f]);
        }
        $('#plan-row-' + planId + ' .input-error')
            .show()
            .html(errors.join('<br>'))
    }
}

function editPlanSuccessFunc(plan) {
    return function (response) {
        plan.total = response.total;
        cancelPlanEdit(plan.id);
        $('#plan-row-' + plan.id)
            .html(plan.createPlanRow().html())
    }
}

function editPlanError(response, status, error) {
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

// ------------- CANCEL EDIT PLAN ----------------

function cancelPlanEdit(planId) {
    let oldData = $('#plan-' + planId + '-old-data>');
    $('#plan-row-' + planId)
        .removeClass('editing')
        .html(oldData.html());
    oldData.remove();
}

// ------------- DELETE PLAN ----------------

function deletePlan(planId) {
    let data = {
        csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val(),
        id: planId
    };
    $.ajax({
        url: '/plan/delete/',
        type: 'POST',
        dataType: 'json',
        data: data,
        success: deletePlanSuccessFunc(planId),
        error: deletePlanError,
    })
}

function deletePlanSuccessFunc(planId) {
    return function () {
        // remove plan row
        $('#plan-row-' + planId).remove();

        // if no row left, display empty box
        let planList = $('#plan-list');
        if (planList.find('.plan').length === 0) {
            $('<div class="row box">')
                .append($('<div class="no-data twelve columns">').text('No plan is set!'))
                .appendTo(planList)
        }
    }
}

function deletePlanError(response, status, error) {
    switch (error) {
        case 'Bad Request':
            alert('Invalid plan id');
            break;
        case 'Internal Server Error':
            alert("Internal Server Error\nPlease try again later");
            break;
        default :
            alert("Unknown error\nPlease try again later");
    }
}

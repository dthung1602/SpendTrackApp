/**
 * Set now to start date field
 */
function setNewPlanStartDateToday() {
    let d = new Date();
    let today = [d.getFullYear(), (d.getMonth() + 1).fillZero(), d.getDate().fillZero()].join('-');
    $('#plan-start-date').val(today);
}

/**
 * Clear all input fields in new entry form
 */
function clearNewPlanFields() {
    $('#new-plan [id^=plan]').val('');
    $('#category').val('empty');
    $('#category-display').html('Select a category');
    $('#new-plan .input-error').hide();
}

// ------------- SUBMIT FORM ----------------

/**
 * Return an object contains all submit data
 */
function getNewPlanData() {
    return {
        csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val(),
        name: $('#plan-name').val().trim(),
        start_date: $('#plan-start-date').val(),
        end_date: $('#plan-end-date').val(),
        category: $('#category').val(),
        compare: $('#plan-compare').val(),
        planned_total: $('#plan-planned-total').val()
    }
}

/**
 * Display errors when submitting the form
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
                if (response.responseJSON.hasOwnProperty(field)) {
                    let errors = response.responseJSON[field];
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
 * Create a function to call when new entry is added successfully
 * @param data: object contain submit data
 * @returns {Function} a function that update page content when a new entry is added successfully
 */
function addNewPlanSuccessFunc(data) {
    return function (response) {
        // get elements
        let categoryDisplay = $('#category-display');
        let now = new Date();
        let startDate = new Date(data.start_date);
        let endDate = new Date(data.end_date);

        // if plan do not start today, inform success
        if (now.toDateString() !== startDate.toDateString()) {
            $('#plan-add-success-panel').show().html('Plan "' + data.name + '" has been added.');

        } else { // if plan starts today, update current plans
            let currentPlansContainer = $('#current-plans');

            // clear 'no-data' div
            currentPlansContainer.find('.no-data').remove();

            // hide add success panel
            $('#plan-add-success-panel').hide();

            // format data
            data.start_date = startDate.toDateString().substr(4);
            data.end_date = endDate.toDateString().substr(4);
            data.target = getTarget(data);

            // add new plan container
            let planContainer = $('<div class="row plan">').appendTo(currentPlansContainer);

            // add data to plan container
            $('<div class="plan-name">').text(data.name).appendTo(planContainer);
            $('<div class="plan-date">').text(data.start_date).appendTo(planContainer);
            $('<div class="plan-date">').text(data.end_date).appendTo(planContainer);
            $('<div class="plan-target">').text(data.target).appendTo(planContainer);
            $('<div class="plan-total">').text("0").appendTo(planContainer);
        }

        // clear form
        clearNewPlanFields();
    }
}

/**
 * Validate form and display errors
 * @param data
 * @returns {boolean} whether form is valid
 */
function validateNewPlanForm(data) {
    let valid = true;
    $('#new-plan .input-error').hide();

    // validate start date and end date
    if (isNaN(Date.parse(data.start_date))) {
        valid = false;
        $('#plan-start-date-error').show().html('Invalid date');
    }
    if (isNaN(Date.parse(data.end_date))) {
        valid = false;
        $('#plan-end-date-error').show().html('Invalid date');
    }

    if (valid) {
        if (data.start_date > data.end_date) {
            valid = false;
            $('#plan-end-date-error').show().html('End date must come after start date');
        }
        let today = (new Date()).toISOString().substr(0, 10);
        if (data.start_date < today) {
            valid = false;
            $('#plan-start-date-error').show().html('Start date must not in the past');
        }
    }

    // content must not be empty
    if (data.name === "") {
        valid = false;
        $('#plan-name-error').show().html('Name cannot be empty');
    }

    // category must not be empty
    if (data.category === "empty") {
        valid = false;
        $('#plan-category-error').show().html('A category must be selected');
    }

    // compare must <, > or =
    if (['<', '>', '='].indexOf(data.compare) === -1) {
        valid = false;
        $('#plan-compare-error').show().html('Compare must be <, > or =');
    }

    // evaluate arithmetic expression in planned total field
    try {
        if (!data.planned_total.match(/^[0-9 +\-*/().]+$/))
            throw "";
        data.planned_total = eval(data.planned_total).toFixed(2);
    } catch (err) {
        valid = false;
        $('#plan-planned-total-error').show().html('Invalid arithmetic expression');
    }

    return valid;
}

/**
 *  Validate form, submit and handle result
 */
function submitNewPlanForm() {
    // get values to submit
    let data = getNewPlanData();

    // validate form
    if (!validateNewPlanForm(data)) return;

    // send ajax request
    $.ajax({
        url: '/plan/add/',
        type: 'POST',
        dataType: 'json',
        data: data,
        success: addNewPlanSuccessFunc(data),
        error: addNewPlanError,
    });
}

function getTarget(data) {
    let compare = {"<": "less than", ">": "greater than", "=": "equal to"}[data.compare];
    let categoryName = $('#category-display').text();
    return "Total in \"" + categoryName + "\" is " + compare + " " + data.planned_total;
}

function successFindPlanFunc(response) {
    // get elements
    let foundPlansContainer = $('#found-plan-container').html('').show();
    let plans = response.plans;

    // display found plans
    if (plans.length > 0) {
        for (let i = 0; i < plans.length; i++) {

            let plan = $('<div class="row plan">').appendTo(foundPlansContainer);
            let planInfo = $('<div class="four columns">').appendTo(plan);
            let planProgress = $('<div class="eight columns">').appendTo(plan);

            // Plan info
            $('<div class="plan-name">').text(plans[i].name).appendTo(planInfo);
            $('<div class="plan-date">').text(plans[i].start_date).appendTo(planInfo);
            $('<div class="plan-date">').text(plans[i].end_date).appendTo(planInfo);
            $('<div class="plan-target">').text(plans[i].target).appendTo(planInfo);
            $('<div class="plan-total">').text(plans[i].total).appendTo(planInfo);

            // TODO something with has_passed, completed

            // plan progress
            let progressBar = $('<div class="progress-bar-background">').appendTo(planProgress);
            $('<div class="progress-bar" id="progress-bar-' + (i + 1) + '">').appendTo(progressBar);
        }

        // TODO draw bars
        return
    }

    // nothing found
    foundPlansContainer.append(
        $('<div class="row">').append(
            $('<div class="no-data twelve columns">').text('No plan is found!')
        )
    );
}

function failFindPlanFunc(response, status, error) {
    let errorField = $('#search-input-error').show();
    switch (error) {
        case 'Bad Request':
            let errorContent = "";
            let keys = Object.keys(response.JSONresponse);
            for (let i = 0; i < keys.length; i++) {
                errorContent += keys[i] + ": " + response.JSONresponse[keys[i]].join('; ') + '<br>';
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

function submitSearchPlanForm(url) {
    submitSearchFormAJAX(
        url,
        successFindPlanFunc,
        failFindPlanFunc
    )
}
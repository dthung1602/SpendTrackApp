/**
 * Create a time bar and a progress bar for each plan in #plan-list
 */
function createPlansProgressBars() {
    let n = $('#plan-list').children().length;
    let today = new Date();

    for (let i = 0; i < n; i++) {

        // get plan info specified in #plan-list
        let startDate = new Date($('#plan-data-' + i + '-start-date').val());
        let endDate = new Date($('#plan-data-' + i + '-end-date').val());
        let total = parseInt($('#plan-data-' + i + '-total').val());
        let plannedTotal = parseInt($('#plan-data-' + i + '-planned-total').val());
        let compare = $('#plan-data-' + i + '-compare').val();

        // time bar
        let totalDays = daysBetween(startDate, endDate);
        let daysElapsed = daysBetween(startDate, today);
        let timeRatio = daysElapsed / totalDays * 100;
        new ProgressBar('#time-progress-' + i, timeRatio, {
            backgroundColor: '#296a84',
            foregroundColor: '#183f62',
            type: 'line'
        });

        // evaluate plan as good, warning or fail
        let planEvaluate = '';
        let planRatio = total / plannedTotal * 100;
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
                else if (total <= plannedTotal)
                    planEvaluate = 'warning';
                else
                    planEvaluate = 'fail';
                break;
            default:
                let ratio = planRatio / timeRatio;
                if (ratio < 0.9)
                    planEvaluate = 'warning';
                else if (ratio > 1.1) {
                    if (total > 1.1 * plannedTotal)
                        planEvaluate = 'fail';
                    else
                        planEvaluate = 'warning'
                } else
                    planEvaluate = 'good';
        }

        // set color to plan bar according to plan evaluation
        let backgroundColor = '';
        let foregroundColor = '';
        switch (planEvaluate) {
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

        // create plan bar
        new ProgressBar('#plan-progress-' + i, planRatio, {
            backgroundColor: backgroundColor,
            foregroundColor: foregroundColor,
            type: 'line'
        });
    }
}

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
        let now = new Date();
        let startDate = new Date(data.start_date);
        let endDate = new Date(data.end_date);

        // if plan do not start today, inform success
        if (now.toDateString() !== startDate.toDateString()) {
            $('#plan-add-success-panel').show().html('Plan "' + data.name + '" has been added.');

        } else { // if plan starts today, update current plans
            let currentPlansContainer = $('#plan-list');

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

function successSearchPlanFunc(response) {
    // get elements
    let foundPlansContainer = $('#plan-list').html('').show();
    let plans = response.plans;

    // display found plans
    if (plans.length > 0) {
        for (let i = 0; i < plans.length; i++) {

            let plan = $('<div class="row plan">').appendTo(foundPlansContainer);
            let planInfo = $('<div class="five columns">').appendTo(plan);
            let planProgress = $('<div class="seven columns">').appendTo(plan);

            // Plan info
            $('<div class="plan-name">').text(plans[i].name).appendTo(planInfo);
            let tableInfo = $('<tbody>').appendTo(
                $('<table>').appendTo(planInfo)
            );
            $('<tr>').appendTo(tableInfo).append(
                $('<td>').text('From')
            ).append(
                $('<td>').text(plans[i].start_date)
            );
            $('<tr>').appendTo(tableInfo).append(
                $('<td>').text('To')
            ).append(
                $('<td>').text(plans[i].end_date)
            );
            $('<tr>').appendTo(tableInfo).append(
                $('<td>').text('Target')
            ).append(
                $('<td>').text(plans[i].target)
            );
            $('<tr>').appendTo(tableInfo).append(
                $('<td>').text('Total')
            ).append(
                $('<td>').text(plans[i].total)
            );

            // plan hidden data
            $('<input type="hidden" id="plan-data-' + i + '-start-date">')
                .appendTo(planProgress).val(plans[i].start_date);
            $('<input type="hidden" id="plan-data-' + i + '-end-date">')
                .appendTo(planProgress).val(plans[i].end_date);
            $('<input type="hidden" id="plan-data-' + i + '-total">')
                .appendTo(planProgress).val(plans[i].total);
            $('<input type="hidden" id="plan-data-' + i + '-planned-total">')
                .appendTo(planProgress).val(plans[i].planned_total);
            $('<input type="hidden" id="plan-data-' + i + '-compare">')
                .appendTo(planProgress).val(plans[i].compare);

            // progress bars
            $('<div class="progress-bar-group">').appendTo(planProgress).append(
                $('<div id="time-progress-' + i + '">')
            ).append(
                $('<div id="plan-progress-' + i + '">')
            )
        }

        createPlansProgressBars();
        return
    }

    // nothing found
    foundPlansContainer.append(
        $('<div class="row box">').append(
            $('<div class="no-data twelve columns">').text('No plan is found!')
        )
    );
}

function failSearchPlanFunc(response, status, error) {
    let errorField = $('#search-input-error').show();
    switch (error) {
        case 'Bad Request':
            let errorContent = "";
            let keys = Object.keys(response.responseJSON);
            for (let i = 0; i < keys.length; i++) {
                errorContent += keys[i] + ": " + response.responseJSON[keys[i]].join('; ') + '<br>';
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
        successSearchPlanFunc,
        failSearchPlanFunc
    )
}


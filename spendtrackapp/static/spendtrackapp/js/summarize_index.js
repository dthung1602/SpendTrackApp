function selectSummarizeType() {
    let type = $('#summarize-type').val();
    $('.summarize-group').hide();
    $('#summarize-' + type).show();
}

function clearFields() {
    let fields = ['#year-year', '#month-year', '#month-month', '#week-year', '#week-week', '#start-date', '#end-date'];
    for (let i = 0; i < fields.length; i++)
        $(fields[i]).val('')
}
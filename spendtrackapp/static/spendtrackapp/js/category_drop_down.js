/**
 * Display select category drop down
 */
function showDropDown() {
    $("#select-category").toggleClass('show');
}

/**
 * Hide select category drop down when click outside
 */
function hideDropDown(event) {
    if (!event.target.matches('.clickable')) {
        let dropDowns = document.getElementsByClassName("select-content");
        for (let i = 0; i < dropDowns.length; i++) {
            let openDropDown = dropDowns[i];
            if (openDropDown.classList.contains('show')) {
                openDropDown.classList.remove('show');
            }
        }
    }
}

window.onclick = hideDropDown;

/**
 * Select a category
 * @param categoryId
 */
// TODO RENAME selectCategory
function select(categoryId) {
    $('#category').val(categoryId);
    let text = (categoryId === "") ? "All category" : $('#cat-' + categoryId).text();
    $('#category-display').text(text);
}

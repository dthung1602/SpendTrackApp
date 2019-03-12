class Category {
    constructor(id, name, pid) {
        this.id = id;
        this.name = name;
        this.pid = pid;
        this.children = [];
        this.parent = null;
        this.level = 1;
    }

    isLeaf() {
        return this.children.length === 0;
    }

    isRoot() {
        return this.pid === "None";
    }

    /**
     * Set descendants' levels according to this level
     */
    setDescendantsLevel() {
        for (let i = 0; i < this.children.length; i++) {
            let child = this.children[i];
            child.level = this.level + 1;
            child.setDescendantsLevel();
        }
    }

    /**
     * Get html elements represent the category hierarchy with this node as root
     * @param catFieldId: ID of the hidden category input field
     * @param allowNonLeaf: can non-leaf categories be selected
     * @returns {Array} an array of <div> objects
     */
    toHtml(catFieldId, allowNonLeaf = false) {
        let innerDiv = $('<div class="level-' + this.level + '" id="cat-' + this.id + '">')
            .text(this.name);
        let div = $('<div class="category">').append(innerDiv);
        if (this.isLeaf() || allowNonLeaf) {
            div.addClass('leaf');
            div.click(Category.generateSelectCategoryFunc(catFieldId, this));
        }
        let divs = [div];
        for (let i = 0; i < this.children.length; i++)
            divs = divs.concat(this.children[i].toHtml(catFieldId, allowNonLeaf));
        return divs;
    }

    /**
     * Get a category represent the null value
     * @returns {Category}
     */
    static nullCategoryOption() {
        return new Category('empty', 'Select a category', null);
    }

    /**
     * Get a category represent all categories
     * @returns {Category}
     */
    static allCategoryOption() {
        return new Category(null, 'All categories', null);
    }

    /**
     * Create the hierarchy from given categories
     * @param {Array<Category>} categoryArray
     * @returns {Array<Category>} roots categories in the hierarchy
     */
    static createHierarchy(categoryArray) {
        // map id -> cat
        let map = {};
        for (let i = 0; i < categoryArray.length; i++) {
            let cat = categoryArray[i];
            map[cat.id] = cat;
        }

        // set parent and children
        let roots = [];
        for (let i = 0; i < categoryArray.length; i++) {
            let cat = categoryArray[i];
            if (cat.isRoot()) {
                roots.push(cat);
            } else {
                let parent = map[cat.pid];
                if (parent !== undefined)
                    parent.children.push(cat);
                cat.parent = parent;
            }
        }

        // set level
        for (let i = 0; i < roots.length; i++)
            roots[i].setDescendantsLevel();

        return roots;
    }

    /**
     * Get category array from hidden input element in html file
     * @returns {Array}
     */
    static getCategoryHiddenData() {
        let cats = [];
        let n = categoryHiddenData.id.length;
        for (let i = 0; i < n; i++) {
            cats.push(new Category(
                categoryHiddenData.id[i],
                categoryHiddenData.name[i],
                categoryHiddenData.pid[i],
            ))
        }
        return cats;
    }

    /**
     * Create html elements represents category hierarchy
     * @param catFieldId: id of the hidden input field to store the selected category id value
     * @param enableAllCategoryOption: can user select all categories?
     * @param allowNonLeaf: can non-leaf categories be selected
     * @returns {Array}
     */
    static toHierarchyHtml(catFieldId, enableAllCategoryOption, allowNonLeaf = false) {
        let cats = this.getCategoryHiddenData();
        let roots = this.createHierarchy(cats);
        if (enableAllCategoryOption)
            roots.splice(0, 0, Category.allCategoryOption());
        let html = [];
        for (let i = 0; i < roots.length; i++)
            html = html.concat(roots[i].toHtml(catFieldId, allowNonLeaf));
        return html;
    }

    /**
     * Create a category select box
     * @param catFieldId
     * @param enableAllCategoryOption
     * @param allowNonLeaf: can non-leaf categories be selected
     * @returns {*|jQuery|*|*}
     */
    static toDropdownMenu(catFieldId, enableAllCategoryOption = true, allowNonLeaf = false) {
        return $('<div class="select">')
            .append('<input type="hidden" id="' + catFieldId + '" autocomplete="off">')
            .append($('<div class="select-btn clickable">')
                .click(Category.generateShowDropDownFunc(catFieldId))
                .append('<span class="clickable" id="display-' + catFieldId + '">')
                .append('<span class="clickable">&#x25BC</span>'))
            .append($('<div  class="select-content" id="select-' + catFieldId + '">')
                .append(Category.toHierarchyHtml(catFieldId, enableAllCategoryOption, allowNonLeaf)));
    }

    /**
     * Generate a function that displays the select category drop down
     */
    static generateShowDropDownFunc(catFieldId) {
        return function () {
            $('#select-' + catFieldId).toggleClass('show');
        }
    }

    /**
     * @param catFieldId
     * @param category
     */
    static generateSelectCategoryFunc(catFieldId, category) {
        return function () {
            $('#display-' + catFieldId).text(category.name);
            $('#' + catFieldId).val(category.id);
        }
    }


    /**
     * Clear the select category with the given id
     * @param catFieldId
     */
    static clearSelectCategoryField(catFieldId) {
        Category.generateSelectCategoryFunc(
            catFieldId,
            Category.nullCategoryOption()
        )();
    }
}


/**
 * Hide select category drop down when click outside
 */
window.onclick = function (event) {
    if (!event.target.matches('.clickable'))
        $(".select-content").removeClass('show');
};

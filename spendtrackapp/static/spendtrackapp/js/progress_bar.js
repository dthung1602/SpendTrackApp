/**
 * Simple progress bar using html, css and jQuery
 *
 * @param selector: a jQuery selector that points to the progress bar element
 * @param percent: a number indicate % of progress. Can be negative or over 100
 * @param options: an object contains progress bar options
 *
 * Available options:
 *      backgroundColor: color % not completed
 *      foregroundColor: color of % completed
 *      width:           css width value of the bar
 *      height:          css height value of the bar
 *      type:            display type of progress bar. Must be either "bar" or "line"
 *
 * If any option is missing, the default value is used
 */

function ProgressBar(selector, percent, options) {
    this.defaultOptions = {
        backgroundColor: 'lightgrey',
        foregroundColor: 'grey',
        width: '100%',
        height: '10px',
        type: 'line', // bar or line
    };
    this.getOptionValue = function (value) {
        return this.options[value] || this.defaultOptions[value];
    };

    percent = Math.max(0, percent);

    this.container = $(selector);
    this.options = options;
    this.percent = percent;

    this.container.addClass('progress-bar');
    this.background = $('<div class="progress-bar-background">').appendTo(this.container);
    this.foreground = $('<div class="progress-bar-foreground">').appendTo(this.background);
    this.overflow = $('<div class="progress-bar-foreground">').appendTo(this.foreground);
    this.label = $('<div class="progress-bar-label">').text(percent.toFixed(2) + '%').appendTo(this.container);

    // set color
    this.background.css('background-color', this.getOptionValue('backgroundColor'));
    this.foreground.css('background-color', this.getOptionValue('foregroundColor'));
    this.overflow.css('background-color', this.getOptionValue('foregroundColor'));

    // set height
    this.foreground.css('height', this.getOptionValue('height'));
    let h = this.foreground.height();
    this.overflow.css('height', h * 2);

    // set width
    this.container.css('width', this.getOptionValue('width'));
    let w = this.container.width();
    this.background.css('width', '100%');
    this.foreground.css('width', Math.max(0, Math.min(100, percent)) + "%");
    this.overflow.css('width', h * 2);

    // set type
    let type = this.getOptionValue('type');

    // line type
    if (type === 'line') {
        this.background.css('height', h / 3);

        this.background.css('border-radius', h / 6);
        this.foreground.css('border-radius', h / 2);
        this.overflow.css('border-radius', h);

        this.foreground.css('position', 'relative');
        this.foreground.css('top', h / 6 - h / 2);

        this.overflow.css('position', 'relative');
        this.overflow.css('top', -h / 2);

        if (this.percent < 0)
            this.overflow.css('left', -h / 2);
        else if (this.percent > 100)
            this.overflow.css('float', 'right');
        else
            this.overflow.css('display', 'none')
    } else if (type === 'bar') {
        this.background.css('height', h);
        this.overflow.css('display', 'none')
    } else {
        throw "Invalid option type";
    }
}

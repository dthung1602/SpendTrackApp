let barChartResponsiveOptions = [];

let barChartOptions = {
    height: 380,
    fullWidth: true,
    seriesBarDistance: 20,
    axisX: {
        showGrid: false,
    },
    axisY: {
        onlyInteger: true,
    }
};

let lineChartResponsiveOptions = [];

let lineChartOptions = {
    height: 380,
    showArea: true,
    axisX: {
        showGrid: false,
    },
    axisY: {
        onlyInteger: true,
    }
};

let pieChartResponsiveOptions = [
    ['screen and (min-width: 640px)', {
        chartPadding: 50,
        labelOffset: 100,
        labelDirection: 'explode'
    }],
    ['screen and (min-width: 1024px)', {
        labelOffset: 80,
        chartPadding: 30
    }]
];

let pieChartOptions = {
    height: 300,
    ignoreEmptyValues: true
};

/**
 * Render charts in summarize week page
 */
function renderCharts() {
    // sum for bar chart
    let lastWeekData = [lastWeekBarChartSeries[0]];
    let thisWeekData = [thisWeekBarChartSeries[0]];
    for (let i = 1; i < 7; i++) {
        lastWeekData[i] = lastWeekData[i - 1] + lastWeekBarChartSeries[i];
        thisWeekData[i] = thisWeekData[i - 1] + thisWeekBarChartSeries[i];
    }

    // bar chart 
    Chartist.Bar('#bar-chart', {
        labels: daysInWeekNamesM,
        series: [
            // lastWeekData,
            // thisWeekData
            lastWeekBarChartSeries,
            thisWeekBarChartSeries
        ]
    }, barChartOptions, barChartResponsiveOptions);

    // filter out non-leaf categories
    let lastWeekLeafCategoriesSeries = [];
    let thisWeekLeafCategoriesSeries = [];
    for (let i = 0; i < categoriesNames.length; i++) {
        if (isLeaf[i]) {
            lastWeekLeafCategoriesSeries.push(lastWeekPieChartSeries[i]);
            thisWeekLeafCategoriesSeries.push(thisWeekPieChartSeries[i]);
        }
    }

    // last week pie chart
    Chartist.Pie('#last-week-pie-chart', {
        labels: categoriesNames,
        series: lastWeekLeafCategoriesSeries
    }, pieChartOptions, pieChartResponsiveOptions);

    // this week pie chart
    Chartist.Pie('#this-week-pie-chart', {
        labels: categoriesNames,
        series: thisWeekLeafCategoriesSeries
    }, pieChartOptions, pieChartResponsiveOptions);
}
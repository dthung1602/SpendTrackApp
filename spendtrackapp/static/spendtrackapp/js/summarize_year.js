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
 * Render charts in summarize year page
 */
function renderCharts() {
    // bar chart 
    Chartist.Bar('#bar-chart', {
        labels: monthNamesAbr,
        series: [
            lastYearBarChartSeries,
            thisYearBarChartSeries
        ]
    }, barChartOptions, barChartResponsiveOptions);

    // filter out non-leaf categories
    let lastYearLeafCategoriesSeries = [];
    let thisYearLeafCategoriesSeries = [];
    for (let i = 0; i < categoriesNames.length; i++) {
        if (isLeaf[i]) {
            lastYearLeafCategoriesSeries.push(lastYearPieChartSeries[i]);
            thisYearLeafCategoriesSeries.push(thisYearPieChartSeries[i]);
        }
    }

    // last year pie chart
    Chartist.Pie('#last-year-pie-chart', {
        labels: categoriesNames,
        series: lastYearLeafCategoriesSeries
    }, pieChartOptions, pieChartResponsiveOptions);

    // this year pie chart
    Chartist.Pie('#this-year-pie-chart', {
        labels: categoriesNames,
        series: thisYearLeafCategoriesSeries
    }, pieChartOptions, pieChartResponsiveOptions);
}
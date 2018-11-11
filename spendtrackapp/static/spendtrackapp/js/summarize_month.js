let lineChartResponsiveOptions = [];

let lineChartOptions = {
    height: 380,
    fullWidth: true,
    showPoint: false,
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
 * Render charts in summarize month page
 */
function renderCharts() {
    // sum for line chart
    let lastMonthData = [lastMonthLineChartSeries[0]];
    let thisMonthData = [thisMonthLineChartSeries[0]];
    for (let i = 1; i < 32; i++) {
        lastMonthData[i] = lastMonthData[i - 1] + lastMonthLineChartSeries[i];
        thisMonthData[i] = thisMonthData[i - 1] + thisMonthLineChartSeries[i];
    }

    // line chart 
    Chartist.Line('#line-chart', {
        labels: range(1, 32),
        series: [
            lastMonthData,
            thisMonthData
        ]
    }, lineChartOptions, lineChartResponsiveOptions);

    // filter out non-leaf categories
    let lastMonthLeafCategoriesSeries = [];
    let thisMonthLeafCategoriesSeries = [];
    for (let i = 0; i < categoriesNames.length; i++) {
        if (isLeaf[i]) {
            lastMonthLeafCategoriesSeries.push(lastMonthPieChartSeries[i]);
            thisMonthLeafCategoriesSeries.push(thisMonthPieChartSeries[i]);
        }
    }

    // last month pie chart
    Chartist.Pie('#last-month-pie-chart', {
        labels: categoriesNames,
        series: lastMonthLeafCategoriesSeries
    }, pieChartOptions, pieChartResponsiveOptions);

    // this month pie chart
    Chartist.Pie('#this-month-pie-chart', {
        labels: categoriesNames,
        series: thisMonthLeafCategoriesSeries
    }, pieChartOptions, pieChartResponsiveOptions);
}
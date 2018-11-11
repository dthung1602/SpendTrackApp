let lineChartResponsiveOptions = [];

let lineChartOptions = {
    height: 380,
    showPoint: false,
    showArea: true,
    fullWidth: false,
    axisX: {
        // showGrid: false,
        labelInterpolationFnc: function (value, index) {
            if (index % Math.floor(lineChartSerries.length / 5) === 0)
                return value;
            return null;
        },
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
 * Render charts in daterange page
 */
function renderCharts() {
    // sum for line chart
    let lineChartData = [lineChartSerries[0]];
    let startDateMillisecond = Date.parse(startDate);
    let daterangeLength = (Date.parse(endDate) - startDateMillisecond) / 86400000;
    let labels = [startDate];
    for (let i = 1; i < daterangeLength; i++) {
        lineChartData[i] = lineChartData[i - 1] + lineChartSerries[i];
        let day = new Date(startDateMillisecond + i * 86400000);
        labels[i] = [day.getFullYear(), day.getMonth() + 1, day.getDate()].join('-')
    }

    // line chart 
    Chartist.Line('#line-chart', {
        labels: labels,
        series: [lineChartData]
    }, lineChartOptions, lineChartResponsiveOptions);

    // filter out non-leaf categories
    let pieChartData = [];
    for (let i = 0; i < categoriesNames.length; i++) {
        if (isLeaf[i])
            pieChartData.push(pieChartSerries[i]);
    }

    // last month pie chart
    Chartist.Pie('#pie-chart', {
        labels: categoriesNames,
        series: pieChartData
    }, pieChartOptions, pieChartResponsiveOptions);
}
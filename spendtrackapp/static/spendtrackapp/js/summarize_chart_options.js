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
function setHistoryChart(element_name, labels, pass_data, fail_data){
    var ctx = document.getElementById(element_name).getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                data: pass_data,
                label: "Pass",
                backgroundColor: '#1cc88a',
                backgroundHoverColor: '#19b37a',
                borderColor: '#1cc88a',
            },
            {
                data: fail_data,
                label: "Fail",
                backgroundColor: '#e74a3b',
                backgroundHoverColor: '#e32d1c',
                borderColor: '#e74a3b',
            }]
        },
        options: {
            maintainAspectRatio: false,
            layout: {
                padding: {
                    left: 10,
                    right: 25,
                    top: 25,
                    bottom: 0
                }
            },
            scales: {
                xAxes: [{
                    gridLines: {
                        display: false,
                        drawBorder: false
                    },
                    ticks: {
                        maxTicksLimit: 6
                    },
                    maxBarThickness: 25,
                }],
                yAxes: [{
                    ticks: {
                        min: 0,
                        maxTicksLimit: 5,
                        padding: 10,
                    },
                    gridLines: {
                        color: "rgb(234, 236, 244)",
                        zeroLineColor: "rgb(234, 236, 244)",
                        drawBorder: false,
                        borderDash: [2],
                        zeroLineBorderDash: [2]
                    }
                }],
            },
            legend: {
                display: false
            }
        }
    })
}

//Config
Chart.defaults.global.defaultFontSize = 14;
Chart.plugins.unregister(ChartDataLabels);
Chart.plugins.register({
  beforeDraw: function (chartInstance) {
    var ctx = chartInstance.chart.ctx;
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, chartInstance.chart.width, chartInstance.chart.height);
  }
});
Chart.Legend.prototype.afterFit = function () {
  this.height = this.height + 20;
};
// Chart.defaults.global.plugins.datalabels.display = function(ctx) {
//   return ctx.dataset.data[ctx.dataIndex] !== 0;
// }

// Chart 01
$.ajax({
  url: $("#chart01").attr("data-url"),
  dataType: 'json',
  success: function (data) {
    // Chart.plugins.unregister(ChartDataLabels);
    let configChart01 = {
      type: 'bar',
      data,
      plugins: [ChartDataLabels],
      options: {
        responsive: true,
        animation: {
          onComplete: doneChart01
        },
        scales: {
          yAxes: [{
            display: false
          }]
        }
      },
      zoom: {
        enabled: true
      }
    }
    let chart01 = new Chart($("#chart01"), configChart01);
    new Chart($("#chart01-popup"), configChart01);

    function doneChart01() {
      let url_base64 = chart01.toBase64Image();
      link_chart01.href = url_base64;
    }
  }
});

$('#expand-chart01').magnificPopup({
  items: [
    {
      src: '#chart01-popup',
      type: 'inline'
    }
  ],
  gallery: {
    enabled: true
  },
});

// Chart 02
$.ajax({
  url: $("#chart02").attr("data-url"),
  dataType: 'json',
  success: function (data) {
    let configChart02 = {
      type: 'bar',
      data,
      plugins: [ChartDataLabels],
      options: {
        responsive: true,
        animation: {
          onComplete: doneChart02
        },
        scales: {
          yAxes: [{
            display: false
          }]
        }
      },
      zoom: {
        enabled: true
      }
    }
    let chart02 = new Chart($("#chart02"), configChart02);
    new Chart($("#chart02-popup"), configChart02);

    function doneChart02() {
      let url_base64 = chart02.toBase64Image();
      link_chart02.href = url_base64;
    }
  }
});

$('#expand-chart02').magnificPopup({
  items: [
    {
      src: '#chart02-popup',
      type: 'inline'
    }
  ],
  gallery: {
    enabled: true
  },
});

// Chart 03
$.ajax({
  url: $("#chart03").attr("data-url"),
  dataType: 'json',
  success: function (data) {
    configChart03 = {
      type: 'polarArea',
      data,
      plugins: [ChartDataLabels],
      options: {
        legend: {
          position: 'top',
        },
        responsive: true,
        animation: {
          onComplete: doneChart03
        },
        scale: {
          display: false
          // ticks: {
          //   beginAtZero: true
          // }
        },
        tooltips: {
          enabled: true,
          // callbacks: {
          //   label: function (tooltipItem, data) {
          //     return data.datasets[tooltipItem.datasetIndex].label + ' : ' + data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
          //   }
          // }
        }
      }
    }

    let chart03 = new Chart($("#chart03"), configChart03);
    new Chart($("#chart03-popup"), configChart03);

    function doneChart03() {
      let url_base64 = chart03.toBase64Image();
      link_chart03.href = url_base64;
    }
  }
});

$('#expand-chart03').magnificPopup({
  items: [
    {
      src: '#chart03-popup', // CSS selector of an element on page that should be used as a popup
      type: 'inline'
    }
  ],
  gallery: {
    enabled: true
  },
});

// Chart 04
$.ajax({
  url: $("#chart04").attr("data-url"),
  dataType: 'json',
  success: function (data) {
    configChart04 = {
      type: 'polarArea',
      data,
      plugins: [ChartDataLabels],
      options: {
        legend: {
          position: 'top',
        },
        responsive: true,
        animation: {
          onComplete: doneChart04
        },
        scale: {
          display: false
          // ticks: {
          //   beginAtZero: true
          // }
        },
        tooltips: {
          enabled: true,
          // callbacks: {
          //   label: function (tooltipItem, data) {
          //     return data.datasets[tooltipItem.datasetIndex].label + ' : ' + data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
          //   }
          // }
        }
      }
    }

    let chart04 = new Chart($("#chart04"), configChart04);
    new Chart($("#chart04-popup"), configChart04);

    function doneChart04() {
      let url_base64 = chart04.toBase64Image();
      link_chart04.href = url_base64;
    }
  }
});

$('#expand-chart04').magnificPopup({
  items: [
    {
      src: '#chart04-popup', // CSS selector of an element on page that should be used as a popup
      type: 'inline'
    }
  ],
  gallery: {
    enabled: true
  },
});

// Chart 05
$.ajax({
  url: $("#chart05").attr("data-url"),
  dataType: 'json',
  success: function (data) {
    configChart05 = {
      type: 'line',
      data,
      plugins: [ChartDataLabels],
      options: {
        legend: {
          display: true,
          position: 'top',
        },
        responsive: true,
        showTooltips: false,
        animation: {
          onComplete: doneChart05
        },
        scales: {
          yAxes: [{
            display: false
          }]
        }
      }
    }

    let chart05 = new Chart($("#chart05"), configChart05);
    new Chart($("#chart05-popup"), configChart05);

    function doneChart05() {
      let url_base64 = chart05.toBase64Image();
      link_chart05.href = url_base64;
    }
  }
});

$('#expand-chart05').magnificPopup({
  items: [
    {
      src: '#chart05-popup', // CSS selector of an element on page that should be used as a popup
      type: 'inline'
    }
  ],
  gallery: {
    enabled: true
  },
});

// Chart 06
$.ajax({
  url: $("#chart06").attr("data-url"),
  dataType: 'json',
  success: function (data) {
    configChart06 = {
      type: 'line',
      data,
      plugins: [ChartDataLabels],
      options: {
        legend: {
          display: true,
          position: 'top',
        },
        responsive: true,
        showTooltips: false,
        animation: {
          onComplete: doneChart06
        },
        scales: {
          yAxes: [{
            display: false,
          }]
        },
        layout: {
          padding: {
            left: 0,
            right: 50,
            top: 0,
            bottom: 0
          }
        }
      }
    }

    let chart06 = new Chart($("#chart06"), configChart06);
    new Chart($("#chart06-popup"), configChart06);

    function doneChart06() {
      let url_base64 = chart06.toBase64Image();
      link_chart06.href = url_base64;
    }
  }
});

$('#expand-chart06').magnificPopup({
  items: [
    {
      src: '#chart06-popup', // CSS selector of an element on page that should be used as a popup
      type: 'inline'
    }
  ],
  gallery: {
    enabled: true
  },
});

// Chart 07
$.ajax({
  url: $("#chart07").attr("data-url"),
  dataType: 'json',
  success: function (data) {
    configChart07 = {
      type: 'horizontalBar',
      data,
      plugins: [ChartDataLabels],
      options: {
        legend: {
          display: false,
        },
        responsive: true,
        showTooltips: false,
        animation: {
          onComplete: doneChart07
        },
        scales: {
          xAxes: [{
            display: false
          }],
          yAxes: [{
            gridLines: {
              display: false
            }
          }]
        },
        layout: {
          padding: {
            left: 0,
            right: 35,
            top: 0,
            bottom: 0
          }
        }
      }
    }

    let chart07 = new Chart($("#chart07"), configChart07);
    new Chart($("#chart07-popup"), configChart07);

    function doneChart07() {
      let url_base64 = chart07.toBase64Image();
      link_chart07.href = url_base64;
    }
  }
});

$('#expand-chart07').magnificPopup({
  items: [
    {
      src: '#chart07-popup', // CSS selector of an element on page that should be used as a popup
      type: 'inline'
    }
  ],
  gallery: {
    enabled: true
  },
});

// Chart 08
$.ajax({
  url: $("#chart08").attr("data-url"),
  dataType: 'json',
  success: function (data) {
    configChart08 = {
      type: 'bar',
      data,
      plugins: [ChartDataLabels],
      options: {
        legend: {
          display: true,
        },
        responsive: true,
        showTooltips: false,
        animation: {
          onComplete: doneChart08
        },
        scales: {
          xAxes: [{
            gridLines: {
              display: false
            }
          }],
          yAxes: [{
            display: false
          }]
        },
        plugins: {
          datalabels: {
            display: function(context) {
              return context.dataset.data[context.dataIndex] !== 0;
            }
          }
        }
        // layout: {
        //   padding: {
        //     left: 0,
        //     right: 35,
        //     top: 0,
        //     bottom: 0
        //   }
        // }
      }
    }

    let chart08 = new Chart($("#chart08"), configChart08);
    new Chart($("#chart08-popup"), configChart08);

    function doneChart08() {
      let url_base64 = chart08.toBase64Image();
      link_chart08.href = url_base64;
    }
  }
});

$('#expand-chart08').magnificPopup({
  items: [
    {
      src: '#chart08-popup', // CSS selector of an element on page that should be used as a popup
      type: 'inline'
    }
  ],
  gallery: {
    enabled: true
  },
});

// Chart 09
$.ajax({
  url: $("#chart09").attr("data-url"),
  dataType: 'json',
  success: function (data) {
    // Chart.plugins.unregister(ChartDataLabels);
    let configChart09 = {
      type: 'bar',
      data,
      plugins: [ChartDataLabels],
      options: {
        responsive: true,
        animation: {
          onComplete: doneChart09
        },
        scales: {
          yAxes: [{
            display: false
          }]
        }
      },
      zoom: {
        enabled: true
      }
    }
    let chart09 = new Chart($("#chart09"), configChart09);
    new Chart($("#chart09-popup"), configChart09);

    function doneChart09() {
      let url_base64 = chart09.toBase64Image();
      link_chart09.href = url_base64;
    }
  }
});

$('#expand-chart09').magnificPopup({
  items: [
    {
      src: '#chart09-popup',
      type: 'inline'
    }
  ],
  gallery: {
    enabled: true
  },
});

// Chart 10
$.ajax({
  url: $("#chart10").attr("data-url"),
  dataType: 'json',
  success: function (data) {
    configChart10 = {
      type: 'bar',
      data,
      plugins: [ChartDataLabels],
      options: {
        legend: {
          display: true,
        },
        responsive: true,
        showTooltips: false,
        animation: {
          onComplete: doneChart10
        },
        scales: {
          xAxes: [{
            gridLines: {
              display: false
            }
          }],
          yAxes: [{
            display: false
          }]
        },
        plugins: {
          datalabels: {
            display: function(context) {
              return context.dataset.data[context.dataIndex] !== 0;
            }
          }
        }
      }
    }

    let chart10 = new Chart($("#chart10"), configChart10);
    new Chart($("#chart10-popup"), configChart10);

    function doneChart10() {
      let url_base64 = chart10.toBase64Image();
      link_chart10.href = url_base64;
    }
  }
});

$('#expand-chart10').magnificPopup({
  items: [
    {
      src: '#chart10-popup', // CSS selector of an element on page that should be used as a popup
      type: 'inline'
    }
  ],
  gallery: {
    enabled: true
  },
});
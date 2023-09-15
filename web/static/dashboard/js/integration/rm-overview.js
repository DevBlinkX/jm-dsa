$(document).ready(function () {
  var days = 90;
  function topCards(days) {
    $(".card-loader").css("visibility", "visible");
    $.ajax({
      type: "GET",
      url: "/api/rm/overview/?days=" + days,
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization: "Bearer " + localStorage.getItem("access-token"),
      },
      dataType: "json",
      success: function (response) {
        $("[data-total-leads]").empty();
        $("[data-account-opened]").empty();
        $("[data-trading-client]").empty();
        $("[data-revenue-earned]").empty();
        $("[data-pending-leads]").empty();
        if (response.success == true) {
          $(".card-loader").css("visibility", "hidden");
          // $("[data-completed], [data-employee-count], [data-pending], [data-total]").empty();
          var total_leads_added = response.data.total_leads_added;
          var total_account_opened = response.data.total_account_opened;
          var total_trading_client = response.data.activation_percentage;
          var net_revenue_earned = response.data.pending_leads;
          var pending_leads = response.data.total_app_download;

          $("[data-total-leads]").append(total_leads_added);
          $("[data-account-opened]").append(total_account_opened);
          $("[data-trading-client]").append(total_trading_client);
          $("[data-revenue-earned]").append(net_revenue_earned);
          $("[data-pending-leads]").append(pending_leads);
        }
      },
      error: function (error) {
        // var error_data = JSON.parse(error.responseText);
        $(".card-loader").css("visibility", "hidden");
      },
    });
  }

  // getLeadChart
  function getLeadChart(days) {
    $(".card-loader").css("visibility", "visible");
    $.ajax({
      type: "GET",
      url: "/api/rm/overview/leads/?days=" + days,
      dataType: "json",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization: "Bearer " + localStorage.getItem("access-token"),
      },
      success: function (response) {
        if (response.success == true) {
          // console.log("response", response.data);
          var monthList = [];
          var addedCount = [];
          var activatedCount = [];
          if (response.data.isEmpty == true) {
            $("#leadChart").remove();
            $("[no-lead-data]").empty();
            $("[no-lead-data]").append(
              `<div data-empty-category class="card w-100 mt-0"><p class="h6 text-center py-5">No Data Available</p></div>`
            );
          } else {
            $.each(response, function () {
              $.each(this, function (k, v) {
                monthList.push(v.month);
                addedCount.push(v.data.added);
                activatedCount.push(v.data.activated);
              });
            });
            $("#leadChart").remove(); // this is my <canvas> element
            $("#leadChartArea").append('<canvas id="leadChart"><canvas>');
            // chart
            var ctx = document.getElementById("leadChart");
            var myLineChart = new Chart(ctx, {
              type: "line",
              data: {
                labels: monthList,
                datasets: [
                  {
                    label: "Added",
                    lineTension: 0.3,
                    backgroundColor: "rgba(250, 116, 21,.1)",
                    borderColor: "rgba(250, 116, 21,1)",
                    pointRadius: 0,
                    pointBackgroundColor: "rgba(250, 116, 21,1)",
                    pointBorderColor: "rgba(250, 116, 21,1)",
                    pointHoverRadius: 0,
                    pointHoverBackgroundColor: "rgba(250, 116, 21,1)",
                    pointHoverBorderColor: "rgba(250, 116, 21,1)",
                    pointHitRadius: 10,
                    pointBorderWidth: 2,
                    fill: true,
                    data: addedCount,
                  },
                  {
                    label: "Activated",
                    lineTension: 0.3,
                    backgroundColor: "#D946EF",
                    borderColor: "#D946EF",
                    pointRadius: 0,
                    pointBackgroundColor: "#D946EF",
                    pointBorderColor: "#D946EF",
                    pointHoverRadius: 0,
                    pointHoverBackgroundColor: "#D946EF",
                    pointHoverBorderColor: "#D946EF",
                    pointHitRadius: 10,
                    pointBorderWidth: 2,
                    data: activatedCount,
                  },
                ],
              },
              options: {
                plugins: {
                  legend: {
                    display: false,
                  },
                },
                maintainAspectRatio: false,
                layout: {
                  padding: {
                    left: 10,
                    right: 25,
                    top: 25,
                    bottom: 0,
                  },
                },
                scales: {
                  x: {
                    time: {
                      unit: "date",
                    },
                    grid: {
                      color: "#ededed",
                      // zeroLineColor: "#fff",
                      // drawBorder: false,
                      borderDash: [8, 4],
                      // zeroLineBorderDash: [5],
                    },
                    ticks: {
                      maxTicksLimit: 12,
                    },
                  },
                  y: {
                    ticks: {
                      maxTicksLimit: 5,
                      padding: 10,
                      // Include a dollar sign in the ticks
                      callback: function (value, index, values) {
                        return "" + number_format(value);
                      },
                    },
                    grid: {
                      color: "#ededed",
                      // zeroLineColor: "#fff",
                      // drawBorder: false,
                      borderDash: [8, 4],
                      // zeroLineBorderDash: [5],
                    },
                  },
                },

                tooltips: {
                  backgroundColor: "rgb(255,255,255)",
                  bodyFontColor: "#858796",
                  titleMarginBottom: 10,
                  titleFontColor: "#6e707e",
                  titleFontSize: 14,
                  borderColor: "#dddfeb",
                  borderWidth: 1,
                  xPadding: 15,
                  yPadding: 15,
                  displayColors: false,
                  intersect: false,
                  mode: "index",
                  caretPadding: 10,
                  callbacks: {
                    label: function (tooltipItem, chart) {
                      var datasetLabel =
                        chart.datasets[tooltipItem.datasetIndex].label || "";
                      return (
                        datasetLabel + ": " + number_format(tooltipItem.yLabel)
                      );
                    },
                  },
                },
              },
            });
          }

          $(".card-loader").css("visibility", "hidden");
        }
      },
      error: function (error) {
        // var error_data = JSON.parse(error.responseText);
        $(".card-loader").css("visibility", "hidden");
      },
    });
  }

  // brokerage chart example
  function getbrokerageChart(days) {
    $(".card-loader").css("visibility", "visible");
    $.ajax({
      type: "GET",
      url: "/api/rm/overview/brokerage/?days=" + days,
      dataType: "json",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization: "Bearer " + localStorage.getItem("access-token"),
      },
      success: function (response) {
        if (response.success == true) {
          var monthList = [];
          var getCount = [];

          if (jQuery.isEmptyObject(response.data) == true) {
            $("#brokerageChart").remove();
            $("[no-brokerage-data]").empty();
            $("[no-brokerage-data]").append(
              `<div data-empty-category class="card w-100 mt-0"><p class="h6 text-center py-5">No Data Available</p></div>`
            );
          } else {
            $.each(response, function () {
              $.each(this, function (k, v) {
                // console.log("response", response);
                monthList.push(k);
                getCount.push(v);
              });
            });
            $("#brokerageChart").remove(); // this is my <canvas> element
            $("#brokerageChartArea").append(
              '<canvas id="brokerageChart"><canvas>'
            );
            // chart
            var ctx = document.getElementById("brokerageChart");
            var myLineChart = new Chart(ctx, {
              type: "bar",
              data: {
                labels: monthList,
                datasets: [
                  {
                    label: "Brokerage",
                    lineTension: 0.3,
                    backgroundColor: "#FA7415",
                    borderColor: "#FA7415",
                    pointRadius: 3,
                    pointBackgroundColor: "#FA7415",
                    pointBorderColor: "#FA7415",
                    pointHoverRadius: 3,
                    pointHoverBackgroundColor: "#FA7415",
                    hoverBackgroundColor: "#FA7415",
                    pointHoverBorderColor: "#FA7415",
                    pointHitRadius: 10,
                    pointBorderWidth: 2,
                    data: getCount,
                    barThickness: 40,
                  },
                ],
              },
              options: {
                maintainAspectRatio: false,
                borderRadius: 10,
                layout: {
                  padding: {
                    left: 10,
                    right: 25,
                    top: 25,
                    bottom: 0,
                  },
                },
                scales: {
                  x: {
                    time: {
                      unit: "date",
                    },
                    grid: {
                      color: "#ededed",
                      // zeroLineColor: "#fff",
                      // drawBorder: false,
                      borderDash: [8, 4],
                      // zeroLineBorderDash: [5],
                    },
                    ticks: {
                      maxTicksLimit: 7,
                    },
                  },
                  y: {
                    ticks: {
                      maxTicksLimit: 5,
                      padding: 10,
                      // Include a dollar sign in the ticks
                      callback: function (value, index, values) {
                        return "" + number_format(value);
                      },
                    },
                    grid: {
                      color: "#ededed",
                      // zeroLineColor: "#fff",
                      // drawBorder: false,
                      borderDash: [8, 4],
                      // zeroLineBorderDash: [5],
                    },
                  },
                },
                plugins: {
                  legend: {
                    display: false,
                  },
                },
                tooltips: {
                  backgroundColor: "rgb(255,255,255)",
                  bodyFontColor: "#858796",
                  titleMarginBottom: 10,
                  titleFontColor: "#6e707e",
                  titleFontSize: 14,
                  borderColor: "#dddfeb",
                  borderWidth: 1,
                  xPadding: 15,
                  yPadding: 15,
                  displayColors: false,
                  intersect: false,
                  mode: "index",
                  caretPadding: 10,
                  callbacks: {
                    label: function (tooltipItem, chart) {
                      var datasetLabel =
                        chart.datasets[tooltipItem.datasetIndex].label || "";
                      return (
                        datasetLabel + ": " + number_format(tooltipItem.yLabel)
                      );
                    },
                  },
                },
              },
            });
          }

          $(".card-loader").css("visibility", "hidden");
        }
      },
      error: function (error) {
        // var error_data = JSON.parse(error.responseText);
        $(".card-loader").css("visibility", "hidden");
      },
    });
  }

  // incentive chart example
  function getincentiveChart(days) {
    $(".card-loader").css("visibility", "visible");
    $.ajax({
      type: "GET",
      url: "/api/rm/overview/incentive/?days=" + days,
      dataType: "json",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization: "Bearer " + localStorage.getItem("access-token"),
      },
      success: function (response) {
        $(".card-loader").css("visibility", "hidden");
        if (response.success == true) {
          var weekList = [];
          var getCounts = [];

          if (jQuery.isEmptyObject(response.data) == true) {
            $("#incentiveChart").remove();
            $("[no-incentive-data]").empty();
            $("[no-incentive-data]").append(
              `<div data-empty-category class="card w-100 mt-0"><p class="h6 text-center py-5">No Data Available</p></div>`
            );
          } else {
            $.each(response, function () {
              $.each(this, function (k, v) {
                weekList.push(k);
                getCounts.push(v);
              });
            });
            $("#incentiveChart").remove();
            $("#incentiveChartArea").append(
              '<canvas id="incentiveChart"><canvas>'
            );
            // chart
            var ctx = document.getElementById("incentiveChart");
            var myLineChart = new Chart(ctx, {
              type: "bar",
              data: {
                labels: weekList,
                datasets: [
                  {
                    label: "Incentive",
                    lineTension: 0.3,
                    backgroundColor: "#D946EF",
                    borderColor: "#D946EF",
                    pointRadius: 3,
                    pointBackgroundColor: "#D946EF",
                    pointBorderColor: "#D946EF",
                    pointHoverRadius: 3,
                    pointHoverBackgroundColor: "#D946EF",
                    pointHoverBorderColor: "#D946EF",
                    pointHitRadius: 10,
                    pointBorderWidth: 1,
                    barThickness: 20,
                    data: getCounts,
                  },
                  // {
                  //   label: "Incentive",
                  //   lineTension: 0.3,
                  //   backgroundColor: "#a24cdb",
                  //   borderColor: "#aa29d44b",
                  //   pointRadius: 3,
                  //   pointBackgroundColor: "#aa29d44b",
                  //   pointBorderColor: "#aa29d44b",
                  //   pointHoverRadius: 3,
                  //   pointHoverBackgroundColor: "#aa29d44b",
                  //   pointHoverBorderColor: "#aa29d44b",
                  //   pointHitRadius: 10,
                  //   pointBorderWidth: 1,
                  //   data: getCounts,
                  // },
                ],
              },
              options: {
                maintainAspectRatio: false,
                borderRadius: 5,
                layout: {
                  padding: {
                    left: 10,
                    right: 25,
                    top: 25,
                    bottom: 0,
                  },
                },
                scales: {
                  x: {
                    time: {
                      unit: "date",
                    },
                    grid: {
                      color: "#ededed",
                      // zeroLineColor: "#fff",
                      // drawBorder: false,
                      borderDash: [8, 4],
                      // zeroLineBorderDash: [5],
                    },
                    ticks: {
                      maxTicksLimit: 13,
                    },
                  },
                  y: {
                    ticks: {
                      maxTicksLimit: 5,
                      padding: 10,
                      // Include a dollar sign in the ticks
                      callback: function (value, index, values) {
                        return "" + number_format(value);
                      },
                    },
                    grid: {
                      color: "#ededed",
                      // zeroLineColor: "#fff",
                      // drawBorder: false,
                      borderDash: [8, 4],
                      // zeroLineBorderDash: [5],
                    },
                  },
                },
                plugins: {
                  legend: {
                    display: false,
                  },
                },
                tooltips: {
                  backgroundColor: "rgb(255,255,255)",
                  bodyFontColor: "#858796",
                  titleMarginBottom: 10,
                  titleFontColor: "#6e707e",
                  titleFontSize: 14,
                  borderColor: "#dddfeb",
                  borderWidth: 1,
                  xPadding: 15,
                  yPadding: 15,
                  displayColors: false,
                  intersect: false,
                  mode: "index",
                  caretPadding: 10,
                  callbacks: {
                    label: function (tooltipItem, chart) {
                      var datasetLabel =
                        chart.datasets[tooltipItem.datasetIndex].label || "";
                      return (
                        datasetLabel + ": " + number_format(tooltipItem.yLabel)
                      );
                    },
                  },
                },
              },
            });
          }
        }
      },
      error: function (error) {
        // var error_data = JSON.parse(error.responseText);
        $(".card-loader").css("visibility", "hidden");
      },
    });
  }

  // conversion pie example
  function getconversionChart(days) {
    $.ajax({
      type: "GET",
      url: "/api/rm/overview/conversion/?days=" + days,
      dataType: "json",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization: "Bearer " + localStorage.getItem("access-token"),
      },
      success: function (response) {
        $("[data-conversion-1]").empty();
        $("[data-conversion-2]").empty();
        $("[data-conversion-3]").empty();

        if (response.success == true) {
          var socialList = [];
          var getCounts = [];

          $.each(response.data, function (k, v) {
            socialList.push(v.source_medium);
            getCounts.push(v.percentage);
          });
          if (socialList.length == 0) {
            $("#conversionChart").remove();
            $("[no-data]").empty();
            $("[no-data]").append(
              `<div data-empty-category class="card w-100 mt-4"><p class="h6 text-center py-5">No Data Available</p></div>`
            );
          } else {
            for (var i = 0; i < socialList.length; i++) {
              $(`[data-conversion-${i + 1}]`).append(`
              <div> <i class="fas fa-circle graph-color-${i + 1}"></i> 
                ${socialList[i]} 
                </div><div class="text-black">
                ${getCounts[i]} %</div>
            `);
            }
            $("#conversionChart").remove(); // this is my <canvas> element
            $("#conversionChartArea").append(
              '<canvas id="conversionChart"><canvas>'
            );

            // chart
            var ctx = document.getElementById("conversionChart");
            var myPieChart = new Chart(ctx, {
              type: "doughnut",
              data: {
                labels: socialList,
                datasets: [
                  {
                    data: getCounts,
                    backgroundColor: ["#FFBC78", "#FB913D", "#FA7415"],
                    hoverBackgroundColor: ["#FFBC78", "#FB913D", "#FA7415"],
                    hoverBorderColor: "rgba(234, 236, 244, 1)",
                  },
                ],
              },
              options: {
                plugin_one: true,
                responsive: true,
                maintainAspectRatio: false,
                // aspectRatio: 2,
                tooltips: {
                  backgroundColor: "rgb(255,255,255)",
                  bodyFontColor: "#858796",
                  borderColor: "#dddfeb",
                  borderWidth: 1,
                  xPadding: 15,
                  yPadding: 15,
                  displayColors: false,
                  caretPadding: 10,
                },
                plugins: {
                  legend: {
                    display: false,
                  },
                },
                cutoutPercentage: 60,
              },
            });
          }
        }
      },
    });
  }

  // conversion pie example
  function getconversionstageChart(days) {
    $.ajax({
      type: "GET",
      url: "/api/rm/overview/conversion-stage/?days=" + days,
      dataType: "json",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization: "Bearer " + localStorage.getItem("access-token"),
      },
      success: function (response) {
        $("[data-conversion-stage-1]").empty();
        $("[data-conversion-stage-2]").empty();
        $("[data-conversion-stage-3]").empty();
        $("[data-conversion-stage-4]").empty();
        if (response.success == true) {
          var socialList = [];
          var getCounts = [];
          $.each(response.data, function (k, v) {
            socialList.push(v.mx_diy_stage);
            getCounts.push(v.percentage);
          });
          if (socialList.length == 0) {
            $("#convrsionstageChart").remove();
            $("[no-stage-data]").empty();
            $("[no-stage-data]").append(
              `<div data-empty-category class="card w-100 mt-4"><p class="h6 text-center py-5">No Data Available</p></div>`
            );
          } else {
            for (var i = 0; i < socialList.length; i++) {
              $(`[data-conversion-stage-${i + 1}]`).append(`
              <div> <i class="fas fa-circle graph-color-p${i + 1}"></i> 
                ${socialList[i]} 
                </div><div class="text-black">
                ${getCounts[i]} %</div>
            `);
            }
            $("#convrsionstageChart").remove(); // this is my <canvas> element
            $("#convrsionstageChartArea").append(
              '<canvas id="convrsionstageChart"><canvas>'
            );
            // chart
            var ctx = document.getElementById("convrsionstageChart");
            var myPieChart = new Chart(ctx, {
              type: "pie",
              data: {
                labels: socialList,
                datasets: [
                  {
                    data: getCounts,
                    backgroundColor: [
                      "#D946EF",
                      "#F1ACFD",
                      "#F5D0FC",
                      "#E978FC",
                    ],
                    hoverBackgroundColor: [
                      "#D946EF",
                      "#F1ACFD",
                      "#F5D0FC",
                      "#E978FC",
                    ],
                    hoverBorderColor: "rgba(234, 236, 244, 1)",
                  },
                ],
              },
              options: {
                responsive: true,
                maintainAspectRatio: false,
                // aspectRatio: 1,
                tooltips: {
                  backgroundColor: "rgb(255,255,255)",
                  bodyFontColor: "#858796",
                  borderColor: "#dddfeb",
                  borderWidth: 1,
                  xPadding: 15,
                  yPadding: 15,
                  displayColors: false,
                  caretPadding: 10,
                },

                // cutoutPercentage: 80,
                plugins: {
                  datalabels: {
                    formatter: (value, ctx) => {
                      let sum = 0;
                      let dataArr = ctx.chart.data.datasets[0].data;
                      dataArr.map((data) => {
                        sum += data;
                      });
                      let percentage = ((value * 100) / sum).toFixed(2) + "%";
                      return percentage;
                    },
                  },

                  legend: {
                    display: false,
                  },
                },
              },
            });
          }
        }
      },
    });
  }

  // conversion pie example
  function getdownloadChart(days) {
    $(".card-loader").css("visibility", "visible");
    $.ajax({
      type: "GET",
      url: "/api/rm/overview/app-downloads/?days=" + days,
      dataType: "json",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization: "Bearer " + localStorage.getItem("access-token"),
      },
      success: function (response) {
        $(".card-loader").css("visibility", "hidden");
        $("[data-download-1]").empty();
        $("[data-download-2]").empty();
        $("[data-download-3]").empty();

        if (response.success == true) {
          var socialList = [];
          var getCounts = [];

          $.each(response.data, function (k, v) {
            socialList.push(k);
            getCounts.push(v);
          });
          if (socialList.length == 0) {
            $("#downloadChart").remove();
            $("[no-download-data]").empty();
            $("[no-download-data]").append(
              `<div data-empty-category class="card w-100 mt-4"><p class="h6 text-center py-5">No Data Available</p></div>`
            );
          } else {
            for (var i = 0; i < socialList.length; i++) {
              $(`[data-download-${i + 1}]`).append(`
              <div> <i class="fas fa-circle graph-color-${i + 1}"></i>
                ${socialList[i]}
                </div><div class="text-black">
                ${getCounts[i]} %</div>
            `);
            }
            $("#downloadChart").remove(); // this is my <canvas> element
            $("#downloadChartArea").append(
              '<canvas id="downloadChart"><canvas>'
            );

            // chart
            var ctx = document.getElementById("downloadChart");
            var myPieChart = new Chart(ctx, {
              type: "doughnut",
              data: {
                labels: socialList,
                hoverOffset: 4,
                datasets: [
                  {
                    data: getCounts,
                    backgroundColor: ["#FA7415", "#D946EF"],
                    hoverBackgroundColor: ["#FA7415", "#D946EF"],
                    hoverBorderColor: "rgba(234, 236, 244, 1)",
                  },
                ],
              },
              options: {
                plugin_one: true,
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                  animateRotate: true,
                },
                // aspectRatio: 2,
                tooltips: {
                  backgroundColor: "rgb(255,255,255)",
                  bodyFontColor: "#858796",
                  borderColor: "#dddfeb",
                  borderWidth: 1,
                  xPadding: 15,
                  yPadding: 15,
                  displayColors: false,
                  caretPadding: 10,
                },
                plugins: {
                  legend: {
                    display: false,
                  },
                },
                cutoutPercentage: 60,
              },
            });
          }
        }
      },
      error: function (error) {
        // var error_data = JSON.parse(error.responseText);
        $(".card-loader").css("visibility", "hidden");
      },
    });
  }

  // function bannerOverview() {
  //   $(".card-loader").css("visibility", "hidden");
  //   $.ajax({
  //     type: "GET",
  //     url: "/api/rm/overview/banner/",
  //     headers: {
  //       "Content-Type": "application/x-www-form-urlencoded",
  //       Authorization: "Bearer " + localStorage.getItem("access-token"),
  //     },
  //     dataType: "json",
  //     success: function (response) {
  //       if (jQuery.isEmptyObject(response.data)) {
  //         $("[data-banner-list]").append("");
  //       } else {
  //         $.each(response, function (k, v) {
  //           $("[data-banner-list]").append(`<div class="item">
  //                           <div class="cta d-flex align-items-center" style="background: url('${response.data.image}') no-repeat;background-size: cover">
  //                               <div class="content w-100">
  //                                   <p class="h4 text-white font-weight-500">${response.data.title}</p>
  //                                   <p class="text-white mb-0">${response.data.short_description} </p>
  //                               </div>
  //                               <div class="button">
  //                                   <a href="${response.data.link}" target="_blank" class="btn btn-cta">Click To New Offer
  //                                       <svg class="arrow ml-3" width="25" height="14" viewBox="0 0 25 14" fill="none"
  //                                           xmlns="http://www.w3.org/2000/svg">
  //                                           <path
  //                                               d="M9.44053 6.78463H23.6326L17.6115 0.847565C17.5695 0.806185 17.5695 0.73924 17.6115 0.69786C17.6534 0.65648 17.7214 0.65648 17.7633 0.69786L23.9686 6.81426C23.9888 6.83417 24.0002 6.86087 24.0002 6.88911C24.0002 6.91722 23.9888 6.94405 23.9686 6.96396L17.7633 13.0804C17.7214 13.1217 17.6534 13.1216 17.6115 13.0802C17.5695 13.039 17.5695 12.9719 17.6115 12.9305L23.6326 6.99562H9.44053C9.38135 6.99562 9.3335 6.94831 9.3335 6.89012C9.3335 6.83193 9.38135 6.78463 9.44053 6.78463Z"
  //                                               fill="#EC590C" stroke="#EC590C" />
  //                                           <circle cx="0.66667" cy="7.11149" r="0.66667" fill="#EC590C" />
  //                                           <circle cx="3.77751" cy="7.11149" r="0.66667" fill="#EC590C" />
  //                                           <circle cx="6.88884" cy="7.11149" r="0.66667" fill="#EC590C" />
  //                                       </svg>
  //                                   </a>
  //                               </div>
  //                           </div>
  //                       </div>`);
  //         });
  //       }

  //       $(".ad-carousel").owlCarousel({
  //         loop: true,
  //         margin: 10,
  //         nav: false,
  //         dots: false,
  //         responsive: {
  //           0: {
  //             items: 1,
  //           },
  //           600: {
  //             items: 1,
  //           },
  //           1000: {
  //             items: 1,
  //           },
  //         },
  //       });
  //       $(".card-loader").css("visibility", "hidden");
  //     },
  //   });
  // }

  topCards(days);
  getLeadChart(days);
  getbrokerageChart(days);
  getincentiveChart(days);
  // getconversionChart(days);
  // getconversionstageChart(days);
  getdownloadChart(days);
  // bannerOverview();

  $(".custom-select").on("change", function () {
    days = this.value;

    topCards(days);
    getLeadChart(days);
    getbrokerageChart(days);
    getincentiveChart(days);
    // getconversionChart(days);
    // getconversionstageChart(days);
    getdownloadChart(days);
  });
});

$(document).ready(function () {
  var days = 90;
  function kycTable(days) {
    $(".main-loader").show();
    $.ajax({
      type: "GET",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization: "Bearer " + localStorage.getItem("access-token"),
      },
      url: "/api/rm/overview/kyc-list/?days=" + days,
      dataType: "json",
      success: function (response) {
        $("[data-kyc-list]").empty();
        let x = 1;
        $.each(response, function (k, v) {
          var name = v.name;
          var kyc = v.kyc;
          var level = x++;
          $("[data-kyc-list]").append(
            "<tr><td><span class='count'>" +
              level +
              "</span></td><td>" +
              kyc +
              "</td><td>" +
              name +
              "</td></tr>"
          );
        });

        $(".main-loader").hide();
      },
      error: function (error) {
        // var error_data = JSON.parse(error.responseText);
        $(".main-loader").hide();
      },
    });
  }
  function brokerTable(days) {
    $(".main-loader").show();
    $.ajax({
      type: "GET",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization: "Bearer " + localStorage.getItem("access-token"),
      },
      url: "/api/rm/overview/broker-list/?days=" + days,
      dataType: "json",
      success: function (response) {
        $("[data-broker-list]").empty();
        let x = 1;
        $.each(response, function (k, v) {
          var name = v.name;
          var brokerage = v.brokerage;
          var level = x++;
          $("[data-broker-list]").append(
            "<tr><td><span class='count'>" +
              level +
              "</span></td><td>" +
              brokerage +
              "</td><td>" +
              name +
              "</td></tr>"
          );
        });

        $(".main-loader").hide();
      },
      error: function (error) {
        // var error_data = JSON.parse(error.responseText);
        $(".main-loader").hide();
      },
    });
  }
  function referralTable(days) {
    $(".main-loader").show();
    $.ajax({
      type: "GET",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization: "Bearer " + localStorage.getItem("access-token"),
      },
      url: "/api/rm/overview/referrals/?days=" + days,
      dataType: "json",
      success: function (response) {
        $("[data-refer-list]").empty();
        let x = 1;
        $.each(response, function (k, v) {
          var name = v.name;
          var kyc = v.kyc;
          var level = x++;
          $("[data-refer-list]").append(
            "<tr><td><span class='count'>" +
              level +
              "</span></td><td>" +
              kyc +
              "</td><td>" +
              name +
              "</td></tr>"
          );
        });

        $(".main-loader").hide();
      },
      error: function (error) {
        // var error_data = JSON.parse(error.responseText);
        $(".main-loader").hide();
      },
    });
  }
  kycTable(days);
  brokerTable(days);
  referralTable(days);

  $(".days-select").on("change", function () {
    days = this.value;

    kycTable(days);
    brokerTable(days);
    referralTable(days);
  });
});

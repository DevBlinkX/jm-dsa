$(document).ready(function () {

  function getTotalMandatesR(start, end) {
    $(".main-loader").show();
    $.ajax({
      type: "GET",
      url:"/api/rmj/overview/total-lead/?to_date=" +end +"&from_date=" +start,
      dataType: "json",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization: "Bearer " + localStorage.getItem("access-token"),
      },
      success: function (response) {
        $(".main-loader").hide();
        $("[data-referral-1]").empty();
        $("[data-referral-2]").empty();
        $("[data-referral-3]").empty();
        $("[data-referral-4]").empty();

        if (response.success == true) {
          var socialList = [];
          var getCounts = [];

          $.each(response.data, function (k, v) {
            socialList.push(k);
            getCounts.push(v);
          });
          if (socialList.length == 0) {
            $("#referralsChart").remove();
            $("[no-referral-data]").empty();
            $("[no-referral-data]").append(
              `<div data-empty-category class="card w-100 mt-4"><p class="h6 text-center py-5">No Data Available</p></div>`
            );
          } else {
            for (var i = 0; i < socialList.length; i++) {
              $(`[data-referral-${i + 1}]`).append(`
              <div> <i class="fas fa-circle graph-color-${i + 1}"></i>
                ${socialList[i]}
                </div><div class="text-black">
                ${getCounts[i]} </div>
            `);
            }
            $("#referralsChart").remove(); // this is my <canvas> element
            $("#referralsChartArea").append(
              '<canvas id="referralsChart"><canvas>'
            );

            // chart
            var ctx = document.getElementById("referralsChart");
            var myPieChart = new Chart(ctx, {
              type: "doughnut",
              data: {
                labels: socialList,

                datasets: [
                  {
                    data: getCounts,
                    backgroundColor: ["#FA7415", "#D946EF","#ffbc78","#858796"],
                    hoverBackgroundColor: ["#FA7415", "#D946EF"],
                    hoverBorderColor: "rgba(234, 236, 244, 1)",
                  },
                ],
              },
              options: {
                plugin_one: true,
                responsive: true,

                maintainAspectRatio: false,
                responsive: true,
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
        $(".main-loader").hide();
        // var error_data = JSON.parse(error.responseText);
        $(".card-loader").css("visibility", "hidden");
      },
    });
  }

  function getTotalChartR(start, end) {
    $(".main-loader").show();
    $(".card-loader").css("visibility", "visible");
    $.ajax({
      type: "GET",
      url:
        "/api/rmj/overview/successful-rate/?to_date=" +
        end +
        "&from_date=" +
        start,
      dataType: "json",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization: "Bearer " + localStorage.getItem("access-token"),
      },
      success: function (response) {
        $(".main-loader").hide();
        $(".card-loader").css("visibility", "hidden");
        if (response.success == true) {
          var weekList = [];
          var getCounts = [];

          if (jQuery.isEmptyObject(response.data) == true) {
            $("#totalChart").remove();
            $("[no-total-data]").empty();
            $("[no-total-data]").append(
              `<div data-empty-category class="card w-100 mt-0"><p class="h6 text-center py-5">No Data Available</p></div>`
            );
          } else {
            $.each(response, function () {
              $.each(this, function (k, v) {
                weekList.push(k);
                getCounts.push(v);
              });
            });
            $("#totalChart").remove();
            $("#totalChartArea").append('<canvas id="totalChart"><canvas>');
            // chart
            var ctx = document.getElementById("totalChart");
            var myLineChart = new Chart(ctx, {
              type: "bar",
              data: {
                labels: weekList,
                datasets: [
                  {
                    label: "Total Payout Earned",
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
                    barThickness: 35,
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
                responsive: true,
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
        $(".main-loader").hide();
        // var error_data = JSON.parse(error.responseText);
        $(".card-loader").css("visibility", "hidden");
      },
    });
  }

  function getbrokerageChartR(start, end) {
    $(".card-loader").css("visibility", "visible");
    $.ajax({
      type: "GET",
      url:
        "/api/rmj/overview/successful-disbursed/?to_date=" + end + "&from_date=" + start,
      dataType: "json",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization: "Bearer " + localStorage.getItem("access-token"),
      },
      success: function (response) {
        $(".card-loader").css("visibility", "hidden");
        $(".main-loader").hide();
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
                    barThickness: 35,
                  },
                ],
              },
              options: {
                maintainAspectRatio: false,
                responsive: true,
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

  function getLeadChartR(start, end) {
    $(".card-loader").css("visibility", "visible");
    $.ajax({
      type: "GET",
      url: "/api/rmj/overview/leads/?to_date=" + end + "&from_date=" + start,
      dataType: "json",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization: "Bearer " + localStorage.getItem("access-token"),
      },
      success: function (response) {
        $(".main-loader").hide();
        $(".card-loader").css("visibility", "hidden");
        if (response.success == true) {
          // console.log("response", response.data);
          var monthList = [];
          var addedCount = [];
          // var activatedCount = [];
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
                // activatedCount.push(v.data.activated);
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
                ],
              },
              options: {
                plugins: {
                  legend: {
                    display: false,
                  },
                },
                responsive: true,
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

  function topCardsR(start, end) {
    $(".card-loader").css("visibility", "visible");
    $.ajax({
      type: "GET",
      url: "/api/rmj/overview/?to_date=" + end + "&from_date=" + start,
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization: "Bearer " + localStorage.getItem("access-token"),
      },
      dataType: "json",
      success: function (response) {
        $(".card-loader").css("visibility", "hidden");
        $(".main-loader").hide();
        $("[data-total-leads]").empty();
        $("[data-pending-mandate]").empty();
        $("[data-rejected-mandate]").empty();
        $("[data-successful-mandate]").empty();
        $("[data-disbursal-rate]").empty();
        if (response.success == true) {
          $(".card-loader").css("visibility", "hidden");
          $(
            "[data-completed], [data-employee-count], [data-pending], [data-total]"
          ).empty();
          var total_leads_added = response.data.total_leads_added;
          var pending_mandate = response.data.pending_mandate;
          var rejected_lead = response.data.rejected_lead;
          var successful_mandate = response.data.successful_mandate;
          var success_rate = response.data.success_rate;

          $("[data-total-leads]").append(total_leads_added);
          $("[data-pending-mandate]").append(pending_mandate);
          $("[data-rejected-mandate]").append(rejected_lead);
          $("[data-successful-mandate]").append(successful_mandate);
          $("[data-disbursal-rate]").append(success_rate);
        }
      },
      error: function (error) {
        // var error_data = JSON.parse(error.responseText);
        $(".card-loader").css("visibility", "hidden");
      },
    });
  }

  $(".custom_dateR").flatpickr({
    mode: "range",
    dateFormat: "Y-m-d",

    onChange: function (dates, instance) {
      if (dates.length == 2) {
        var start = this.formatDate(dates[0], "Y-m-d");
        var end = this.formatDate(dates[1], "Y-m-d");
        $('[data-clear-filter]').show();
        $(".main-loader").show();
        topCardsR(start, end);
        getLeadChartR(start, end);
        getbrokerageChartR(start, end);
        getTotalChartR(start, end);
        getTotalMandatesR(start, end);
        $(".main-loader").hide();
      }
    },
  });

});

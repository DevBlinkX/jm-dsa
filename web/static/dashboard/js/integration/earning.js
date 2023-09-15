$(document).ready(function () {
  var days = 30;

  $(".download-select").on("change", function () {
    var url =
      "/dra/downloads/settlements/?days=" +
      days +
      "&download_type=" +
      this.value;
    var link = document.createElement("a");
    link.href = url;
    link.download = "Download Report";
    link.click();
    window.open(url, "_blank");
    link.remove();
  });

  function earningTable() {
    $(".main-loader").show();
    $.ajax({
      type: "GET",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization: "Bearer " + localStorage.getItem("access-token"),
      },
      url: "/api/dra/settlement-list/",
      dataType: "json",
      success: function (response) {
        $("[data-earning-table]").empty();
        var count = response.count;
        var total = count / 10;
        if (count > 10) {
          var total = count / 10;
        } else {
          total = 0;
        }
        if (typeof total === "number") {
          if (total % 1 === 0) {
            total;
          } else {
            total = Math.floor(total + 1);
          }
        } else {
          total = 1;
        }
        $("#pagination-here").bootpag({
          total: total,
          page: 1,
          maxVisible: 5,
          leaps: true,
          href: "javascript: void(0);",
          wrapClass: "pagination",
          activeClass: "active",
          prev: ' <i class="fa fa-arrow-left" aria-hidden="true"></i>',
          next: ' <i class="fa fa-arrow-right" aria-hidden="true"></i>',
        });
        $("#pagination-here").find("a").addClass("page-link", "orange-color");
        $("#pagination-here").find("li").addClass("page-item");
        if (response.results == 0) {
          $("[data-empty-category]").show();
        } else {
          $.each(response.results, function (k, v) {
            var sr = k + 1;
            var month = v.month;
            var year = v.year;
            var converted = v.converted;
            var trade_active = v.trad_active;
            var gross_brokerage = v.gross_brokerage;
            var incentive = v.incentive;
            var net_brokerage = v.net_brokerage;
            var total = v.total;

            $("[data-earning-table]").append(
              "<tr class='text-center'><td>" +
                sr +
                "</td><td>" +
                month +
                ", " +
                year +
                "</td><td> " +
                converted +
                "</td><td>" +
                trade_active +
                "</td><td> &#8377; " +
                incentive +
                "</td><td> &#8377; " +
                net_brokerage +
                "</td><td> &#8377; " +
                gross_brokerage +
                "</td><td> &#8377; " +
                total +
                "</td></tr>"
            );
          });
        }
        $(".main-loader").hide();
      },
    });
  }
  $(".days-select").on("change", function () {
    $(".card-loader").css("visibility", "visible");
    days = this.value;
    $.ajax({
      type: "GET",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization: "Bearer " + localStorage.getItem("access-token"),
      },
      url: "/api/dra/settlement-list/?days=" + this.value,
      dataType: "json",
      success: function (response) {
        $("[data-earning-table]").empty();
        var count = response.count;
        var total = count / 10;
        if (count > 10) {
          var total = count / 10;
        } else {
          total = 0;
        }
        if (typeof total === "number") {
          if (total % 1 === 0) {
            total;
          } else {
            total = Math.floor(total + 1);
          }
        } else {
          total = 1;
        }
        $("#pagination-here").bootpag({
          total: total,
          page: 1,
          maxVisible: 5,
          leaps: true,
          href: "javascript: void(0);",
          wrapClass: "pagination",
          activeClass: "active",
          prev: ' <i class="fa fa-arrow-left" aria-hidden="true"></i>',
          next: ' <i class="fa fa-arrow-right" aria-hidden="true"></i>',
        });
        $("#pagination-here").find("a").addClass("page-link", "orange-color");
        $("#pagination-here").find("li").addClass("page-item");
        if (response.results == 0) {
          $("[data-empty-category]").show();
          // $("[data-earning-table]").append(
          //   `<div data-empty-category class="card w-100 mt-4"><p class="h6 text-center py-5">No Data Available</p></div>`
          // );
        } else {
          $.each(response.results, function (k, v) {
            var sr = k + 1;
            var month = v.month;
            var year = v.year;
            var converted = v.converted;
            var trade_active = v.trad_active;
            var gross_brokerage = v.gross_brokerage;
            var incentive = v.incentive;
            var net_brokerage = v.net_brokerage;
            var total = v.total;

            $("[data-earning-table]").append(
              "<tr class='text-center'><td>" +
                sr +
                "</td><td>" +
                month +
                ", " +
                year +
                "</td><td> " +
                converted +
                "</td><td>" +
                trade_active +
                "</td><td> &#8377; " +
                incentive +
                "</td><td> &#8377; " +
                net_brokerage +
                "</td><td> &#8377; " +
                gross_brokerage +
                "</td><td> &#8377; " +
                total +
                "</td></tr>"
            );
          });
        }
        $(".card-loader").css("visibility", "hidden");
      },
      error: function (error) {
        // var error_data = JSON.parse(error.responseText);
        $(".card-loader").css("visibility", "hidden");
      },
    });
  });

  //   date range
  $(".custom_date").flatpickr({
    mode: 'range',
    dateFormat: "Y-m-d",

    onChange: function(dates, instance) {
        if (dates.length == 2) {
            var start = this.formatDate(dates[0], "Y-m-d");
            var end = this.formatDate(dates[1], "Y-m-d");
            $(".card-loader").css("visibility", "visible");
            days = this.value;
            $.ajax({
              type: "GET",
              headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                Authorization: "Bearer " + localStorage.getItem("access-token"),
              },
              url: "/api/dra/settlement-list/?&to_date=" + end+"&from_date="+ start,
              dataType: "json",
              success: function (response) {
                $("[data-earning-table]").empty();
                var count = response.count;
                var total = count / 10;
                if (count > 10) {
                  var total = count / 10;
                } else {
                  total = 0;
                }
                if (typeof total === "number") {
                  if (total % 1 === 0) {
                    total;
                  } else {
                    total = Math.floor(total + 1);
                  }
                } else {
                  total = 1;
                }
                $("#pagination-here").bootpag({
                  total: total,
                  page: 1,
                  maxVisible: 5,
                  leaps: true,
                  href: "javascript: void(0);",
                  wrapClass: "pagination",
                  activeClass: "active",
                  prev: ' <i class="fa fa-arrow-left" aria-hidden="true"></i>',
                  next: ' <i class="fa fa-arrow-right" aria-hidden="true"></i>',
                });
                $("#pagination-here").find("a").addClass("page-link", "orange-color");
                $("#pagination-here").find("li").addClass("page-item");
                if (response.results == 0) {
                  $("[data-empty-category]").show();
                  // $("[data-earning-table]").append(
                  //   `<div data-empty-category class="card w-100 mt-4"><p class="h6 text-center py-5">No Data Available</p></div>`
                  // );
                } else {
                  $.each(response.results, function (k, v) {
                    var sr = k + 1;
                    var month = v.month;
                    var year = v.year;
                    var converted = v.converted;
                    var trade_active = v.trad_active;
                    var gross_brokerage = v.gross_brokerage;
                    var incentive = v.incentive;
                    var net_brokerage = v.net_brokerage;
                    var total = v.total;

                    $("[data-earning-table]").append(
                      "<tr class='text-center'><td>" +
                        sr +
                        "</td><td>" +
                        month +
                        ", " +
                        year +
                        "</td><td> " +
                        converted +
                        "</td><td>" +
                        trade_active +
                        "</td><td> &#8377; " +
                        incentive +
                        "</td><td> &#8377; " +
                        net_brokerage +
                        "</td><td> &#8377; " +
                        gross_brokerage +
                        "</td><td> &#8377; " +
                        total +
                        "</td></tr>"
                    );
                  });
                }
                $(".card-loader").css("visibility", "hidden");
              },
              error: function (error) {
                // var error_data = JSON.parse(error.responseText);
                $(".card-loader").css("visibility", "hidden");
              },
            });
        }
    }
  })
  //   pagination ajax call
  $("#pagination-here").on("page", function (event, num) {
    $(".card-loader").css("visibility", "visible");
    $.ajax({
      type: "GET",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization: "Bearer " + localStorage.getItem("access-token"),
      },
      url: "/api/dra/settlement-list/?page=" + num,
      dataType: "json",
      success: function (response) {
        $("[data-earning-table]").empty();
        if (response.results == 0) {
          $("[data-empty-category]").show();
          // $("[data-earning-table]").append(
          //   `<div data-empty-category class="card w-100 mt-4"><p class="h6 text-center py-5">No Data Available</p></div>`
          // );
        } else {
          $.each(response.results, function (k, v) {
            var sr = k + 1;
            var month = v.month;
            var year = v.year;
            var converted = v.converted;
            var trade_active = v.trad_active;
            var gross_brokerage = v.gross_brokerage;
            var incentive = v.incentive;
            var net_brokerage = v.net_brokerage;
            var total = v.total;

            $("[data-earning-table]").append(
              "<tr class='text-center'><td>" +
                sr +
                "</td><td>" +
                month +
                ", " +
                year +
                "</td><td> " +
                converted +
                "</td><td>" +
                trade_active +
                "</td><td> &#8377; " +
                incentive +
                "</td><td> &#8377; " +
                net_brokerage +
                "</td><td> &#8377; " +
                gross_brokerage +
                "</td><td> &#8377; " +
                total +
                "</td></tr>"
            );
          });
        }
        $(".card-loader").css("visibility", "hidden");
      },
      error: function (error) {
        // var error_data = JSON.parse(error.responseText);
        $(".card-loader").css("visibility", "hidden");
      },
    });
  });

  function paymentPlanModal() {
    $(".main-loader").show();
    $.ajax({
      type: "GET",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization: "Bearer " + localStorage.getItem("access-token"),
      },
      url: "/api/dra/payout-info/",
      dataType: "json",
      success: function (response) {
        $("[data-incentive]").html(+response[0].incentive);
        $("[data-brokerage]").html(response[0].brokerage + "%");
        $(".main-loader").hide();
      },
      error: function (error) {
        // var error_data = JSON.parse(error.responseText);
        $(".main-loader").hide();
      },
    });
  }

  earningTable();
  paymentPlanModal();
});

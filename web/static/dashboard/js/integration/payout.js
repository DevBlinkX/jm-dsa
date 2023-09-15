$(document).ready(function () {
  var days = 30;

  $(".download-select").on("change", function () {
    var url =
      "/dra/downloads/payout/?days=" +
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
  $(".main-loader").show();
  $.ajax({
    type: "GET",
    url: "/api/dra/payout-page/",
    dataType: "json",
    success: function (response) {
      $(".main-loader").hide();
      console.log(response);
      var next = response.next;
      var prev = response.prev;
      var count = response.count;

      if (response.results == 0) {
        $("[data-empty-category]").show();
        // $("[data-payout-list]").append(
        //   `<div data-empty-category class="card w-100 mt-4"><p class="h6 text-center py-5">No Data Available</p></div>`
        // );
      } else {
        $.each(response.results, function (k, v) {
          var sr = k + 1;
          var date = v.date;
          var payment_mode = v.payment_mode;
          var amount = v.amount;
          var status = v.status;

          if (status === true) {
            $("[data-payout-list]").append(
              "<tr class='text-center'><td>" +
                sr +
                "</td><td>" +
                date +
                "</td><td>" +
                payment_mode +
                "</td><td>" +
                amount +
                "</td><td>" +
                status +
                "</td></tr>"
            );
          } else {
            $("[data-payout-list]").append(
              "<tr class='text-center'><td>" +
                sr +
                "</td><td>" +
                date +
                "</td><td>" +
                payment_mode +
                "</td><td>" +
                amount +
                "</td><td>" +
                status +
                "</td></tr>"
            );
          }
        });
      }
    },
    error: function (error) {
      $(".main-loader").hide();
      // var error_data = JSON.parse(error.responseText);
      $(".card-loader").css("visibility", "hidden");
    },
  });
  $(".days-select").on("change", function () {
    $(".main-loader").show();
    days = this.value;
    $.ajax({
      type: "GET",
      url: "/api/dra/payout-page/?days=" + this.value,
      dataType: "json",
      success: function (response) {
        $(".main-loader").hide();
        $("[data-payout-list]").empty();
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
          // $("[data-payout-list]").append(
          //   `<div data-empty-category class="card w-100 mt-4"><p class="h6 text-center py-5">No Data Available</p></div>`
          // );
        } else {
          $(".main-loader").hide();
          $.each(response.results, function (k, v) {
            var sr = k + 1;
            var date = v.date;
            var payment_mode = v.payment_mode;
            var amount = v.amount;
            var status = v.status;

            if (status === true) {
              $("[data-payout-list]").append(
                "<tr class='text-center'><td>" +
                  sr +
                  "</td><td>" +
                  date +
                  "</td><td>" +
                  payment_mode +
                  "</td><td>" +
                  amount +
                  "</td><td><a href='#' class='green-btn'>Paid</a></td></tr>"
              );
            } else {
              $("[data-payout-list]").append(
                "<tr class='text-center'><td>" +
                  sr +
                  "</td><td>" +
                  date +
                  "</td><td>" +
                  payment_mode +
                  "</td><td>" +
                  amount +
                  "</td><td><a href='#' class='pending-btn'>Pending</a></td></tr>"
              );
            }
          });
        }
        $(".main-loader").hide();
      },
      error: function (error) {
        // var error_data = JSON.parse(error.responseText);
        $(".main-loader").hide();
      },
    });
  });

  // data range
  $(".custom_date").flatpickr({
    mode: 'range',
    dateFormat: "Y-m-d",

    onChange: function(dates, instance) {
        if (dates.length == 2) {
            var start = this.formatDate(dates[0], "Y-m-d");
            var end = this.formatDate(dates[1], "Y-m-d");
          $(".main-loader").show();
          days = this.value;
          $.ajax({
            type: "GET",
            url: "/api/dra/payout-page/?to_date=" + end+"&from_date="+ start,
            dataType: "json",
            success: function (response) {
              $(".main-loader").hide();
              $("[data-payout-list]").empty();
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
                // $("[data-payout-list]").append(
                //   `<div data-empty-category class="card w-100 mt-4"><p class="h6 text-center py-5">No Data Available</p></div>`
                // );
              } else {
                $(".main-loader").hide();
                $.each(response.results, function (k, v) {
                  var sr = k + 1;
                  var date = v.date;
                  var payment_mode = v.payment_mode;
                  var amount = v.amount;
                  var status = v.status;

                  if (status === true) {
                    $("[data-payout-list]").append(
                      "<tr class='text-center'><td>" +
                        sr +
                        "</td><td>" +
                        date +
                        "</td><td>" +
                        payment_mode +
                        "</td><td>" +
                        amount +
                        "</td><td><a href='#' class='green-btn'>Paid</a></td></tr>"
                    );
                  } else {
                    $("[data-payout-list]").append(
                      "<tr class='text-center'><td>" +
                        sr +
                        "</td><td>" +
                        date +
                        "</td><td>" +
                        payment_mode +
                        "</td><td>" +
                        amount +
                        "</td><td><a href='#' class='pending-btn'>Pending</a></td></tr>"
                    );
                  }
                });
              }
              $(".main-loader").hide();
            },
            error: function (error) {
              // var error_data = JSON.parse(error.responseText);
              $(".main-loader").hide();
            },
          });
        }
      }
  })
  //   pagination ajax call
  $("#pagination-here").on("page", function (event, num) {
    $(".main-loader").show();
    $.ajax({
      type: "GET",
      url: "/api/dra/payout-page/?page=" + num,
      dataType: "json",
      success: function (response) {
        $(".main-loader").hide();
        $("[data-payout-list]").empty();
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
          // $("[data-payout-list]").append(
          //   `<div data-empty-category class="card w-100 mt-4"><p class="h6 text-center py-5">No Data Available</p></div>`
          // );
        } else {
          $(".main-loader").hide();
          $.each(response.results, function (k, v) {
            var sr = k + 1;
            var date = v.date;
            var payment_mode = v.payment_mode;
            var amount = v.amount;
            var status = v.status;

            if (status === true) {
              $("[data-payout-list]").append(
                "<tr class='text-center'><td>" +
                  sr +
                  "</td><td>" +
                  date +
                  "</td><td>" +
                  payment_mode +
                  "</td><td>" +
                  amount +
                  "</td><td><a href='#' class='green-btn'>Paid</a></td></tr>"
              );
            } else {
              $("[data-payout-list]").append(
                "<tr class='text-center'><td>" +
                  sr +
                  "</td><td>" +
                  date +
                  "</td><td>" +
                  payment_mode +
                  "</td><td>" +
                  amount +
                  "</td><td><a href='#' class='pending-btn'>Pending</a></td></tr>"
              );
            }
          });
        }
        $(".main-loader").hide();
      },
      error: function (error) {
        // var error_data = JSON.parse(error.responseText);
        $(".main-loader").hide();
      },
    });
  });
});

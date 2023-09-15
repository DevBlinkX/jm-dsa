$(document).ready(function () {
  const urlParams = new URLSearchParams(window.location.search);
  const getName = urlParams.get("name");
  
  $.ajax({
    type: "GET",
    url: "/api/rmj-leads/?name=" + getName,
    dataType: "json",
    success: function (response) {
      $(".main-loader").hide();
      $("[data-leads-list]").empty();
      var count = response.count;
      console.log(count);
      if (count > 10) {
        var total = count / 10;
      } else {
        total = 0;
      }

      if (typeof total === "number" && total != 0) {
        if (total % 1 === 0) {
          total;
        } else {
          total = Math.floor(total + 1);
        }
      } else {
        total = 0;
      }
      console.log("2", count);
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

      if (response.results.length == 0) {
        // $("[data-leads-list]").append(
        //     `<div data-empty-category class="card w-100 mt-4"><p class="h6 text-center py-5">No Data Available</p></div>`
        // );
        $(".main-loader").hide();
        $("[ data-empty-category ]").show();
      } else {
        $(".main-loader").hide();
        $.each(response.results, function (k, v) {
          var sr = k + 1;
          var name = v.name;
          var email = v.email;
          var mobile_no = v.mobile_no;
          var date_created = v.date_created;
          var mandate_status = v.mandate_status;
          var status = v.status;
          var step = v.step;
          var dra_name = v.dra_name;

          $("[data-leads-list]").append(
            "<tr class='table-row'><td>" +
              sr +
              "</td><td class='name'>" +
              name +
              "</td><td class='email'>" +
              email +
              "</td><td class='mobile'> " +
              mobile_no +
              "</td><td class='text-center'> " +
              date_created +
              "</td><td class='text-center'> "+mandate_status+"</td><td class='text-center'> "+status+" </td><td class='text-center'> "+step+" </td><td class='text-center'> <a href='#'class='dashboard-btn'>Remind</a> </td></tr>"
          );
        });

        //          $(".card-loader").css("visibility", "hidden");
      }
    },
    error: function (error) {
      // var error_data = JSON.parse(error.responseText);
      $(".main-loader").hide();
    },
  });
  //   select ajax call
  $(".custom-select").on("change", function () {
    $(".main-loader").show();
    $.ajax({
      type: "GET",
      url: "/api/rmj-leads/?name=" + getName + "&days=" + this.value,
      dataType: "json",
      success: function (response) {
        $('[data-clear-filter]').show();
        $(".main-loader").hide();
        $("[data-leads-list]").empty();
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
        if (response.results.length == 0) {
          // $("[data-leads-list]").append(
          //     `<div data-empty-category class="card w-100 mt-4"><p class="h6 text-center py-5">No Data Available</p></div>`
          // );
          $(".main-loader").hide();
          $("[ data-empty-category ]").show();
        } else {
          $(".main-loader").hide();
          $.each(response.results, function (k, v) {
          var sr = k + 1;
          var name = v.name;
          var email = v.email;
          var mobile_no = v.mobile_no;
          var date_created = v.date_created;
          var mandate_status = v.mandate_status;
          var status = v.status;
          var step = v.step;
          var dra_name = v.dra_name;

          $("[data-leads-list]").append(
            "<tr class='table-row'><td>" +
              sr +
              "</td><td class='name'>" +
              name +
              "</td><td class='email'>" +
              email +
              "</td><td class='mobile'> " +
              mobile_no +
              "</td><td class='text-center'> " +
              date_created +
              "</td><td class='text-center'> "+mandate_status+"</td><td class='text-center'> "+status+" </td><td class='text-center'> "+step+" </td><td class='text-center'> <a href='#'class='dashboard-btn'>Remind</a> </td></tr>"
          );
          });

          $(".card-loader").css("visibility", "hidden");
        }
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
            $.ajax({
              type: "GET",
              url: "/api/rmj-leads/?name=" + getName + "&to_date=" + end+"&from_date="+ start,
              dataType: "json",
              success: function (response) {
                $('[data-clear-filter]').show();
                $(".main-loader").hide();
                $("[data-leads-list]").empty();
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
                if (response.results.length == 0) {
                  // $("[data-leads-list]").append(
                  //     `<div data-empty-category class="card w-100 mt-4"><p class="h6 text-center py-5">No Data Available</p></div>`
                  // );
                  $(".main-loader").hide();
                  $("[ data-empty-category ]").show();
                } else {
                  $(".main-loader").hide();
                  $.each(response.results, function (k, v) {
                    var sr = k + 1;
          var name = v.name;
          var email = v.email;
          var mobile_no = v.mobile_no;
          var date_created = v.date_created;
          var mandate_status = v.mandate_status;
          var status = v.status;
          var step = v.step;
          var dra_name = v.dra_name;

          $("[data-leads-list]").append(
            "<tr class='table-row'><td>" +
              sr +
              "</td><td class='name'>" +
              name +
              "</td><td class='email'>" +
              email +
              "</td><td class='mobile'> " +
              mobile_no +
              "</td><td class='text-center'> " +
              date_created +
              "</td><td class='text-center'> "+mandate_status+"</td><td class='text-center'> "+status+" </td><td class='text-center'> "+step+" </td><td class='text-center'> <a href='#'class='dashboard-btn'>Remind</a> </td></tr>"
          );
                  });

                  $(".card-loader").css("visibility", "hidden");
                }
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
      url: "/api/rmj-leads/?name=" + getName + "&page=" + num,
      dataType: "json",
      success: function (response) {
        $("[data-leads-list]").empty();
        $(".main-loader").hide();
        $.each(response.results, function (k, v) {
          var sr = k + 1;
          var name = v.name;
          var email = v.email;
          var mobile_no = v.mobile_no;
          var date_created = v.date_created;
          var mandate_status = v.mandate_status;
          var status = v.status;
          var step = v.step;
          var dra_name = v.dra_name;

          $("[data-leads-list]").append(
            "<tr class='table-row'><td>" +
              sr +
              "</td><td class='name'>" +
              name +
              "</td><td class='email'>" +
              email +
              "</td><td class='mobile'> " +
              mobile_no +
              "</td><td class='text-center'> " +
              date_created +
              "</td><td class='text-center'> "+mandate_status+"</td><td class='text-center'> "+status+" </td><td class='text-center'> "+step+" </td><td class='text-center'> <a href='#'class='dashboard-btn'>Remind</a> </td></tr>"
          );
        });

        $(".card-loader").css("visibility", "hidden");
      },
      error: function (error) {
        // var error_data = JSON.parse(error.responseText);
        $(".main-loader").hide();
      },
    });
  });
});

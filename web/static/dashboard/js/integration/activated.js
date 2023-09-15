$(document).ready(function () {
  const urlParams = new URLSearchParams(window.location.search);
  const getName = urlParams.get("name");

  // first load ajax call
  $(".card-loader").css("visibility", "hidden");
  $(".main-loader").show();
  $.ajax({
    type: "GET",
    url: "/api/dra/activated/user-list/?name=" + getName,
    dataType: "json",
    success: function (response) {
      console.log(response);
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
        // $("[data-activated-list]").append(
        //   `<div data-empty-category class="card w-100 mt-4"><p class="h6 text-center py-5">No Data Available</p></div>`
        // );
        $(".main-loader").hide();
        $("[data-activated-list]").empty();
        $("[data-empty-category]").show();
      } else {
        $.each(response.results, function (k, v) {
          console.log(response.results);
          var sr = k + 1;
          var name = v.name;
          var email = v.email;
          var mobile_no = v.mobile;
          var user_channel = v.user_channel;
          var is_activated = v.is_activated;

          if (is_activated == true) {
            $("[data-activated-list]").append(
              "<tr><td>" +
                sr +
                "</td><td>" +
                name +
                "</td><td>" +
                email +
                "</td><td> " +
                mobile_no +
                "</td><td> " +
                user_channel +
                "</td><td> <span class='green-dot'></span></td></tr>"
            );
          } else {
            $("[data-activated-list]").append(
              "<tr><td>" +
                sr +
                "</td><td>" +
                name +
                "</td><td>" +
                email +
                "</td><td> " +
                mobile_no +
                "</td><td> " +
                user_channel +
                "</td><td> <span class='red-dot'></span></td></tr>"
            );
          }
        });
        $(".main-loader").hide();
      }
      $(".main-loader").hide();
    },
    error: function (error) {
      // var error_data = JSON.parse(error.responseText);
      $(".main-loader").hide();
    },
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
            $.ajax({
              type: "GET",
              url:
                "/api/dra/activated/user-list/?name=" + getName + "&to_date=" + end+"&from_date="+ start,
              dataType: "json",
              success: function (response) {
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
                  // $("[data-activated-list]").append(
                  //   `<div data-empty-category class="card w-100 mt-4"><p class="h6 text-center py-5">No Data Available</p></div>`
                  // );
                  $(".card-loader").css("visibility", "hidden");
                  $("[data-activated-list]").empty();
                  $("[data-empty-category]").show();
                } else {
                  $("[data-activated-list]").empty();

                  $.each(response.results, function (k, v) {
                    var sr = k + 1;
                    var name = v.name;
                    var email = v.email;
                    var mobile_no = v.mobile;
                    var user_channel = v.user_channel;
                    var is_activated = v.is_activated;

                    if (is_activated == true) {
                      $("[data-activated-list]").append(
                        "<tr><td>" +
                          sr +
                          "</td><td>" +
                          name +
                          "</td><td>" +
                          email +
                          "</td><td> " +
                          mobile_no +
                          "</td><td> " +
                          user_channel +
                          "</td><td> <span class='green-dot'></span></td></tr>"
                      );
                    } else {
                      $("[data-activated-list]").append(
                        "<tr><td>" +
                          sr +
                          "</td><td>" +
                          name +
                          "</td><td>" +
                          email +
                          "</td><td> " +
                          mobile_no +
                          "</td><td> " +
                          user_channel +
                          "</td><td> <span class='red-dot'></span></td></tr>"
                      );
                    }
                  });
                  $(".card-loader").css("visibility", "hidden");
                }
              },
              error: function (error) {
                // var error_data = JSON.parse(error.responseText);
                $(".card-loader").css("visibility", "hidden");
              },
            });
      }
    }
  })

  //   select ajax call
  $(".days-select").on("change", function () {
    $(".card-loader").css("visibility", "visible");
    $.ajax({
      type: "GET",
      url:
        "/api/dra/activated/user-list/?name=" + getName + "&days=" + this.value,
      dataType: "json",
      success: function (response) {
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
          // $("[data-activated-list]").append(
          //   `<div data-empty-category class="card w-100 mt-4"><p class="h6 text-center py-5">No Data Available</p></div>`
          // );
          $(".card-loader").css("visibility", "hidden");
          $("[data-activated-list]").empty();
          $("[data-empty-category]").show();
        } else {
          $("[data-activated-list]").empty();

          $.each(response.results, function (k, v) {
            var sr = k + 1;
            var name = v.name;
            var email = v.email;
            var mobile_no = v.mobile;
            var user_channel = v.user_channel;
            var is_activated = v.is_activated;

            if (is_activated == true) {
              $("[data-activated-list]").append(
                "<tr><td>" +
                  sr +
                  "</td><td>" +
                  name +
                  "</td><td>" +
                  email +
                  "</td><td> " +
                  mobile_no +
                  "</td><td> " +
                  user_channel +
                  "</td><td> <span class='green-dot'></span></td></tr>"
              );
            } else {
              $("[data-activated-list]").append(
                "<tr><td>" +
                  sr +
                  "</td><td>" +
                  name +
                  "</td><td>" +
                  email +
                  "</td><td> " +
                  mobile_no +
                  "</td><td> " +
                  user_channel +
                  "</td><td> <span class='red-dot'></span></td></tr>"
              );
            }
          });
          $(".card-loader").css("visibility", "hidden");
        }
      },
      error: function (error) {
        // var error_data = JSON.parse(error.responseText);
        $(".card-loader").css("visibility", "hidden");
      },
    });
  });

  //   pagination ajax call
  $("#pagination-here").on("page", function (event, num) {
    $(".card-loader").css("visibility", "visible");

    $.ajax({
      type: "GET",
      url: "/api/dra/activated/user-list/?name=" + getName + "&page=" + num,
      dataType: "json",
      success: function (response) {
        $("[data-activated-list]").empty();
        if (response.results.length == 0) {
          // $("[data-activated-list]").append(
          //   `<div data-empty-category class="card w-100 mt-4"><p class="h6 text-center py-5">No Data Available</p></div>`
          // );

          $("[data-activated-list]").empty();
          $("[data-empty-category]").show();
          $(".card-loader").css("visibility", "hidden");
        } else {
          $.each(response.results, function (k, v) {
            var sr = k + 1;
            var name = v.name;
            var email = v.email;
            var mobile_no = v.mobile;
            var user_channel = v.user_channel;
            var is_activated = v.is_activated;

            if (is_activated == true) {
              $("[data-activated-list]").append(
                "<tr><td>" +
                  sr +
                  "</td><td>" +
                  name +
                  "</td><td>" +
                  email +
                  "</td><td> " +
                  mobile_no +
                  "</td><td> " +
                  user_channel +
                  "</td><td> <span class='green-dot'></span></td></tr>"
              );
            } else {
              $("[data-activated-list]").append(
                "<tr><td>" +
                  sr +
                  "</td><td>" +
                  name +
                  "</td><td>" +
                  email +
                  "</td><td> " +
                  mobile_no +
                  "</td><td> " +
                  user_channel +
                  "</td><td> <span class='red-dot'></span></td></tr>"
              );
            }
          });
          $(".card-loader").css("visibility", "hidden");
        }
      },
      error: function (error) {
        // var error_data = JSON.parse(error.responseText);
        $(".card-loader").css("visibility", "hidden");
      },
    });
  });
});

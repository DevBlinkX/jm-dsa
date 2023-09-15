$(document).ready(function () {
  function rmSignupTable() {
    $(".main-loader").show();
    $.ajax({
      type: "GET",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization: "Bearer " + localStorage.getItem("access-token"),
      },
      url: "/api/rm/signup/list/",
      dataType: "json",
      success: function (response) {
        $(".main-loader").hide();
        $("[data-rm-signup]").empty();

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
          // $("[data-rm-signup]").append(
          //   `<div data-empty-category class="card w-100 mt-4"><p class="h6  py-5">No Data Available</p></div>`
          // );
          $("[data-empty-category]").show();
        } else {
          $.each(response.results, function (k, v) {
            var username = v.username;
            var name = v.name;
            var email = v.email;
            var number = v.mobile;
            var stage = v.stage;
            var createdAt = v.date;
            var agreement = v.agreement;
            var adminStatus = v.admin_status;
            if (adminStatus == "approved" || adminStatus == "submitted") {
              $("[data-rm-signup]").append(
                "<tr class=''><td>" +
                  name +
                  "</td><td>" +
                  email +
                  "</td><td>" +
                  number +
                  "</td><td>" +
                  stage +
                  "</td><td>" +
                  createdAt +
                  "</td><td class=''>" +
                  agreement +
                  "</td><td class='d-none username'>" +
                  username +
                  `</td><td class="text-capitalize">` +
                  adminStatus +
                  "</td></tr>"
              );
            } else if (
              adminStatus == "pending" ||
              adminStatus == "unapproved"
            ) {
              $("[data-rm-signup]").append(
                "<tr class=''><td>" +
                  name +
                  "</td><td>" +
                  email +
                  "</td><td>" +
                  number +
                  "</td><td>" +
                  stage +
                  "</td><td>" +
                  createdAt +
                  "</td><td class=''>" +
                  agreement +
                  "</td><td class='d-none username'>" +
                  username +
                  `</td><td><a href="#" class='pending-btn text-capitalize' data-toggle='modal'
                    data-target='#signup-dra-modal'>` +
                  adminStatus +
                  "</a></td></tr>"
              );
            } else {
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

  $(document).on("click", ".pending-btn", function () {
    var username = $(this).closest("td").prev().html();
    $("#username-form").val(username);
    var that = $(this);

    $("[data-rm-form]").on("submit", function (e) {
      e.preventDefault();
      e.stopPropagation();
      $(".main-loader").show();

      var formdata = new FormData($(this)[0]);

      var href = $(this).attr("action");

      $.ajax({
        type: "POST",
        url: href,
        headers: {
          Authorization: "Bearer " + localStorage.getItem("access-token"),
        },
        data: formdata,
        dataType: "json",
        processData: false,
        contentType: false,
        success: function (response) {
          $(".main-loader").hide();
          if (response.success == true) {
            $(".main-loader").show();
            $(".pending-btn").removeAttr("data-target");
            $(".pending-btn").addClass("table-secondary-color");
            $(".pending-btn").removeClass("pending-btn");

            setTimeout(function () {
              $(".main-loader").hide();
            }, 1000);
            $("#signup-dra-modal").modal("toggle");
            $("#rm-modal-form").trigger("reset");
            that.html("submitted");
            $("#signup-dra-modal").modal("toggle");
            $(".pending-btn").removeAttr("data-target");
          }
        },
        error: function (err) {
          $(".main-loader").hide();
        },
      });
    });
  });

  //   select ajax call
  $(".custom-select").on("change", function () {
    $(".main-loader").show();
    $.ajax({
      type: "GET",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization: "Bearer " + localStorage.getItem("access-token"),
      },
      url: "/api/rm/signup/list/?days=" + this.value,
      dataType: "json",
      success: function (response) {
        $(".main-loader").hide();
        $("[data-rm-signup]").empty();

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
          // $("[data-rm-signup]").append(
          //   `<div data-empty-category class="card w-100 mt-4"><p class="h6  py-5">No Data Available</p></div>`
          // );
          $("[data-empty-category]").show();
        } else {
          $.each(response.results, function (k, v) {
            var username = v.username;
            var name = v.name;
            var email = v.email;
            var number = v.mobile;
            var stage = v.stage;
            var createdAt = v.date;
            var agreement = v.agreement;
            var adminStatus = v.admin_status;
            if (adminStatus == "approved" || adminStatus == "submitted") {
              $("[data-rm-signup]").append(
                "<tr class=''><td>" +
                  name +
                  "</td><td>" +
                  email +
                  "</td><td>" +
                  number +
                  "</td><td>" +
                  stage +
                  "</td><td>" +
                  createdAt +
                  "</td><td class=''>" +
                  agreement +
                  "</td><td class='d-none username'>" +
                  username +
                  `</td><td class="text-capitalize">` +
                  adminStatus +
                  "</td></tr>"
              );
            } else if (
              adminStatus == "pending" ||
              adminStatus == "unapproved"
            ) {
              $("[data-rm-signup]").append(
                "<tr class=''><td>" +
                  name +
                  "</td><td>" +
                  email +
                  "</td><td>" +
                  number +
                  "</td><td>" +
                  stage +
                  "</td><td>" +
                  createdAt +
                  "</td><td class=''>" +
                  agreement +
                  "</td><td class='d-none username'>" +
                  username +
                  `</td><td><a href="#" class='pending-btn text-capitalize' data-toggle='modal'
                    data-target='#signup-dra-modal'>` +
                  adminStatus +
                  "</a></td></tr>"
              );
            } else {
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
  //   pagination ajax call
  $("#pagination-here").on("page", function (event, num) {
    $(".main-loader").show();
    $.ajax({
      type: "GET",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization: "Bearer " + localStorage.getItem("access-token"),
      },
      url: "/api/rm/signup/list/?page=" + num,
      dataType: "json",
      success: function (response) {
        $(".main-loader").hide();
        $("[data-rm-signup]").empty();

        if (response.results.length == 0) {
          // $("[data-rm-signup]").append(
          //   `<div data-empty-category class="card w-100 mt-4"><p class="h6  py-5">No Data Available</p></div>`
          // );
          $("[data-empty-category]").show();
        } else {
          $.each(response.results, function (k, v) {
            var username = v.username;
            var name = v.name;
            var email = v.email;
            var number = v.mobile;
            var stage = v.stage;
            var createdAt = v.date;
            var agreement = v.agreement;
            var adminStatus = v.admin_status;
            if (adminStatus == "approved" || adminStatus == "submitted") {
              $("[data-rm-signup]").append(
                "<tr class=''><td>" +
                  name +
                  "</td><td>" +
                  email +
                  "</td><td>" +
                  number +
                  "</td><td>" +
                  stage +
                  "</td><td>" +
                  createdAt +
                  "</td><td class=''>" +
                  agreement +
                  "</td><td class='d-none username'>" +
                  username +
                  `</td><td class="text-capitalize">` +
                  adminStatus +
                  "</td></tr>"
              );
            } else if (
              adminStatus == "pending" ||
              adminStatus == "unapproved"
            ) {
              $("[data-rm-signup]").append(
                "<tr class=''><td>" +
                  name +
                  "</td><td>" +
                  email +
                  "</td><td>" +
                  number +
                  "</td><td>" +
                  stage +
                  "</td><td>" +
                  createdAt +
                  "</td><td class=''>" +
                  agreement +
                  "</td><td class='d-none username'>" +
                  username +
                  `</td><td><a href="#" class='pending-btn text-capitalize' data-toggle='modal'
                    data-target='#signup-dra-modal'>` +
                  adminStatus +
                  "</a></td></tr>"
              );
            } else {
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

  rmSignupTable();
});

$(document).ready(function () {
  function appendKnowledgeCards() {
    $(".main-loader").show();
    $(".card-loader").css("visibility", "visible");
    $.ajax({
      type: "GET",
      url: "/api/dra/knowlage-center-list/",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization: "Bearer " + localStorage.getItem("access-token"),
      },
      dataType: "json",
      success: function (response) {
        $(".main-loader").hide();
        $(".card-loader").css("visibility", "hidden");
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
          $("[data-empty-insights]").show();
        } else {
          $.each(response.results, function (k, v) {
            $("[data-knowldge-cards]").append(`<div class="card">
                            <div class="img-wrapper">
                                <a href="/dra-knowledge-center-details/?${v.slug}"><img src="${v.image}" alt="dot" class="top-right"></a>
                            </div>
                            <div class="text-wrapper">
                                <div class="category-wrapper mb-2">
                                    <div class="category">${v.category.name}</div>
                                </div>
                                <div class="">
                                    <a href="/dra-knowledge-center-details/?${v.slug}" class="heading my-3 text-capitalize">${v.title}</a>
                                </div>
                                
                                <div class="d-flex justify-content-between align-items-center date-wrapper">
                                    <div class="date font-size-15">
                                        ${v.new_date_format}
                                    </div>

                                    <a href="/dra-knowledge-center-details/?${v.slug}"><svg class="arrow" width="25" height="14" viewBox="0 0 25 14" fill="none"
                                        xmlns="http://www.w3.org/2000/svg">
                                        <path
                                            d="M9.44053 6.78463H23.6326L17.6115 0.847565C17.5695 0.806185 17.5695 0.73924 17.6115 0.69786C17.6534 0.65648 17.7214 0.65648 17.7633 0.69786L23.9686 6.81426C23.9888 6.83417 24.0002 6.86087 24.0002 6.88911C24.0002 6.91722 23.9888 6.94405 23.9686 6.96396L17.7633 13.0804C17.7214 13.1217 17.6534 13.1216 17.6115 13.0802C17.5695 13.039 17.5695 12.9719 17.6115 12.9305L23.6326 6.99562H9.44053C9.38135 6.99562 9.3335 6.94831 9.3335 6.89012C9.3335 6.83193 9.38135 6.78463 9.44053 6.78463Z"
                                            fill="url(#paint0_linear_417_5049)" stroke="url(#paint0_linear_417_5049)" />
                                        <circle cx="0.66667" cy="7.11149" r="0.66667" fill="url(#paint0_linear_417_5049)" />
                                        <circle cx="3.77751" cy="7.11149" r="0.66667" fill="url(#paint0_linear_417_5049)" />
                                        <circle cx="6.88884" cy="7.11149" r="0.66667" fill="url(#paint0_linear_417_5049)" />
                                        <defs>
                                            <linearGradient id="paint0_linear_417_5049" x1="15" y1="-8.5" x2="18.5" y2="28"
                                                gradientUnits="userSpaceOnUse">
                                                <stop stop-color="#EC590C" />
                                                <stop offset="1" stop-color="#C027D2" />
                                            </linearGradient>
                                        </defs>
                                    </svg></a>
                                </div>
                            </div>

                        </div>`);
          });
        }
      },
      error: function (error) {
        $(".main-loader").hide();
        $(".card-loader").css("visibility", "hidden");
      },
    });
  }

  function appendTrending() {
    $(".main-loader").show();

    $.ajax({
      type: "GET",
      url: "/api/dra/trending/knowlage-center/",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization: "Bearer " + localStorage.getItem("access-token"),
      },
      dataType: "json",
      success: function (response) {
        $(".main-loader").hide();

        if (response == 0) {
          $("[data-empty-trending]").show();
        } else {
          $.each(response, function (k, v) {
            $("[data-trending-cards]").append(`<div class="card">
                            <div class="img-wrapper">
                                <a href="/dra-knowledge-center-details/?${v.slug}"><img src="${v.image}" alt="dot" class="top-right"></a>
                            </div>
                            <div class="text-wrapper">
                                <div class="category-wrapper mb-2">
                                    <div class="category">${v.category.name}</div>
                                </div>
                                <div class="">
                                    <a href="/dra-knowledge-center-details/?${v.slug}" class="heading my-3 text-capitalize">${v.title}</a>
                                </div>
                                
                                <div class="d-flex justify-content-between align-items-center date-wrapper">
                                    <div class="date font-size-15">
                                        ${v.new_date_format}
                                    </div>

                                    <a href="/dra-knowledge-center-details/?${v.slug}"><svg class="arrow" width="25" height="14" viewBox="0 0 25 14" fill="none"
                                        xmlns="http://www.w3.org/2000/svg">
                                        <path
                                        d="M9.44053 6.78463H23.6326L17.6115 0.847565C17.5695 0.806185 17.5695 0.73924 17.6115 0.69786C17.6534 0.65648 17.7214 0.65648 17.7633 0.69786L23.9686 6.81426C23.9888 6.83417 24.0002 6.86087 24.0002 6.88911C24.0002 6.91722 23.9888 6.94405 23.9686 6.96396L17.7633 13.0804C17.7214 13.1217 17.6534 13.1216 17.6115 13.0802C17.5695 13.039 17.5695 12.9719 17.6115 12.9305L23.6326 6.99562H9.44053C9.38135 6.99562 9.3335 6.94831 9.3335 6.89012C9.3335 6.83193 9.38135 6.78463 9.44053 6.78463Z"
                                        fill="url(#paint0_linear_417_5049)" stroke="url(#paint0_linear_417_5049)" />
                                    <circle cx="0.66667" cy="7.11149" r="0.66667" fill="url(#paint0_linear_417_5049)" />
                                    <circle cx="3.77751" cy="7.11149" r="0.66667" fill="url(#paint0_linear_417_5049)" />
                                    <circle cx="6.88884" cy="7.11149" r="0.66667" fill="url(#paint0_linear_417_5049)" />
                                    <defs>
                                        <linearGradient id="paint0_linear_417_5049" x1="15" y1="-8.5" x2="18.5" y2="28"
                                            gradientUnits="userSpaceOnUse">
                                            <stop stop-color="#EC590C" />
                                            <stop offset="1" stop-color="#C027D2" />
                                        </linearGradient>
                                    </defs>
                                    </svg></a>
                                </div>
                            </div>

                        </div>`);
          });
        }
      },
      error: function (error) {
        $(".main-loader").hide();
      },
    });
  }

  // tags
  function getTags() {
    $(".main-loader").show();
    $.ajax({
      type: "GET",
      url: "/api/dra/tag-list/",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization: "Bearer " + localStorage.getItem("access-token"),
      },
      dataType: "json",
      success: function (response) {
        $(".main-loader").hide();
        if (response.length == 0) {
          $("[data-empty-tags]").show();
        } else {
          $.each(response, function (k, v) {
            $("[data-tags]").append('<span class="tags">' + v.name + '</span>');
          });
        }
      },
      error: function (error) {
        $(".main-loader").hide();
      },
    });
  }

  //keywords
  function getKeywords() {
    $(".main-loader").show();
    $.ajax({
      type: "GET",
      url: "/api/get-keyword-list/",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization: "Bearer " + localStorage.getItem("access-token"),
      },
      dataType: "json",
      success: function (response) {
        $(".main-loader").hide();
        if (response.length == 0) {
          $("[data-empty-keywords]").show();
        } else {
          $.each(response, function (k, v) {
            $("[data-keywords]").append(
              '<span class="tags">' + v.name + "</span>"
            );
          });
        }
      },
      error: function (error) {
        $(".main-loader").hide();
      },
    });
  }
  // category
  function getCategory() {
    $(".main-loader").show();
    $.ajax({
      type: "GET",
      url: "/api/dra/category-list/",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization: "Bearer " + localStorage.getItem("access-token"),
      },
      dataType: "json",
      success: function (response) {
        $(".main-loader").hide();
        $.each(response, function (k, v) {
          $("[data-category-list]").append(
            '<li class="nav-item"><a class="nav-link text-capitalize" data-toggle="tab" href="#' +
              v.slug +
              '" role="tab" aria-controls="' +
              v.slug +
              '" aria-selected="false" data-tab="' +
              v.slug +
              '">' +
              v.name +
              "</a></li>"
          );
          // $('[data-category-tabs]').append('<div class="tab-pane fade" id="'+v.slug+'" role="tabpanel" aria-labelledby="'+v.slug+'-tab"><div class="tab-grid my-4" data-category-cards></div></div>')
          // $("[data-category-list]").find('.nav-link').first().addClass("active");
          // $("[data-category-tabs]").find('.tab-pane').first().addClass("show active");
        });
      },
      error: function (error) {
        $(".main-loader").hide();
      },
    });
  }

  getTags();
  getKeywords();
  getCategory();
  appendKnowledgeCards();
  appendTrending();

  setTimeout(function () {
    $("[data-tab]").on("click", function () {
      var getCataval = $(this).data("tab");
      $("[data-category-tabs], [data-category-cards]").empty();

      $("[data-category-tabs]").append(
        '<div class="tab-pane fade" id="' +getCataval +'" role="tabpanel" aria-labelledby="' +getCataval +'-tab"><div class="tab-grid my-4" data-category-cards></div></div>');
        $(".main-loader").show();
      $.ajax({
        type: "GET",
        url: "/api/dra/knowlage-center-list/?category__slug="+getCataval,
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          Authorization: "Bearer " + localStorage.getItem("access-token"),
        },
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

          $(".main-loader").hide();
          if(response.results == 0){
              $("[data-category-cards]").removeClass('tab-grid');
              $("[data-category-cards]").append(
                `<div data-empty-category class="card w-100 mt-4"><p class="h6 text-center py-5">No Data Available</p></div>`
            );
          } else {
          $.each(response.results, function (k, v) {

              $("[data-category-cards]")
                .append(`<div class="card detail-available">
                                    <div class="img-wrapper">
                                        <a href="/dra-knowledge-center-details/?${v.slug}"><img src="${v.image}" alt="dot"
                                                class="top-right"></a>
                                    </div>
                                    <div class="text-wrapper">
                                        <div class="category-wrapper mb-2">
                                            <div class="category">${v.category.name}</div>
                                        </div>
                                        <div class="heading my-3 text-capitalize">
                                            <a href="/dra-knowledge-center-details/?${v.slug}" class="heading">${v.title}</a>
                                        </div>
                                        
                                        <div class="d-flex justify-content-between align-items-center date-wrapper">
                                            <div class="date font-size-15">
                                                ${v.new_date_format}
                                            </div>

                                            <a href="/dra-knowledge-center-details/?${v.slug}"><svg class="arrow" width="25" height="14" viewBox="0 0 25 14"
                                                    fill="none" xmlns="http://www.w3.org/2000/svg">
                                                    <path
                                                    d="M9.44053 6.78463H23.6326L17.6115 0.847565C17.5695 0.806185 17.5695 0.73924 17.6115 0.69786C17.6534 0.65648 17.7214 0.65648 17.7633 0.69786L23.9686 6.81426C23.9888 6.83417 24.0002 6.86087 24.0002 6.88911C24.0002 6.91722 23.9888 6.94405 23.9686 6.96396L17.7633 13.0804C17.7214 13.1217 17.6534 13.1216 17.6115 13.0802C17.5695 13.039 17.5695 12.9719 17.6115 12.9305L23.6326 6.99562H9.44053C9.38135 6.99562 9.3335 6.94831 9.3335 6.89012C9.3335 6.83193 9.38135 6.78463 9.44053 6.78463Z"
                                                    fill="url(#paint0_linear_417_5049)" stroke="url(#paint0_linear_417_5049)" />
                                                <circle cx="0.66667" cy="7.11149" r="0.66667" fill="url(#paint0_linear_417_5049)" />
                                                <circle cx="3.77751" cy="7.11149" r="0.66667" fill="url(#paint0_linear_417_5049)" />
                                                <circle cx="6.88884" cy="7.11149" r="0.66667" fill="url(#paint0_linear_417_5049)" />
                                                <defs>
                                                    <linearGradient id="paint0_linear_417_5049" x1="15" y1="-8.5" x2="18.5" y2="28"
                                                        gradientUnits="userSpaceOnUse">
                                                        <stop stop-color="#EC590C" />
                                                        <stop offset="1" stop-color="#C027D2" />
                                                    </linearGradient>
                                                </defs>
                                                </svg></a>
                                        </div>
                                    </div>

                                </div>`);
            
          });
          }
        },
        error: function (error) {
          // var error_data = JSON.parse(error.responseText);
          $(".main-loader").hide();
        },
      });
    });
    $("[data-category-list]").find(".nav-link").first().click();
  }, 1000);

  //   pagination ajax call
  $("#pagination-here").on("page", function (event, num) {
    $(".main-loader").show();
    $.ajax({
      type: "GET",
      url: "/api/dra/knowlage-center-list/?page=" + num,
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization: "Bearer " + localStorage.getItem("access-token"),
      },
      dataType: "json",
      success: function (response) {
        $(".main-loader").hide();
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
          $("[data-empty-insights]").show();
        } else {
          $.each(response.results, function (k, v) {
            $("[data-knowldge-cards]").append(`<div class="card">
                            <div class="img-wrapper">
                                <a href="/dra-knowledge-center-details/?${v.slug}"><img src="${v.image}" alt="dot" class="top-right"></a>
                            </div>
                            <div class="text-wrapper">
                                <div class="category-wrapper mb-2">
                                    <div class="category">${v.category.name}</div>
                                </div>
                                <div class="">
                                    <a href="/dra-knowledge-center-details/?${v.slug}" class="heading my-3 text-capitalize">${v.title}</a>
                                </div>
                                
                                <div class="d-flex justify-content-between align-items-center date-wrapper">
                                    <div class="date font-size-15">
                                        ${v.new_date_format}
                                    </div>

                                    <a href="/dra-knowledge-center-details/?${v.slug}"><svg class="arrow" width="25" height="14" viewBox="0 0 25 14" fill="none"
                                        xmlns="http://www.w3.org/2000/svg">
                                        <path
                                        d="M9.44053 6.78463H23.6326L17.6115 0.847565C17.5695 0.806185 17.5695 0.73924 17.6115 0.69786C17.6534 0.65648 17.7214 0.65648 17.7633 0.69786L23.9686 6.81426C23.9888 6.83417 24.0002 6.86087 24.0002 6.88911C24.0002 6.91722 23.9888 6.94405 23.9686 6.96396L17.7633 13.0804C17.7214 13.1217 17.6534 13.1216 17.6115 13.0802C17.5695 13.039 17.5695 12.9719 17.6115 12.9305L23.6326 6.99562H9.44053C9.38135 6.99562 9.3335 6.94831 9.3335 6.89012C9.3335 6.83193 9.38135 6.78463 9.44053 6.78463Z"
                                        fill="url(#paint0_linear_417_5049)" stroke="url(#paint0_linear_417_5049)" />
                                    <circle cx="0.66667" cy="7.11149" r="0.66667" fill="url(#paint0_linear_417_5049)" />
                                    <circle cx="3.77751" cy="7.11149" r="0.66667" fill="url(#paint0_linear_417_5049)" />
                                    <circle cx="6.88884" cy="7.11149" r="0.66667" fill="url(#paint0_linear_417_5049)" />
                                    <defs>
                                        <linearGradient id="paint0_linear_417_5049" x1="15" y1="-8.5" x2="18.5" y2="28"
                                            gradientUnits="userSpaceOnUse">
                                            <stop stop-color="#EC590C" />
                                            <stop offset="1" stop-color="#C027D2" />
                                        </linearGradient>
                                    </defs>
                                    </svg></a>
                                </div>
                            </div>

                        </div>`);
          });
        }
      },
      error: function (error) {
        // var error_data = JSON.parse(error.responseText);
        $(".main-loader").hide();
      },
    });
  });
});

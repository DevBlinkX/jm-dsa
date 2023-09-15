(function ($) {
  // $(".error").css('visiblity', 'hidden');
  $(".error").attr("style", "visibility: hidden");

  const validateEmail = (email) => {
    return email.match(
      /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    );
  };

  const validateMobile = (mobile) => {
    return mobile.match(/^[789]\d{9}$/);
  };

  $("[data-check-username]").on("change", function (e) {
    var href = "/api/check/username/";
    var username = $("#name").val();
    // $("#nameHelp").attr("style", 'visibility: visible');
    if (username != "") {
      $.ajax({
        type: "POST",
        url: href,
        data: { username: username },
        dataType: "json",
        success: function (response) {
          $("#nameHelp").attr("style", "visibility: hidden");
        },
        error: function (error) {
          var error_data = JSON.parse(error.responseText);
          $("#nameHelp").attr("style", "visibility: visible");
        },
      });
    }
  });
$("[data-check-email]").keyup(function () {
  var email = $("[data-check-email]").val();
  if (validateEmail(email)) {
      $.ajax({
        type: "POST",
        url: "/api/check/email/",
        data: { email: email },
        dataType: "json",
        success: function (response) {
          if (response.success == false) {
            $("[data-email-error]").attr("style", "visibility: visible");
            $("[data-email-error]").text(response.msg);
            $('[data-signup-form="step-1"]').removeClass("signup-submit-email");
          } else {
            $('[data-signup-form="step-1"]').addClass("signup-submit-email");
            $("[data-email-error]").attr("style", "visibility: hidden");
          }
        },
        error: function (error) {
          var error_data = JSON.parse(error.responseText);
          $('[data-signup-form="step-1"]').removeClass("signup-submit-email");
          $("[data-email-error]").attr("style", "visibility: visible");
        },
      });
    } else {
      $("[data-email-error]").text("Please Enter Valid Email ID");
      $("[data-email-error]").attr("style", "visibility: visible");
    }
});
  $("[data-check-mobile]").keyup(function () {
    var mobile = $("[data-check-mobile]").val();

    if (validateMobile(mobile)) {
      $.ajax({
        type: "POST",
        url: "/api/check/mobile/",
        data: { mobile: mobile },
        dataType: "json",
        success: function (response) {
          if (response.success === false) {
            $("[data-mobile-error]").attr("style", "visibility: visible");
            $("[data-mobile-error]").text(response.msg);
            $('[data-signup-form="step-1"]').removeClass(
              "signup-submit-mobile"
            );
          } else {
            $('[data-signup-form="step-1"]').addClass("signup-submit-mobile");
            $("[data-mobile-error]").attr("style", "visibility: hidden");
          }
        },
        error: function (error) {
          var error_data = JSON.parse(error.responseText);
          $('[data-signup-form="step-1"]').removeClass("signup-submit-mobile");
          $("[data-mobile-error]").attr("style", "visibility: visible");
        },
      });
    } else {
      $("[data-mobile-error]").text("Please Enter Valid Mobile Number");
      $("[data-mobile-error]").attr("style", "visibility: visible");
    }

  });
$('.form-check').click(function () {
  if($('#flexCheckDefault').is(':checked')){
      $("#agreeCheck").attr("style", "visibility: hidden");
      $('[data-signup-form="step-1"]').addClass("signup-submit-checkbox");
  } else {
      $("#agreeCheck").attr("style", "visibility: visible");
      $('[data-signup-form="step-1"]').removeClass("signup-submit-checkbox");
  }
});

  $('[data-step-button="1"]').click(function () {
    if (
      $('[data-signup-form="step-1"]').hasClass("signup-submit-email") &&
      $('[data-signup-form="step-1"]').hasClass("signup-submit-mobile") &&
      $('[data-signup-form="step-1"]').hasClass("signup-submit-checkbox") 
    ) {
      $(".main-loader").show();
      setTimeout(function () {
        $(".main-loader").hide();
      }, 2000);
      $('[data-signup-form="step-1"]').fadeOut();
      countdown();
      $("#agreeCheck").attr("style", "visibility: visible");
      $('[data-signup-form="step-2"]').fadeIn();
    } else {
      // $("#agreeCheck").attr("style", "visibility: visible");
      $('[data-signup-form="step-1"]').removeClass("signup-submit");
    }
    
  });


  $("[data-signup-form]").on("submit", function (e) {
    e.preventDefault();
    e.stopPropagation();
    $(".main-loader").show();

    var formdata = new FormData($(this)[0]);
    var href = $(this).attr("action");
    $.ajax({
      type: "POST",
      url: href,
      data: formdata,
      dataType: "json",
      processData: false,
      contentType: false,
      success: function (data) {
        console.log(data);
        if (data.status === false) {
          $(".main-loader").hide();
          $("#otpHelp").attr("style", "visibility: visible");
          $("[data-mobile-error]").text(data.message);
          $("[data-signup-resend-otp]").show();
        } else {
          $(".main-loader").hide();
          $("#otpHelp").attr("style", "visibility: hidden");
          if (data.is_rne === true) {
            if (
              window.location.pathname == "/signup-dra/" ||
              window.location.pathname == "/signup-dra/" ||
              window.location.pathname == "/homepage/"
            ) {
              localStorage.clear();
              window.location = "/accountrejected";
            } else if (
              window.location.pathname == "/signup-corporate/" ||
              window.location.pathname == "/signup-corporate"
            ) {
              localStorage.clear();
              window.location = "/corporate";
            } else {
              $("#otpHelp").attr("style", "visibility: hidden");
            }
          }
          if (data.is_dra === false) {
            if (
              window.location.pathname == "/signup-dra/" ||
              window.location.pathname == "/signup-dra/" ||
              window.location.pathname == "/homepage/"
            ) {
              localStorage.setItem("access-token", data.token.access);
              $("#verify_demat_account").modal("show");
            } else if (
              window.location.pathname == "/signup-corporate/" ||
              window.location.pathname == "/signup-corporate"
            ) {
              localStorage.setItem("access-token", data.token.access);
              window.location = "/corporate";
            } else {
              $("#otpHelp").attr("style", "visibility: hidden");
            }
          } else {
            if (
              window.location.pathname == "/signup-dra/" ||
              window.location.pathname == "/signup-dra/" ||
              window.location.pathname == "/homepage/"
            ) {
              localStorage.setItem("access-token", data.token.access);
              window.location = "/thankyou";
            } else if (
              window.location.pathname == "/signup-corporate/" ||
              window.location.pathname == "/signup-corporate"
            ) {
              localStorage.setItem("access-token", data.token.access);
              window.location = "/corporate";
            } else {
              $("#otpHelp").attr("style", "visibility: hidden");
            }
          }
        }
      },
      error: function (err) {
        if (err.responseJSON.status === false) {
          $(".main-loader").hide();
          $("#otpHelp").attr("style", "visibility: visible");
          $("[data-mobile-error]").text(err.responseJSON.message);
          $("[data-signup-resend-otp]").show();
        }
      },
    });
  });
  function countdown() {
    var seconds = 60;
    function tick() {
      var counter = document.getElementById("counter");
      seconds--;
      counter.innerHTML = "0:" + (seconds < 10 ? "0" : "") + String(seconds);
      if (seconds > 0) {
        setTimeout(tick, 1000);
      } else {
        document.getElementById("counter").innerHTML = `
                    <span class="resend-btn orange-color cursor-pointer">Resend</span>
            `;
        seconds = 60;
        //   document.getElementById("counter").innerHTML = "";
      }
    }
    tick();
  }

  $("#counter").on("click", ".resend-btn", function (e) {
    // $(".main-loader").show();

    e.preventDefault();
    mobileInput = $("[data-check-mobile]").val();
    console.log(mobileInput);
    $.ajax({
      type: "POST",
      url: "/api/resend/verification-code/",
      data: { mobile: mobileInput },
      success: function (response) {
        countdown();
        // console.log("this is working");
        // $(".main-loader").hide();
        // toastr.success('Verified Successfully');
      },
      error: function (error) {
        // var error_data = JSON.parse(error.responseText);
        console.log("error");
        // $(".main-loader").hide();
        // toastr.error('Bad Request')
      },
    });
  });

  $("[data-signup-resend-otp]").on("click", function (e) {
    $(".main-loader").show();
    e.preventDefault();
    mobileInput = $("[data-check-mobile]").val();
    console.log(mobileInput);
    $.ajax({
      type: "POST",
      url: "/api/send/otp/",
      data: { mobile: mobileInput },
      success: function (response) {
        $(".main-loader").hide();
        // toastr.success('Verified Successfully');
      },
      error: function (error) {
        var error_data = JSON.parse(error.responseText);
        $(".main-loader").hide();
        // toastr.error('Bad Request')
      },
    });
  });
  $("[data-other-platform]").slideUp();

  //   other platform api  click

  $("[data-other-platform-tab]").on("click", function (e) {
    $(".main-loader").show();
    $("[data-other-platform]").slideDown();
    $("#socialPlatform").attr("disabled", false);
    $.ajax({
      url: "/api/platform",
      type: "GET",
      dataType: "json",
      success: function (res, textStatus, xhr) {
        $(".main-loader").hide();
        var jsonObj = res.data;
        $("select#socialPlatform").html("");
        for (var i = 0; i < jsonObj.length; i++) {
          $("<option />")
            .val(jsonObj[i].name)
            .text(jsonObj[i].name)
            .appendTo($("select#socialPlatform"));

          $(".account-type-label").addClass("label-active");
          $("#socialPlatform").prop("required", "true");
        }
      },
      error: function (xhr, textStatus, errorThrown) {
        // toastr.error("Bad Request");
      },
    });
  });

  //   ends here

  // other social api call here
  $("[data-social]").on("click", function (e) {
    $(this).data("clicked", true);
    if (!$(this).data("clicked")) {
      $("[data-other-platform]").slideUp();
    } else {
      $("[data-other-platform]").slideDown();
    }
    var getSocial = $(this).data("social");
    $("select#socialPlatform").html("");
    console.log(getSocial);
    $("<option />")
      .val(getSocial)
      .text(getSocial)
      .appendTo($("select#socialPlatform"));
    $("#socialPlatform").attr("disabled", true);
    $(".account-type-label").addClass("label-active");
  });
  // ends here
  // social media page form submit

  $("[data-other-platform]").on("submit", function (e) {
    e.preventDefault();
    e.stopPropagation();
    $(".main-loader").show();
    var account = $("#account").val();
    var followers = $("#followers").val();
    var accountType = $("#socialPlatform").val();
    var href = $(this).attr("action");
    $.ajax({
      type: "POST",
      url: href,
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization: "Bearer " + localStorage.getItem("access-token"),
      },
      data: {
        account_type: accountType,
        account_id: account,
        followers: followers,
      },

      success: function (response) {
        if (response.data === null) {
          $("#back_to_other_account").modal("show");
        }
        if (response.data.followers < response.data.minimum_allowed) {
          $("#back_to_other_account").modal("show");
        } else {
          if (response.isDRA === false) {
            $("#verify_demat_account").modal("show");
          } else {
            window.location.href = "/thankyou";
          }
        }
        if (response.status === true) {
          $(".main-loader").hide();
          localStorage.clear();
        }
      },
      error: function (err) {},
    });
  });

  // ends here

  $(".form-control").on("change blur", function (e) {
    if (!this.value) {
      $(this).parent(".form-group").find(".text-danger").addClass("error");
      $(this)
        .parent(".form-group")
        .find(".form-control-placeholder")
        .removeClass("valid-label");
    } else {
      $(this).parent(".form-group").find(".text-danger").removeClass("error");
      $(this)
        .parent(".form-group")
        .find(".form-control-placeholder")
        .addClass("valid-label");
    }
  });

  // corporate page submit
  $("[data-corporate-form]").on("submit", function (e) {
    e.preventDefault();
    e.stopPropagation();
    $(".main-loader").show();
    console.log("this is here too");
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
        if (response.status === null) {
          $("#back_to_other_account").modal("show");
          $(".main-loader").hide();
        }
        if (response.data.followers < response.data.minimum_allowed) {
          $("#back_to_other_account").modal("show");
          $(".main-loader").hide();
        } else {
          if (response.isDRA === false) {
            $("#verify_demat_account").modal("show");
            $(".main-loader").hide();
          } else {
            $(".main-loader").hide();
            window.location.href = "/thankyou";
          }
        }
        if (response.status === true) {
          $(".main-loader").hide();
          localStorage.clear();
        }
      },
      error: function (err) {
        console.log("this is in error");
      },
    });
  });

  // $('[data-step-button="2"]').click(function(){
  //     $(".main-loader").show();
  //     setTimeout(function() {
  //         $(".main-loader").hide();
  //     }, 2000);
  //     $('[data-signup-form="step-1"]').fadeOut();
  //     $('[data-signup-form="step-2"]').fadeOut();
  //     $('[data-signup-form="step-3"]').fadeIn();
  // });

  $(".otp").keyup(function () {
    var otp1 = $(".otp-1").val();
    var otp2 = $(".otp-2").val();
    var otp3 = $(".otp-3").val();
    var otp4 = $(".otp-4").val();
    var otp5 = $(".otp-5").val();
    var otp6 = $(".otp-6").val();
    var otp = otp1 + otp2 + otp3 + otp4 + otp5 + otp6;
    $("#mobile_verification_code").val(otp);
  });



  // tnc page
  $("[data-tnc]").on("click", function (e) {
    $(".main-loader").show();

    $.ajax({
      url: "/api/term-condition/agree/",
      type: "POST",
      dataType: "json",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization: "Bearer " + localStorage.getItem("access-token"),
      },
      data: { is_agreed: true },
      success: function (data) {
        if (data.status === false) {
        } else {
          window.location = "/";
        }
      },
      error: function (xhr, textStatus, errorThrown) {
        //  window.location = "/";
      },
    });
  });
})(window.jQuery);

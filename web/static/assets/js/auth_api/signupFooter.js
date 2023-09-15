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

  $("[data-check-username-footer]").on("change", function (e) {
    var href = "/api/check/username/";
    var username = $("#name-footer").val();
    // $("#nameHelp-footer").attr("style", 'visibility: visible');
    if (username != "") {
      $.ajax({
        type: "POST",
        url: href,
        data: { username: username },
        dataType: "json",
        success: function (response) {
          $("#nameHelp-footer").attr("style", "visibility: hidden");
        },
        error: function (error) {
          var error_data = JSON.parse(error.responseText);
          $("#nameHelp-footer").attr("style", "visibility: visible");
        },
      });
    }
  });
$("[data-check-mobile-footer]").keyup(function () {
    var mobile = $("[data-check-mobile-footer]").val();
    if (validateMobile(mobile)) {
      $.ajax({
        type: "POST",
        url: "/api/check/mobile/",
        data: { mobile: mobile },
        dataType: "json",
        success: function (response) {
          if (response.success === false) {
            $("[data-mobile-error-footer]").attr(
              "style",
              "visibility: visible"
            );
            $("[data-mobile-error-footer]").text(response.msg);
            $('[data-signup-form-footer="step-1"]').removeClass(
              "signup-submit-mobile"
            );
          } else {
            $('[data-signup-form-footer="step-1"]').addClass(
              "signup-submit-mobile"
            );
            $("[data-mobile-error-footer]").attr("style", "visibility: hidden");
          }
        },
        error: function (error) {
          var error_data = JSON.parse(error.responseText);
          $('[data-signup-form-footer="step-1"]').removeClass(
            "signup-submit-mobile"
          );
          $("[data-mobile-error-footer]").attr("style", "visibility: visible");
        },
      });
    } else {
      $("[data-mobile-error-footer]").text("Please Enter Valid Mobile Number");
      $("[data-mobile-error-footer]").attr("style", "visibility: visible");
    }
});

  $("[data-check-email-footer]").keyup(function () {
    var email = $("[data-check-email-footer]").val();

    if (validateEmail(email)) {
      $.ajax({
        type: "POST",
        url: "/api/check/email/",
        data: { email: email },
        dataType: "json",
        success: function (response) {
          if (response.success == false) {
            $("[data-email-error-footer]").attr("style", "visibility: visible");
            $("[data-email-error-footer]").text(response.msg);
            $('[data-signup-form-footer="step-1"]').removeClass(
              "signup-submit-email"
            );
          } else {
            $('[data-signup-form-footer="step-1"]').addClass(
              "signup-submit-email"
            );
            $("[data-email-error-footer]").attr("style", "visibility: hidden");
          }
        },
        error: function (error) {
          var error_data = JSON.parse(error.responseText);
          $('[data-signup-form-footer="step-1"]').removeClass(
            "signup-submit-email"
          );
          $("[data-email-error-footer]").attr("style", "visibility: visible");
        },
      });
    } else {
      $("[data-email-error-footer]").text("Please Enter Valid Email ID");
      $("[data-email-error-footer]").attr("style", "visibility: visible");
    }
  });

  // $(".form-check").click(function () {
  //   if ($("#flexCheckDefault").is(":checked")) {
  //     $("#agreeCheck").attr("style", "visibility: hidden");
  //     $('[data-signup-form-footer="step-1"]').addClass(
  //       "signup-submit-checkbox"
  //     );
  //   } else {
  //     $("#agreeCheck").attr("style", "visibility: visible");
  //     $('[data-signup-form-footer="step-1"]').removeClass(
  //       "signup-submit-checkbox"
  //     );
  //   }
  // });

  $('[data-step-button-footer="1"]').click(function () {
    if (
      $('[data-signup-form-footer="step-1"]').hasClass("signup-submit-email") &&
      $('[data-signup-form-footer="step-1"]').hasClass("signup-submit-mobile")
    ) {
      $(".main-loader").show();
      setTimeout(function () {
        $(".main-loader").hide();
      }, 2000);
      $('[data-signup-form-footer="step-1"]').fadeOut();
      secondCountdown();
      // $("#agreeCheck").attr("style", "visibility: visible");
      $('[data-signup-form-footer="step-2"]').fadeIn();
    } else {
      // $("#agreeCheck").attr("style", "visibility: visible");
      $('[data-signup-form-footer="step-1"]').removeClass("signup-submit");
    }
  });

  $("[data-signup-form-footer ]").on("submit", function (e) {
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
        if (data.status === false) {
          $(".main-loader").hide();
          $("#otpHelp-footer").attr("style", "visibility: visible");
          $("[data-mobile-error-footer]").text(data.message);
          $("[data-signup-resend-otp]").show();
        } else {
          $(".main-loader").hide();
          $("#otpHelp-footer").attr("style", "visibility: hidden");
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
              $("#otpHelp-footer").attr("style", "visibility: hidden");
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
              $("#otpHelp-footer").attr("style", "visibility: hidden");
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
              $("#otpHelp-footer").attr("style", "visibility: hidden");
            }
          }
        }
      },
      error: function (err) {
        if (err.responseJSON.status === false) {
          $(".main-loader").hide();
          $("#otpHelp-footer").attr("style", "visibility: visible");
          $("[data-mobile-error-footer]").text(err.responseJSON.message);
          $("[data-signup-resend-otp]").show();
        }
      },
    });
  });
  function secondCountdown() {
    var seconds = 60;
    function tick() {
      var counter = document.getElementById("counter-footer");
      seconds--;
      counter.innerHTML = "0:" + (seconds < 10 ? "0" : "") + String(seconds);
      if (seconds > 0) {
        setTimeout(tick, 1000);
      } else {
        document.getElementById("counter-footer").innerHTML = `
                    <span class="resend-btn orange-color cursor-pointer">Resend</span>
            `;
        seconds = 60;
        //   document.getElementById("counter").innerHTML = "";
      }
    }
    tick();
  }

  $("#counter-footer").on("click", ".resend-btn", function (e) {
    // $(".main-loader").show();

    e.preventDefault();
    mobileInput = $("[data-check-mobile-footer]").val();
    $.ajax({
      type: "POST",
      url: "/api/resend/verification-code/",
      data: { mobile: mobileInput },
      success: function (response) {
        secondCountdown();
      },
      error: function (error) {
        // var error_data = JSON.parse(error.responseText);
      },
    });
  });

  $("[data-signup-resend-otp]").on("click", function (e) {
    $(".main-loader").show();
    e.preventDefault();
    mobileInput = $("[data-check-mobile-footer]").val();
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

  $(".otp-footer").keyup(function () {
    var otp1 = $(".otp-1-footer").val();
    var otp2 = $(".otp-2-footer").val();
    var otp3 = $(".otp-3-footer").val();
    var otp4 = $(".otp-4-footer").val();
    var otp5 = $(".otp-5-footer").val();
    var otp6 = $(".otp-6-footer").val();
    var otp = otp1 + otp2 + otp3 + otp4 + otp5 + otp6;
    $("#mobile_verification_code-footer").val(otp);
  });
})(window.jQuery);

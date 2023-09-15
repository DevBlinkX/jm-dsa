(function ($) {
  // $(".error").css('visiblity', 'hidden');
  $(".error").attr("style", 'visibility: hidden');

  const validateEmail = (email) => {
    return email.match(
      /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    );
  };


  // login mobile-number-step
  $("[data-login-rm-form]").on("submit", function (e) {
    $(".main-loader").show();
    e.preventDefault();
    e.stopPropagation();

    var form = new FormData($(this)[0]);
    var email = $("[data-email-value]").val();
    var href = $(this).attr("action");

    $.ajax({
      type: "POST",
      url: href,
      headers: {},
      data: {
        email: email,
      },
      success: function (data) {
        $(".getLoginId").text(email);
        if (data.status === false) {
          $("[data-email-error]").attr("style", 'visibility: visible');
          $("[data-email-error]").text(data.msg);
          $(".main-loader").hide();
        } else {
          $("#eEmailId").val($("[data-email-value]").val());
          $(".main-loader").hide();
          $(".login-page").addClass("hidden");
          $(".otp-page").removeClass("hidden");
        }
      },
      error: function (error) {
        var error_data = JSON.parse(error.responseText);
        $(".main-loader").hide();
        $("[data-email-error]").attr("style", 'visibility: visible');
        $("[data-email-error]").text(error_data.msg);
      },
    });
  });
  // ends here

  // check session

  function loginSession(e) {
    $.ajax({
      type: "POST",
      url: "/api/session/login/",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization: "Bearer " + localStorage.getItem("access-token"),
      },
      success: function (data) {
        if (data.status === false) {
        } else {
          window.location = "/";
        }
      },
      error: function (error) {
        var error_data = JSON.parse(error.responseText);
      },
    });
  }

  // login otp-submit-step
  $("[data-otp-rm-form]").on("submit", function (e) {
    e.preventDefault();
    e.stopPropagation();
    $(".main-loader").show();
    var href = $(this).attr("action");
    var otp1 = $(".otp-1").val();
    var otp2 = $(".otp-2").val();
    var otp3 = $(".otp-3").val();
    var otp4 = $(".otp-4").val();
    var otp5 = $(".otp-5").val();
    var otp6 = $(".otp-6").val();
    var otp = otp1 + otp2 + otp3 + otp4 + otp5 + otp6;
    var email = $("#eEmailId").val();
    if (otp.length == 6) {
      $.ajax({
        type: "POST",
        url: href,
        headers: {},
        data: {
          code: otp,
          email: email,
        },
        success: function (data) {
          if (data.status == false) {
            $("#otpHelp").attr("style", 'visibility: visible');
            $(".main-loader").hide();
          } else {
            $("#otpHelp").attr("style", 'visibility: hidden');
            $(".main-loader").hide();
            localStorage.setItem("access-token", data.data.access);
            loginSession();
          }
        },
        error: function (error) {
          var error_data = JSON.parse(error.responseText);

          $("#otpHelp").attr("style", 'visibility: visible');
          $(".main-loader").hide();
        },
      });
    }
  });
  // ends here

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
        // toastr.error("Bad Request");
      },
    });
  });
})(window.jQuery);

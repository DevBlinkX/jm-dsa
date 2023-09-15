from django.urls import path
from account.views import UserView, PlatformsView


urlpatterns = [
    path('check/email/', UserView.as_view({'post': 'check_email'})),
    path('check/mobile/', UserView.as_view({'post': 'check_mobile'})),
    path('check/username/', UserView.as_view({'post': 'check_username'})),

    # e sign verification
    # path('send/esign/otp/', UserView.as_view({'post': 'resend_mobile_verification_code'})),
    # path('esign/verification/', UserView.as_view({'post': 'verify_mobile_new'})),

    # path('login/', UserView.as_view({'post': 'login'}), name="login_api"),
    path('send/otp/', UserView.as_view({'post': 'send_login_otp'}), name="send_login_otp"),
    path('login/otp/', UserView.as_view({'post': 'login_with_otp'}), name="login_with_otp"),
    path('session/login/', UserView.as_view({'post': 'session_login'})),

    path('resend/verification-code/', UserView.as_view({'post': 'resend_mobile_verification_code'})),
    path('signup/', UserView.as_view({'post': 'signup'})),
    path('update/corporate/', UserView.as_view({'post': 'add_corporate_data'})),
    path('channel/save/', UserView.as_view({'post': 'save_channel_detail'})),
    path('check/followers/', UserView.as_view({'post': 'check_followers_status'})),

    # path('get/instagram-details/', UserView.as_view({'post': 'get_instagram_details'})),
    # path('get/facebook/page/detail/', UserView.as_view({'post': 'get_facebook_page_detail'})),
    # path('get/facebook/instagram/detail/', UserView.as_view({'post': 'get_facebook_instagram_detail'})),
    # path('get/youtube/account/detail/', UserView.as_view({'post': 'get_youtube_account_detail'})),


    # path('get/subscribers/',UserView.as_view({'post':'get_subscribers_details'}),name="subscribers"),
    path('profile/', UserView.as_view({'get': 'profile'})),
    path('profile/update/', UserView.as_view({'post': 'profile_update'})),
    # path('password/change/', UserView.as_view({'post': 'change_password'})),
    path('bankdetail/update/', UserView.as_view({'post': 'update_bank_detail'})),
    path('term-condition/agree/', UserView.as_view({'post': 'agree_to_term_and_condition'})),

    path('request/callback/', UserView.as_view({'post': 'request_call_back'})),
    path('create/shorturl/', UserView.as_view({'post': 'create_short_url'})),


    path('platform/', PlatformsView.as_view()),
    path('platform/<int:pk>/', PlatformsView.as_view()),
]

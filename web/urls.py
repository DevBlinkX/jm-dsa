from django.urls import path, include
from django.contrib.auth.decorators import login_required
from web.views import *

urlpatterns = [
    path('select-user/', select_user, name='select-user'),
    path('', home_page, name='home-page'),
    path('signup-dsa/', signup_dra, name='signup-dra'),
    path('signup-corporate/', signup_corporate, name='signup-corporate'),

    path('login/', login, name='login'),
    path('login/rm/', login_rm, name='login-rm'),
    path('logout/', logout_view, name='logout'),
    path('otp/', otp, name='otp'),
    path('corporate/', corporate, name='corporate'),
    path('social-media/', social_media, name='social-media'),
    path('thankyou/', thankyou, name='thankyou'),
    path('homepage/', indexPage, name='homepage'),
    path('landing/', landingPage, name='landing'),
    
    path('accountrejected/', accountrejected, name='accountrejected'),
    path('terms-and-conditions/', terms_and_conditions, name='terms-and-conditions'),

    
    # DRA dashboard
    path('dra-overview/', dra_overview, name='dra-overview'),
    path('dra-activated/', dra_activated, name='dra-activated'),
    path('dra-leads/', dra_leads, name='dra-leads'),
    path('dra-profile/', dra_profile, name='dra-profile'),
    path('dra-payout/', dra_payout, name='dra-payout'),
    path('dra-leaderboard/', dra_leaderboard, name='dra-leaderboard'),
    path('dra-knowledge-center/', dra_knowledge_center, name='dra-knowledge-center'),
    path('dra-knowledge-center-details/', dra_knowledge_center_details, name='dra-knowledge-center-details'),
    path('dra-help/', dra_help, name='dra-help'),
    path('dra-earning/', dra_earning, name='dra-earning'),
    # Download repors urls
    path('dra/downloads/payout/', download_pauout_details, name='dra-download-pauout-details'),
    path('dra/downloads/settlements/', download_settlements, name='dra-download-settlement-details'),
    path('dra/downloads/tds/', download_tds_certificate, name='dra-download-tds-certificate'),

    # RM dashboard
    path('rm-overview/', rm_overview, name='rm-overview'),
    path('rm-activated/', rm_activated, name='rm-activated'),
    path('rm-leads/', rm_leads, name='rm-leads') ,
    path('rm-payout/', rm_payout, name='rm-payout'),
    path('rm-settlements/', rm_settlements, name='rm-settlements'),
    path('rm-opportunities/', rm_opportunities, name='rm-opportunities'),
    path('rm-signup/', rm_signup, name='rm-signup'),
    path('rm-help/', rm_help, name='rm-help'),

    # Download RM reports

    # DSA dashboard
    path('dsa-overview/', dsa_overview, name='dsa-overview'),
    path('dsa-leads/', dsa_leads, name='dsa-leads'),
    path('dsa-profile/', dsa_profile, name='dsa-profile'),
    path('dsa-payout/', dsa_payout, name='dsa-payout'),
    path('dsa-leaderboard/', dsa_leaderboard, name='dsa-leaderboard'),
    path('dsa-knowledge-center/', dsa_knowledge_center, name='dsa-knowledge-center'),
    path('dsa-knowledge-center-details/', dsa_knowledge_center_details, name='dsa-knowledge-center-details'),
    path('dsa-help/', dsa_help, name='dsa-help'),
    path('dsa-earning/', dsa_earning, name='dsa-earning'),
    path('dsa/downloads/payout/', download_pauout_details, name='dsa-download-pauout-details'),
    path('dsa/downloads/settlements/', download_settlements, name='dsa-download-settlement-details'),
    path('dsa/downloads/tds/', download_tds_certificate, name='dsa-download-tds-certificate'),
    
    # rmj dashboard
    path('rmj-overview/', rmj_overview, name='rmj-overview'),
    path('rmj-leads/', rmj_leads, name='rmj-leads'),
    path('rmj-profile/', rmj_profile, name='rmj-profile'),
    path('rmj-payout/', rmj_payout, name='rmj-payout'),
    path('rmj-help/', rmj_help, name='rmj-help'),
    path('rmj/downloads/payout/', download_pauout_details, name='rmj-download-pauout-details'),
    path('rmj/downloads/settlements/', download_settlements, name='rmj-download-settlement-details'),
    path('rmj/downloads/tds/', download_tds_certificate, name='rmj-download-tds-certificate'),
]

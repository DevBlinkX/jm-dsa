from django.urls import path,include
from core.api_views import *



urlpatterns = [
    path('dsa/overview/', DashbardView.as_view({'get': 'get_overview'})),
    path('dsa/overview/banner/', BanerView.as_view({'get': 'get_latest_banner'})),
    path('dsa/overview/leads/', DashbardView.as_view({'get': 'get_leads'})),
    path('dsa/overview/conversion/', DashbardView.as_view({'get': 'get_conversion'})),
    path('dsa/overview/app-downloads/', DashbardView.as_view({'get': 'get_app_downloads'})),
    path('dsa/overview/total-lead/', DashbardView.as_view({'get': 'get_total_mandates'})),
    path('dsa/overview/conversion-stage/', DashbardView.as_view({'get': 'get_conversion_stage'})),
    path('dsa/overview/brokerage/', DashbardView.as_view({'get': 'get_brokerage'})),
    path('dsa/overview/incentive/', DashbardView.as_view({'get': 'get_incentive'})),
    
    path('dsa/overview/successful-rate/', DashbardView.as_view({'get': 'get_successful_rate'})),
    path('dsa/overview/successful-disbursed/', DashbardView.as_view({'get': 'get_successful_disbursed'})),

    path('dsa/overview/total-payout-earned/', DashbardView.as_view({'get': 'get_total_brokerage_and_incentive'})),

    path('dsa/leads/', DRALeadsView.as_view()),
    path('dsa/leads/remind/', DashbardView.as_view({'post': 'send_leads_reminder'})),
    path('dsa/add-leads/', DRA_Add_LeadsView.as_view({'post':'create_Lead'})),
    path('dsa/add-share-leads/',DRA_Add_share_LeadsView.as_view({'post':'create_share_Lead'})),
    path('dsa/add-rmj/',RMJ_Add.as_view({'post':'create_rmj'})),
    path('dsa/leads/import/', Leadimport.as_view({'post':'import_data'})),

    path('dsa/trending/knowlage-center/', TrendingKnowlageCenter.as_view()),
    path('dsa/knowlage-center-list/', KnowlageCenterList.as_view()),
    path('dsa/knowlage-center-details/<str:slug>/', KnowlageCenterdetails.as_view({'get': 'retrive'})),
    path('dsa/knowlage-assets-list/<str:slug>/', KnowlageAssetsList.as_view({'get': 'retrive'})),
    path('dsa/category-list/', CategoryList.as_view()),
    path('dsa/tag-list/', TagsList.as_view()),
    path('dsa/activated/user-list/', DRAUserList.as_view()),

    path('dsa/rm-info/', RMInformationView.as_view()),

    path('dsa/leaderboard/broker-list/', DRA_BrokerList.as_view()),
    path('dsa/leaderboard/kyc-list/', DRAKycList.as_view()),
    path('dsa/leaderboard/total-earning-list/', DRA_TotalEarningList.as_view()),

    # path('dsa/get-referrals/', ReferralsList.as_view()),
    path('dsa/settlement-list/', SettlementList.as_view()),
    path('dsa/payout-page/', PayoutPage.as_view()),
    path('dsa/payout-info/', PayoutInfo.as_view()),


    path('dsa/financial-year/', TDSView.as_view({'get':'get_financial_year'})),
    path('dsa/segment/', TDSView.as_view({'get': 'get_segments'})),
    path('dsa/get/quarters/', TDSView.as_view({'get': 'get_quarters'})),
    path('dsa/download/tds/', TDSView.as_view({'post': 'download_tds'})),

    path('rmj/overview/broker-list/', RM_BrokerList.as_view()),
    path('rmj/overview/kyc-list/', RMKycList.as_view()),
    path('rmj/overview/referrals/', ReferralsList.as_view()),
    path('rmj/signup/list/', RMSignUpList.as_view()),
    path('rmj/dsa/signup/', RMSignupView.as_view({'post': 'update_user_incentive_percentage'})),
    path('rmj-activated/', RMActivatedUserList.as_view()),
    path('rmj-opportunities/', RMOpportunities.as_view()),
    path('rmj-leads/', RMLeadsView.as_view()),
    path('rmj/add-leads/', RMJ_Add_LeadsView.as_view({'post':'create_Lead'})),

    path('rmj/leads/import/', LeadRMimport.as_view({'post':'import_data'})),
    path('rmj-payout/', RMPayout.as_view()),
    path('rmj-settlements/', RMSettlement.as_view()),
    path('rmj-payout/', RMPayout.as_view()),
 
    # RM dashboard overview api
    path('rmj/overview/', RMDashbardView.as_view({'get': 'get_overview'})),
    path('rmj/overview/leads/', RMDashbardView.as_view({'get': 'get_leads'})),
    path('rmj/overview/conversion/', RMDashbardView.as_view({'get': 'get_conversion'})),
    path('rmj/overview/app-downloads/', RMDashbardView.as_view({'get': 'get_app_downloads'})),
    path('rmj/overview/total-lead/', RMDashbardView.as_view({'get': 'get_total_mandates'})),
    path('rmj/overview/conversion-stage/', RMDashbardView.as_view({'get': 'get_conversion_stage'})),
    path('rmj/overview/brokerage/', RMDashbardView.as_view({'get': 'get_brokerage'})),
    path('rmj/overview/incentive/', RMDashbardView.as_view({'get': 'get_incentive'})),

    path('rmj/overview/successful-rate/', RMDashbardView.as_view({'get': 'get_successful_rate'})),
    path('rmj/overview/successful-disbursed/', RMDashbardView.as_view({'get': 'get_successful_disbursed'})),

    path('get-keyword-list/', KeywordList.as_view()),
    path('get/rmj/detail/', RMDetailView.as_view({'post': 'get_rm_details'})),
    path('faq/', faq_view.as_view({'get': 'get_faq'})),

    # RM opportunities tabs API 
    path('rmj/opportunities/tabs/lead/generation/', RMOpportunitiesTabs.as_view({'get': 'get_dra_inactive_lead_generation'})),
    path('rmj/opportunities/tabs/account/activation/', RMOpportunitiesTabs.as_view({'get': 'get_dra_inactive_account_activation'})),
    path('rmj/opportunities/tabs/brokerage/generation/', RMOpportunitiesTabs.as_view({'get': 'get_dra_inactive_brokerage_generation'})),
    path('rmj/opportunities/tabs/downfall/account/activation/', RMOpportunitiesTabs.as_view({'get': 'get_dra_downfall_account_activation'})),
    path('rmj/opportunities/tabs/downfall/brokerage/generation/', RMOpportunitiesTabs.as_view({'get': 'get_dra_downfall_brokerage_generation'})),
    path('rmj/opportunities/tabs/degrowth/leads/', RMOpportunitiesTabs.as_view({'get': 'get_dra_degrowth_lead'})),
]



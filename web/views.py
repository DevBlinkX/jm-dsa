from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from account.decorators import has_dra_dashboard_access, has_rm_dashboard_access, has_dsa_dashboard_access,has_rmj_dashboard_access
import pandas as pd
import pdfkit
from account.models import TimingSlot

# Create your views here.


def home_page(request, **kwargs):
    if request.user.is_authenticated:
        if request.user.user_type=='rmj':
            return redirect('rmj-overview')
        if not request.user.is_aggre_term_condition:
            return redirect('terms-and-conditions')
        else:
            return redirect('dsa-overview')
    return render(request, 'web/auth/login.html.j2')
    # return render(request, 'web/base.html.j2')

def signup_dra(request, **kwargs):
    return render(request, 'web/auth/signup-dra.html.j2')

def signup_corporate(request, **kwargs):
    return render(request, 'web/auth/signup-corporate.html.j2')

def login(request, **kwargs):
    return render(request, 'web/auth/login.html.j2')


def logout_view(request, **kwargs):
    """
    logout session
    """
    logout(request)
    return redirect('/')

def otp(request, **kwargs):
    return render(request, 'web/auth/otp-verification.html.j2')

def social_media(request, **kwargs):
    return render(request, 'web/auth/social-media-step.html.j2')

def select_user(request, **kwargs):
    return render(request, 'web/auth/select-user.html.j2')

def corporate(request, **kwargs):
    return render(request, 'web/auth/corporate.html.j2')

def thankyou(request, **kwargs):
    return render(request, 'web/auth/thankyou.html.j2')

def indexPage(request, **kwargs):
    return render(request, 'web/index.html.j2')

def landingPage(request, **kwargs):
    return render(request, 'web/landing.html.j2')

def accountrejected(request, **kwargs):
    return render(request, 'web/auth/accountrejected.html.j2')


@login_required(login_url='/login/')
def terms_and_conditions(request, **kwargs):
    return render(request, 'web/auth/tnc.html.j2')


@login_required(login_url='/login/')
@has_dsa_dashboard_access
def dra_overview(request, **kwargs):
    context = {
        "page":'overview'
    }
    return render(request, 'web/dashboard/dra/overview.html.j2', context)

@login_required(login_url='/login/')
@has_dsa_dashboard_access
def dra_activated(request, **kwargs):
    context = {
        "page":'activated'
    }   
    return render(request, 'web/dashboard/dra/activated.html.j2', context)

@login_required(login_url='/login/')
@has_dsa_dashboard_access
def dra_leads(request, **kwargs):
    context = {
        "page":'leads'
    }
    return render(request, 'web/dashboard/dra/leads.html.j2', context)

@login_required(login_url='/login/')
@has_dsa_dashboard_access
def dra_knowledge_center(request, **kwargs):
    context = {
        "page":'knowledge_center'
    }
    return render(request, 'web/dashboard/dra/knowledge-center.html.j2', context)

@login_required(login_url='/login/')
@has_dsa_dashboard_access
def dra_leaderboard(request, **kwargs):
    context = {
        "page":'leaderboard'
    }
    return render(request, 'web/dashboard/dra/leaderboard.html.j2', context)

@login_required(login_url='/login/')
@has_dsa_dashboard_access
def dra_profile(request, **kwargs):
    context = {
        "page":'profile'
    }
    return render(request, 'web/dashboard/dra/profile.html.j2', context)

@login_required(login_url='/login/')
@has_dsa_dashboard_access
def dra_knowledge_center_details(request, **kwargs):
    context = {
        "page":'knowledge_center'
    }
    return render(request, 'web/dashboard/dra/knowledge-center-details.html.j2', context)

@login_required(login_url='/login/')
@has_dsa_dashboard_access
def dra_payout(request, **kwargs):
    context = {
        "page":'payout'
    }
    return render(request, 'web/dashboard/dra/payout.html.j2', context)

@login_required(login_url='/login/')
@has_dsa_dashboard_access
def dra_help(request, **kwargs):
    context = {
        "page":'help',
        "timing":TimingSlot.objects.all(),
    }
    return render(request, 'web/dashboard/dra/help.html.j2',context)

@login_required(login_url='/login/')
@has_dsa_dashboard_access
def dra_earning(request, **kwargs):
    context = {
        "page":'earning'
    }
    return render(request, 'web/dashboard/dra/earning.html.j2', context)

@login_required(login_url='/login/')
@has_rmj_dashboard_access
def rm_overview(request, **kwargs):
    context = {
        "page":'rmoverview'
    }
    return render(request, 'web/dashboard/rm/overview.html.j2', context)

@login_required(login_url='/login/')
@has_rmj_dashboard_access
def rm_activated(request, **kwargs):
    context = {
        "page":'rmactivated'
    }
    return render(request, 'web/dashboard/rm/activated.html.j2', context)

@login_required(login_url='/login/')
@has_rmj_dashboard_access
def rm_leads(request, **kwargs):
    context = {
        "page":'rmleads'
    }
    return render(request, 'web/dashboard/rm/leads.html.j2', context)

@login_required(login_url='/login/')
@has_rmj_dashboard_access
def rm_payout(request, **kwargs):
    context = {
        "page":'rmpayout'
    }
    return render(request, 'web/dashboard/rm/payout.html.j2', context)


@login_required(login_url='/login/')
@has_rmj_dashboard_access
def rm_settlements(request, **kwargs):
    context = {
        "page":'rmsettlements'
    }
    return render(request, 'web/dashboard/rm/settlements.html.j2', context)


@login_required(login_url='/login/')
@has_rmj_dashboard_access
def rm_opportunities(request, **kwargs):
    context = {
        "page":'rmopportunity'
    }
    return render(request, 'web/dashboard/rm/opportunities.html.j2', context)

@login_required(login_url='/login/')
@has_rmj_dashboard_access
def rm_signup(request, **kwargs):
    context = {
        "page":'rmsignup'
    }
    return render(request, 'web/dashboard/rm/signup.html.j2', context)

@login_required(login_url='/login/')
@has_rmj_dashboard_access
def rm_help(request, **kwargs):
    context = {
        "page":'rmhelp',
        "timing":TimingSlot.objects.all(),
    }
    return render(request, 'web/dashboard/rm/help.html.j2',context)


# Downloads views

@login_required(login_url='/login/')
@has_dsa_dashboard_access
def download_pauout_details(request, **kwargs):
    """
    download payout excel sheet
    """
    from core.dra_reports import get_report_data
    from core.models import Payout
    filename = "payout-logs"
    download_type = request.GET.get("download_type", 'xlsx')
    days = request.GET.get("days", '90')
    qs = Payout.objects.filter(dra=request.user)
    results = {
        "headers": ["Date", "Payment Mode", "Amount", "Status"],
        "data": [
            {
                "Date": i.date,
                "Payment Mode": i.payment_mode,
                "Amount": i.amount,
                "Status": i.status
            } for i in qs
        ]
    }
    kwargs = {
        "user": request.user
    }
    file_obj = get_report_data(results, **kwargs)
    if download_type == 'pdf':
        data = pd.read_excel(file_obj)
        html_cnt = '<div class="dataTables_wrapper">{data}</div>'
        raw_html_file = html_cnt.format(data=data.to_html(classes='dataTable').replace('<td>NaN</td>', ''))
        pdf = pdfkit.from_string(raw_html_file, False)
        # css='static/pdf_style.css'
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={filename}.pdf'
        return response
    else:
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={filename}.xlsx'
        response.write(file_obj.read())
        return response



@login_required(login_url='/login/')
@has_dsa_dashboard_access
def download_tds_certificate(request, **kwargs):
    """
    download payout excel sheet
    """
    from core.dra_reports import get_report_data
    from core.models import Payout
    filename = "payout-logs"
    download_type = request.GET.get("download_type", 'xlsx')
    days = request.GET.get("days", '90')
    qs = Payout.objects.filter(dra=request.user)
    results = {
        "headers": ["Date", "Payment Mode", "Amount", "Status"],
        "data": [
            {
                "Date": i.date,
                "Payment Mode": i.payment_mode,
                "Amount": i.amount,
                "Status": i.status
            } for i in qs
        ]
    }
    kwargs = {
        "user": request.user
    }
    file_obj = get_report_data(results, **kwargs)
    data = pd.read_excel(file_obj)
    html_cnt = '<div class="dataTables_wrapper">{data}</div>'
    raw_html_file = html_cnt.format(data=data.to_html(classes='dataTable').replace('<td>NaN</td>', ''))
    pdf = pdfkit.from_string(raw_html_file, False)
    # css='static/pdf_style.css'
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={filename}.pdf'
    return response


@login_required(login_url='/login/')
@has_dsa_dashboard_access
def download_settlements(request, **kwargs):
    """
    download settlements excel sheet
    """
    from core.dra_reports import get_report_data
    from core.models import Settlement
    filename = "Settlements"
    download_type = request.GET.get("download_type", 'xlsx')
    days = request.GET.get("days", '90')
    user = request.user
    qs = Settlement.objects.filter(dra=user).order_by('-created_at')

    results = {
        "headers": ["Month", "CONVERTED", "TRADE ACTIVE", "GROSS BROKERAGE", "INCENTIVE", "NET BROKERAGE", "TOTAL"],
        "data": [
            {
                "Month": f"{i.month} {i.year}",
                "CONVERTED": i.converted,
                "TRADE ACTIVE": i.trad_active,
                "GROSS BROKERAGE": i.gross_brokerage,
                "INCENTIVE": i.incentive,
                "NET BROKERAGE": i.net_brokerage,
                "TOTAL": i.total
            } for i in qs
        ]
    }
    kwargs = {
        "user": request.user
    }
    file_obj = get_report_data(results, **kwargs)
    if download_type == 'pdf':
        data = pd.read_excel(file_obj)
        html_cnt = '<div class="dataTables_wrapper">{data}</div>'
        raw_html_file = html_cnt.format(data=data.to_html(classes='dataTable').replace('<td>NaN</td>', ''))
        pdf = pdfkit.from_string(raw_html_file, False)
        # css='static/pdf_style.css'
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={filename}.pdf'
        return response
    else:
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={filename}.xlsx'
        response.write(file_obj.read())
        return response


def login_rm(request, **kwargs):
    return render(request, 'web/auth/login-rm.html.j2')



# DSA
@login_required(login_url='/login/')
@has_dsa_dashboard_access
def dsa_overview(request, **kwargs):
    context = {
        "page":'overview'
    }
    return render(request, 'web/dashboard/dsa/overview.html.j2', context)

@login_required(login_url='/login/')
@has_dsa_dashboard_access
def dsa_leads(request, **kwargs):
    context = {
        "page":'leads'
    }
    return render(request, 'web/dashboard/dsa/leads.html.j2', context)

@login_required(login_url='/login/')
@has_dsa_dashboard_access
def dsa_profile(request, **kwargs):
    context = {
        "page":'profile'
    }
    return render(request, 'web/dashboard/dsa/profile.html.j2', context)

@login_required(login_url='/login/')
@has_dsa_dashboard_access
def dsa_payout(request, **kwargs):
    context = {
        "page":'payout'
    }
    return render(request, 'web/dashboard/dsa/payout.html.j2', context)

@login_required(login_url='/login/')
@has_dsa_dashboard_access
def dsa_leaderboard(request, **kwargs):
    context = {
        "page":'leaderboard'
    }
    return render(request, 'web/dashboard/dsa/leaderboard.html.j2', context)

@login_required(login_url='/login/')
@has_dsa_dashboard_access
def dsa_knowledge_center(request, **kwargs):
    context = {
        "page":'knowledge-center'
    }
    return render(request, 'web/dashboard/dsa/knowledge-center.html.j2', context)

@login_required(login_url='/login/')
@has_dsa_dashboard_access
def dsa_knowledge_center_details(request, **kwargs):
    context = {
        "page":'knowledge-center-details'
    }
    return render(request, 'web/dashboard/dsa/knowledge-center-details.html.j2', context)

@login_required(login_url='/login/')
@has_dsa_dashboard_access
def dsa_help(request, **kwargs):
    context = {
        "page":'help',
        "timing":TimingSlot.objects.all(),
    }
    return render(request, 'web/dashboard/dsa/help.html.j2', context)

@login_required(login_url='/login/')
@has_dsa_dashboard_access
def dsa_earning(request, **kwargs):
    context = {
        "page":'earning'
    }
    return render(request, 'web/dashboard/dsa/earning.html.j2', context)


# RMJ
@login_required(login_url='/login/')
@has_rmj_dashboard_access
def rmj_overview(request, **kwargs):
    context = {
        "page":'overview'
    }
    return render(request, 'web/dashboard/rmj/overview.html.j2', context)

@login_required(login_url='/login/')
@has_rmj_dashboard_access
def rmj_leads(request, **kwargs):
    context = {
        "page":'leads'
    }
    return render(request, 'web/dashboard/rmj/leads.html.j2', context)

@login_required(login_url='/login/')
@has_rmj_dashboard_access
def rmj_profile(request, **kwargs):
    context = {
        "page":'profile'
    }
    return render(request, 'web/dashboard/rmj/profile.html.j2', context)

@login_required(login_url='/login/')
@has_rmj_dashboard_access
def rmj_payout(request, **kwargs):
    context = {
        "page":'payout'
    }
    return render(request, 'web/dashboard/rmj/payout.html.j2', context)

@login_required(login_url='/login/')
@has_rmj_dashboard_access
def rmj_help(request, **kwargs):
    context = {
        "page":'help'
    }
    return render(request, 'web/dashboard/rmj/help.html.j2', context)
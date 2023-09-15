from datetime import datetime, timedelta
from django.conf import settings
import os
import requests
import string
import random
from django.utils import timezone
import json
from account.models import User
from core.models import Leads, Incentive, Brokerage
from django.db.models.functions import ExtractMonth, ExtractYear
from django.db.models import Sum
import calendar
from account.utils import send_mail
from django.template.loader import get_template
from project.jinja2 import ampmtime, indian_date_format
import csv
from io import StringIO
from core.encryption import aes_encrypt, aes_decrypt

JMFL_EMAILS = ['AOTMIS@jmfl.com', 'fundsho@jmfl.com', 'softtest2@jmfl.com']
JMFL_EMAILS_CC = ["srijan@scaledesk.com", "milind.panchal@jmfl.com", 'javed@scaledesk.com']

LEAD_LOOKUP_VALUES = [
    "ProspectID",
    "FirstName",
    "LastName",
    "EmailAddress",
    "mx_Referred_DRA_Code",
    "mx_Client_Code", 
    "mx_DRA_Code",
    "mx_DIY_Stage",
    "Phone",
    "Source"
]


def update_dra_client_code(user):
    try:
        url = f"https://api-in21.leadsquared.com/v2/LeadManagement.svc/Leads.Get?accessKey={settings.LEAD_SQUARE_ACCESS_KEY}&secretKey={settings.LEAD_SQUARE_SECRET_KEY}"
        payload = {
            "Parameter": {
                    "LookupName": "mx_DRA_Code",
                    "LookupValue": user.dra_tag,
                    "SqlOperator": "="
                },
                "Columns": {
                    "Include_CSV": ",".join(LEAD_LOOKUP_VALUES)
                },
                "Sorting": {
                    "ColumnName": "CreatedOn",
                    "Direction": "1"
                },
                "Paging": {
                    "PageIndex": 1,
                    "PageSize": 100
                }
        }
        headers = {"Content-Type": "application/json"}
        res = requests.post(url, json=payload, headers=headers)
        res = res.json()
        if len(res) > 0:
            res = res[0]
            user.mx_client_code = res.get("mx_Client_Code")
            user.mx_referred_dra_code = res.get("mx_Referred_DRA_Code")
            user.mx_dra_code = res.get("mx_DRA_Code")
            user.prospect_id = res.get("ProspectID")
            user.save()
    except:
        pass



def get_all_leads():
    users = User.objects.filter(user_type='dra')
    try:
        url = f"https://api-in21.leadsquared.com/v2/LeadManagement.svc/Leads.Get?accessKey={settings.LEAD_SQUARE_ACCESS_KEY}&secretKey={settings.LEAD_SQUARE_SECRET_KEY}"
        for user in users:

            if user.dra_tag is None or user.dra_tag == "":
                continue

            # check for client code
            if not user.mx_client_code:
                update_dra_client_code(user)

            payload = {
                "Parameter": {
                        "LookupName": "mx_Referred_DRA_Code",
                        "LookupValue": user.dra_tag,
                        "SqlOperator": "="
                    },
                    "Columns": {
                        "Include_CSV": ",".join(LEAD_LOOKUP_VALUES)
                    },
                    "Sorting": {
                        "ColumnName": "CreatedOn",
                        "Direction": "1"
                    },
                    "Paging": {
                        "PageIndex": 1,
                        "PageSize": 100
                    }
            }
            headers = {"Content-Type": "application/json"}
            res = requests.post(url, json=payload, headers=headers)
            res = res.json()
            for r in res:
                is_created = False
                try:
                    ll = Leads.objects.get(
                            mx_client_code=r.get("mx_client_code"),
                            phone=r.get("Phone"),
                            email=r.get("EmailAddress"),
                            prospect_id=r.get("ProspectID")
                        )
                except:
                    is_created = True
                    ll = Leads(dra=user)
                    ll.email = r.get("EmailAddress")
                    ll.phone = r.get("Phone")
                    ll.mx_client_code = r.get("mx_Client_Code")
                    ll.lsq_created_on = r.get("CreatedOn")

                ll.first_name = r.get("FirstName")
                ll.last_name = r.get("LastName")
                ll.prospect_id = r.get("ProspectID")
                ll.mx_client_code = r.get("mx_Client_Code")
                ll.mx_dra_code = r.get("mx_DRA_Code")
                ll.mx_referred_dra_code = r.get("mx_Referred_DRA_Code")
                ll.source = r.get("Source")
                ll.source_medium = r.get("SourceMedium")
                ll.source_campaign = r.get("SourceCampaign")
                ll.mx_diy_stage = r.get("mx_DIY_Stage")
                ll.save()

                if is_created:
                    # if new lead, create incentiav entree
                    inc = Incentive(
                        dra=user,
                        lead=ll,
                        incentive_amount=user.incentive_perlead
                    )
                    inc.save()
                is_created = False
            # update total kyc
            user.total_kyc = user.my_leads.count()
            user.save()
    except Exception as e:
        return False, False



def calculate_settlements():
    pass


def get_brokarage_access_token():
    url = "https://centralbouat.jmfonline.in/token"
    data = {
        "grant_type": "client_credentials",
        "client_secret": os.environ.get("BROKARAGE_SD_CLIENT_SECRET"),
        "scope": "SDApi",
        "client_id": os.environ.get("BROKARAGE_SD_CLIENT_ID")
    }
    res = requests.post(url, data=data, verify=False)
    res = res.json()
    return res.get("access_token")


def save_brokarage(dra, access_token=None, start_date=None, end_date=None):
    if access_token is None:
        access_token = get_brokarage_access_token()
    # url = "https://centralbouat.jmfonline.in/NetBrokerageforDRADetails" # this is test url
    url = "https://myconnect.jmfonline.in/jmbote/NetBrokerageforDRA"
    if start_date is None and end_date is None:
        dt = timezone.now().date()
        previous_date = dt - timedelta(days=1)
        start_date = datetime.strftime(previous_date, "%b %d %Y")
        end_date = datetime.strftime(previous_date, "%b %d %Y")

    dracode = dra.dra_tag
    fromdate = start_date
    todate = end_date
    reportType = "D"
    IV = os.environ.get("BROKARAGE_AES_ENCRYPTION_IV")
    KEY = os.environ.get("BROKARAGE_AES_ENCRYPTION_KEY")

    enc_dracode = aes_encrypt(dracode, IV, KEY)
    enc_fromdate = aes_encrypt(fromdate, IV, KEY)
    enc_todate = aes_encrypt(todate, IV, KEY)
    enc_reportType = aes_encrypt(reportType, IV, KEY)

    enc_payload = f"{enc_dracode}&AND&{enc_fromdate}&AND&{enc_todate}&AND&{enc_reportType}"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}
    res = requests.post(url, json=enc_payload, headers=headers)
    res = res.content
    res = res.decode('utf-8')
    dsc_res = json.loads(aes_decrypt(res, IV, KEY))

    for r in dsc_res:
        brk = Brokerage(dra=dra)
        brk.api_updated_date = r.get("updatedDate")
        brk.total_cummulative_brokerage = r.get("totalcummulativeBrokerage")
        brk.total_cumulative_net_brokerage = r.get("totalcummulativeNetBrokerageofDRA")
        brk.unique_cummulative_count = r.get("uniquecummulativeclientcount")
        brk.sharing = r.get("sharing")
        brk.branch = r.get("branch")
        brk.save()


def get_daily_brokarage():
    users = User.objects.filter(user_type='dra', is_staff=False, is_superuser=False)
    access_token = get_brokarage_access_token()
    dt = timezone.now().date()
    previous_date = dt - timedelta(days=1)

    start_date = datetime.strftime(previous_date, "%b %d %Y")
    end_date = datetime.strftime(previous_date, "%b %d %Y")
    
    for dra in users:
        save_brokarage(dra, access_token=access_token, start_date=start_date, end_date=end_date)


def generate_jv_file_report():
    # (600) account opening incentive account D
    # (999A) TDS tax on account opening incentive account C
    # (602) Borkarage share account D
    # 10 % TDS on account opening incentive
    dt = timezone.now().date()
    first_date = dt.replace(day=1)
    last_month_date = first_date - timedelta(days=1)
    # last_month_date = first_date
    from core.dra_reports import get_report_data
    headers = [
        "SrNo",
        "VDate",
        "EDate",
        "CltCode",
        "DrCr",
        "Amount",
        "Narration"
    ]
    result = []
    incentive_data = Incentive.objects.filter(created_at__month=last_month_date.month, created_at__year=last_month_date.year, dra__admin_status='approved').annotate(
        month=ExtractMonth('created_at'), year=ExtractYear("created_at")).values('dra__dra_tag', "month", "year").annotate(total=Sum('incentive_amount')).values("month", "year", "total", "dra__dra_tag")
    i = 1
    for iD  in incentive_data:
        total = iD.get("total")
        if not total:
            total = 0
        result.append(
            [
                i,
                indian_date_format(dt),
                indian_date_format(dt),
                iD.get("dra__dra_tag", 'NA'),
                "C",
                total,
                f"Account opening incentives for the month of {calendar.month_name[iD.get('month')]} {iD.get('year')}"
            ]
        )
        result.append(
            [
                i,
                indian_date_format(dt),
                indian_date_format(dt),
                600,
                "D",
                total,
                f"Account opening incentives for the month of {calendar.month_name[iD.get('month')]} {iD.get('year')}"
            ]
        )
        i = i+1
        tds = round((total * 10) / 100, 2)
        result.append(
            [
                i,
                indian_date_format(dt),
                indian_date_format(dt),
                iD.get("dra__dra_tag", 'NA'),
                "D",
                tds,
                "TDS tax on account opening incentives of DRA"
            ]
        )
        result.append(
            [
                i,
                indian_date_format(dt),
                indian_date_format(dt),
                "999A",
                "C",
                tds,
                "TDS tax on account opening incentives of DRA"
            ]
        )
        i = i+1

    # api_updated_date calculate on this field
    brokarage_data = Brokerage.objects.filter(created_at__month=last_month_date.month, created_at__year=last_month_date.year, dra__admin_status='approved').annotate(
        month=ExtractMonth('created_at'), year=ExtractYear("created_at")).values("dra__dra_tag", "month", "year").annotate(total=Sum('total_cumulative_net_brokerage')).values("month", "year", "total", "dra__dra_tag")

    for bD  in brokarage_data:
        total = bD.get("total")
        if not total:
            total = 0
        result.append(
            [
                i,
                indian_date_format(dt),
                indian_date_format(dt),
                bD.get("dra__dra_tag", 'NA'),
                "C",
                total,
                f"Brokerage sharing for the month of {calendar.month_name[bD.get('month')]} {bD.get('year')}"
            ]
        )
        result.append(
            [
                i,
                indian_date_format(dt),
                indian_date_format(dt),
                602,
                "D",
                total,
                f"Brokerage sharing for the month of {calendar.month_name[bD.get('month')]} {bD.get('year')}"
            ]
        )
        i = i+1

    # report_data = {
    #     "headers": headers,
    #     "data": result
    # }
    # jv_file = get_report_data(report_data, in_memory=True, sheet_name="jv_file")
    # jv_file.seek(0)
    csvfile = StringIO()
    csvwriter = csv.writer(csvfile)
    # writing the headers
    csvwriter.writerow(headers)
    # writing the rows
    csvwriter.writerows(result)
    msg_body = get_template('email/jv_report.html').render({})
    dict_to_send = {
        "emails": JMFL_EMAILS,
        "cc": JMFL_EMAILS_CC,
        "subject": "JM FINANCIAL!",
        "msg_body": msg_body,
        "file_name": "jv_report.csv",
        "content_type": "text/csv",
        "attachment": csvfile.getvalue()
    }
    send_mail(**dict_to_send)


def generate_mis_file_report():
    dt = timezone.now().date()
    first_date = dt.replace(day=1)
    last_month_date = first_date - timedelta(days=1)
    from core.dra_reports import get_report_data
    headers = [
        "SrNo",
        "DRA Name",
        "Month",
        "Total Activated accounts",
        "Account opening Incentives",
        "Account opening Incentives payable",
        "Brokerage sharing %",
        "Gross brokerage Generated",
        "Net Brokerage Generated",
        "Grand Total",
        "Payable Amount"
    ]
    result = []
    i = 1
    users = User.objects.filter(user_type='dra', admin_status='approved', is_activated=True, is_staff=False, is_superuser=False)
    date = datetime.today()

    for dra in users:
        brokerage = Brokerage.objects.filter(dra=dra, created_at__month=last_month_date.month, created_at__year=last_month_date.year)
        
        gross_brokarage = brokerage.aggregate(total=Sum('total_cummulative_brokerage'))['total']
        if not gross_brokarage:
            gross_brokarage = 0
        net_brokarage = brokerage.aggregate(total=Sum('total_cumulative_net_brokerage'))['total']
        if not net_brokarage:
            net_brokarage = 0
        total_incentive = Incentive.objects.filter(dra=dra, created_at__month=last_month_date.month, created_at__year=last_month_date.year).aggregate(total=Sum('incentive_amount'))['total']
        if not total_incentive:
            total_incentive = 0

        tds = round((total_incentive * 10) / 100, 2)
        incentive_payable = total_incentive - tds
        lead_count = Leads.objects.filter(dra=dra, created_at__month=last_month_date.month, created_at__year=last_month_date.year).count()

        d = {
            "SrNo": i,
            "DRA Name": f"{dra.name}",
            "Month": f'{calendar.month_name[last_month_date.month]}',
            "Total Activated accounts": f"{lead_count}",
            "Account opening Incentives": f"{total_incentive}",
            "Account opening Incentives payable": f"{incentive_payable}",
            "Brokerage sharing %": dra.brokerage_percentage if dra.brokerage_percentage else 0,
            "Gross brokerage Generated": gross_brokarage,
            "Net Brokerage Generated": net_brokarage,
            "Grand Total": total_incentive + net_brokarage,
            "Payable Amount": f"{incentive_payable + net_brokarage}"
        }
        result.append(d)
        i = i+1
    report_data = {
        "headers": headers,
        "data": result
    }
    mis_file = get_report_data(report_data, in_memory=True, sheet_name="mis_file")
    mis_file.seek(0)
    msg_body = get_template('email/payout_report.html').render({})
    dict_to_send = {
        "emails": JMFL_EMAILS,
        "cc": JMFL_EMAILS_CC,
        "subject": "JM FINANCIAL!",
        "msg_body": msg_body,
        "file_name": "payout_report.xlsx",
        "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "attachment": mis_file.read()
    }
    send_mail(**dict_to_send)


def generate_daily_incentive_file_report():
    today_date = timezone.now()
    from core.dra_reports import get_report_data
    headers = [
        "Sr No",
        "Entry type",
        "DRA code",
        "Client code",
        "Current Brokerage Sharing %",
        "Current Account opening incentives (Rs)",
        "Previous Brokerage Sharing %",
        "Previous Account opening incentives (Rs)",
        "Date of Creation/modification of DRA",
        "Time of Creation /modification of DRA",
        "Date at Email sent by Scale desk team",
        "Time at Email sent by Scale desk team",
        "Created/modified by user",
        "Remarks"
    ]
    result = []
    i = 1
    users = User.objects.filter(user_type='dra', admin_status='approved', is_activated=True, is_staff=False, is_superuser=False)
    for dra in users:
        d = {
            "Sr No": i,
            "Entry type": "New",
            "DRA code": dra.dra_tag,
            "Client code": dra.mx_client_code,
            "Current Brokerage Sharing %": dra.brokerage_percentage if dra.brokerage_percentage else 0,
            "Current Account opening incentives (Rs)": dra.incentive_perlead if dra.incentive_perlead else 0,
            "Previous Brokerage Sharing %": dra.previous_brokerage_percentage if dra.previous_brokerage_percentage else "NA",
            "Previous Account opening incentives (Rs)": dra.previous_incentive_perlead if dra.previous_incentive_perlead else "NA",
            "Date of Creation/modification of DRA": indian_date_format(today_date.date()),
            "Time of Creation /modification of DRA": ampmtime(today_date.time()),
            "Date at Email sent by Scale desk team": indian_date_format(today_date.date()),
            "Time at Email sent by Scale desk team": ampmtime(today_date.time()),
            "Created/modified by user": dra.reporting_manager.name if dra.reporting_manager else "NA",
            "Remarks": "As inputted by user in SD"
        }
        result.append(d)
        i = i+1

    report_data = {
        "headers": headers,
        "data": result
    }
    daily_report = get_report_data(report_data, in_memory=True, sheet_name=f'daily_incentive_report_{today_date.date().strftime("%Y%m%d")}')
    # return daily_report

    daily_report.seek(0)
    msg_body = get_template('email/payout_report.html').render({})
    dict_to_send = {
        "emails": JMFL_EMAILS,
        "cc": JMFL_EMAILS_CC,
        "subject": "JM FINANCIAL!",
        "msg_body": msg_body,
        "file_name": "daily-report.xlsx",
        "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "attachment": daily_report.read()
    }
    send_mail(**dict_to_send)

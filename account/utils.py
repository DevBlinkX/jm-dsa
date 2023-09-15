from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.conf import settings
import os
User = get_user_model()
from django.core.mail import EmailMessage
from account.decorators import postpone
from django.db import connection
import requests
import string
import random
from django.utils import timezone
import json
from urllib import parse 


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def generate_random_code(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def register_users(request, *args, **kwargs):
    """
    function to register the user
    """
    from django.contrib.auth import login, authenticate
    try:
        email=kwargs.pop("email")
        username=kwargs.pop("username")
        password=kwargs.pop("password", None)
        mobile=kwargs.pop("mobile")
        name=kwargs.pop("name")
        medium = kwargs.get('medium')
        user_type= "dsa"
        # city = kwargs.get('city', None)
        
        if password is None:
            password = generate_random_code(size=8)

        if User.objects.filter(mobile=mobile).exists():
            user = User.objects.get(mobile=mobile)
            user.username = username
            user.set_password(password)
        else:
            user = User.objects.create_user(username, email, password,user_type=user_type)

        user.name = name
        # user.city = city
        # try:
        #     dt = timezone.now().date()
        #     pk = "{0:0=3d}".format(user.id)
        #     influencer = f'INF{dt.year}{pk}'
        #     user.influencer = influencer
        # except:
        #     pass
        user.mobile = mobile

        if medium == 'web':
            user.registration_medium = medium
        else:
            user.registration_medium = 'app'

        user.save()
        return user
    except Exception as e:
        raise e


@postpone
def send_mail(*args,**kwargs):
    """
    function to send the mail
    """
    try:
        subject = kwargs.pop("subject")
        msg_body = kwargs.pop("msg_body")
        emails = kwargs.pop("emails")
        cc = kwargs.pop("cc", None)
        attachment = kwargs.pop("attachment", None)
        if not isinstance(emails, list):
            emails = [emails]

        if cc:
            if not isinstance(cc, list):
                cc = [cc]
        else:
            cc = []

        try:
            msg = EmailMessage(subject, msg_body, settings.DEFAULT_FROM_EMAIL, emails, cc=cc)
            msg.content_subtype = "html"
            if attachment:
                msg.attach(kwargs.pop("file_name"), attachment, kwargs.pop("content_type"))
            msg.send()
            return True
        except:
            return False
    except:
        pass
    finally:
        connection.close()


def send_regular_mail(*args, **kwargs):
    """
    function to send the mail
    """
    try:
        subject = kwargs.pop("subject")
        msg_body = kwargs.pop("msg_body")
        emails = kwargs.pop("emails")
        attachment = kwargs.pop("attachment", None)
        if not isinstance(emails, list):
            emails = [emails]
        try:
            msg = EmailMessage(subject, msg_body, settings.DEFAULT_FROM_EMAIL, emails)
            msg.content_subtype = "html"
            if attachment:
                msg.attach(kwargs.pop("file_name"), attachment, kwargs.pop("content_type"))
            msg.send()
            return True
        except:
            return False
    except:
        pass


def send_sms(*args, **kwargs):
    """
    function to send the sms
    """
    to = kwargs.get("to")
    message = kwargs.get("message")
    user_id =  settings.SMS_USER_ID
    password = settings.SMS_PASSWORD
    # url = f"https://enterprise.smsgupshup.com/GatewayAPI/rest?msg={msg}&v=1.1&userid={user_id}&password={password}&send_to={to}&msg_type=text&method=sendMessage"
    url = f"https://enterprise.smsgupshup.com/GatewayAPI/rest?msg={message}&v=1.1&userid={user_id}&password={password}&send_to={to}&msg_type=text&method=sendMessage"
    result = requests.get(url)
    return result


def get_dra_client(mobile):
    mobile = mobile.strip()
    url = f"https://api-in21.leadsquared.com/v2/LeadManagement.svc/Leads.Get?accessKey={settings.LEAD_SQUARE_ACCESS_KEY}&secretKey={settings.LEAD_SQUARE_SECRET_KEY}"
    payload = {
        "Parameter": {
            "LookupName": "Phone",
            "LookupValue": f"+91-{mobile}",
            "SqlOperator": "="
        },
        "Columns": {
            "Include_CSV": "ProspectID, FirstName, LastName, EmailAddress, Phone, mx_Client_Code, mx_DRA_Code,mx_Referred_DRA_Code , Source, SourceMedium, SourceCampaign, mx_DIY_Stage, mx_First_Trade_Date, Created_On"
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
    if len(res):
        return res[0]
    else:
        return None


def check_dra_user(mobile):
    try:
        res = get_dra_client(mobile)
        if res:
            if res.get("SourceCampaign") == "RNE":
                return True, True
            return False, True
        return False, False
    except Exception as e:
        return False, False


def update_dra_code(user):
    try:
        if not user.prospect_id:
            dra_client = get_dra_client(user.mobile)
            if dra_client:
                user.prospect_id = dra_client.get("ProspectID")
                user.save()
        base_url = "https://api-in21.leadsquared.com/v2/LeadManagement.svc/Lead.Update"
        url = f"{base_url}?accessKey={settings.LEAD_SQUARE_ACCESS_KEY}&secretKey={settings.LEAD_SQUARE_SECRET_KEY}&leadId={user.prospect_id}&postUpdatedLead=true"
        payload = [
            {
                "Attribute": "Phone",
                "Value": f"+91-{user.mobile}"
            },
            {
                "Attribute": "mx_DRA_Code",
                "Value": user.dra_tag
            }
        ]
        headers = {"Content-Type": "application/json"}
        res = requests.post(url, json=payload, headers=headers)
        res = res.json()
        return res
    except:
        pass


def generate_dra_code(user):
    from core.aes_encryption import encrypt
    user_id = str(user.id)
    dra_code = f"DSA{user_id.zfill(7)}"
    try:
        user.dra_code_encrypted = encrypt(dra_code)
    except:
        pass
    user.dra_tag = dra_code
    user.save()
    res = update_dra_code(user)
    return res


from django.template.loader import get_template

def test_mail():
    instance ={
        "name": "Javed Ahamad",
        "email": "javed@scaledesk.com"
    } 
    msg_body = get_template('email/profile-activated.html').render(
                    {"user": instance})
    dict_to_send = {
        "emails": instance.get("email"),
        "subject": "JM FINANCIAL- Welcome !",
        "msg_body": msg_body
    }
    send_regular_mail(**dict_to_send)


def whatsapp_opt_in(mobile):
    try:        
        url = "https://media.smsgupshup.com/GatewayAPI/rest"
        method = "OPT_IN"
        format = "json"
        userid = settings.WHATSAPP_USER_ID
        password = settings.WHATSAPP_PASSWORD
        phone_number = mobile
        v=1.1
        auth_scheme="plain"
        channel="WHATSAPP"
        url = f"{url}?method={method}&format={format}&userid={userid}&password={password}&phone_number={phone_number}&v={v}&auth_scheme={auth_scheme}&channel={channel}"
        res = requests.get(url)
        print(res.json())
        return res.json()
    except:
        pass


def send_whatsapp_message(mobile, message=None):
    url = "http://media.smsgupshup.com/GatewayAPI/rest"
    data = {
        "send_to": mobile,
        "msg_type": "Text",
        "userid": settings.WHATSAPP_USER_ID,
        "password": settings.WHATSAPP_PASSWORD,
        "auth_scheme": "plain",
        "method": "SendMessage",
        "format": "json",
        "msg": "message"
    }
    # print(data)
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    res = requests.post(url, data=data, headers=headers)
    # print(res.json())
    return res.json()

# def send_whatsapp_message(mobile,message=None):
#     try:
#         print(message)
#         url="https://media.smsgupshup.com/GatewayAPI/rest?method=SendMessage&userid="+settings.WHATSAPP_USER_ID+"&password="+settings.WHATSAPP_PASSWORD+"&send_to=7210643394&v=1.1&format=json&msg"+message
#         print(url)
#         res = requests.post(url)
#         res=res.json()
#         print(res)
      
#         if res.get("response").get("status"):
#             return True
#     except Exception as e:
        
#         print(str(e))
#     return False

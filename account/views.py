from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework import viewsets
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from django.conf import settings
from account.models import CorporateDetail, User, Platform, MobileVerificationCode, BankDetail
from account.serializers import PlatformsSerializer, UserSerializer, validate_bank_detail, \
    get_serialized_bank_detail
from account.utils import get_tokens_for_user, register_users, generate_random_code, \
     send_mail, send_sms, check_dra_user
from django.template.loader import get_template
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import logging
import json
from django.db.models import Q
import requests
import os


logger = logging.getLogger(__name__)
from rest_framework.parsers import MultiPartParser, FileUploadParser


def is_email(input):
    import re
    pat = re.compile("[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?")
    m = pat.match(input)
    if m:
        return True
    return False


def is_mobile(input):
    if len(input) == 10:
        return str(input).isnumeric()
    return False


def get_user_detail(username):
    try:
        if is_email(username):
            user = get_user_model().objects.get(email=username)
            return user
        elif is_mobile(username):
            profile = Profile.objects.get(mobile=username)
            return profile.user
        user = get_user_model().objects.get(username=username)
        return user
    except Exception:
        return None

def verify_mobile_number(mobile, code):
        """
        Function for create user
        """
        try:
            mb = MobileVerificationCode.objects.filter(mobile=mobile).last()
            if mb.code == code:
                return True
            else:
                return False
        except Exception as e:
            return False


def check_user_profile_status(user):
    errors = []
    st = True
    profile = user.profile
    if not profile.mobile_verified:
        st = False
        errors.append("Mobile Verification Pending")

    if not profile.email_verified:
        st = False
        errors.append("Email Verification Pending")

    if not profile.is_active:
        st = False
        errors.append("Manual Account Verification Pending")

    return st, errors
    # return True, []


def check_flag_status(profile):
    flag = True
    if not profile.mobile_verified:
        flag = False
    if not profile.email_verified:
        flag = False
    return flag

def validate_password(password):
    if password is None:
        return False, "Password can not be blank"

    if len(password) < 6:
        return False, "Password must be 6 character long"

    return True, None


def validate_mobile(mobile):
    mobile = str(mobile)
    if len(mobile) == 10:
        if (mobile).startswith('0'):
            return False
        return mobile.isdigit()
    return False


def send_mobile_verification_code(mobile, email=None, user=None):
    try:
        # try:
        #     pcode = MobileVerificationCode.objects.filter(mobile=mobile).last()
        #     ct = timezone.now()
        #     ct = ct - timedelta(minutes=5)
        #     if not pcode.is_verified and pcode.created_at >=ct:
        #         msg = f'Your OTP for mobile verification is {pcode.code}. You can use this only once. Do not share this OTP with anyone for security reasons. - JMFL'
        #         res = send_sms(to=mobile, message=msg)
        #         return res
        # except:
        #     pass

        code = generate_random_code()
        mb = MobileVerificationCode()
        mb.code = code
        mb.mobile = mobile
        mb.email = email
        mb.user = user
        mb.save()
        if email is not None:
            msg_body = get_template('email/otp.html').render({"code": code})
            dict_to_send = {
                "emails": email,
                "subject": "JM FINANCIAL!",
                "msg_body": msg_body
            }
            send_mail(**dict_to_send)
        # msg = f"Hi, Your OTP Verification Code is {code} to proceed at JM Financial. This code is valid for next 10 minutes. For security reason do not share this OTP with anyone- JM Financial Services"
        # msg = f"Hurray…! Welcome {code} to  JM Financials.-JMFS"
        msg = f"Hi, Your OTP Verification Code is {code} to proceed at JM Financial. This code is valid for next 10 minutes. For security reason do not share this OTP with anyone- JM Financial Services"
        res = send_sms(to=mobile, message=msg)
        print(res)
        return res
    except:
        print("error")
        return None

def validate_mobile_code(mobile, code):
    try:
        mb = MobileVerificationCode.objects.filter(mobile=mobile).last()
        if mb.code == code:
            mb.is_verified = True
            mb.save()
            token = None
            if mb.user:
                if mb.user.user_type == "rmj":
                    token= get_tokens_for_user(mb.user)
                    return True, token
                elif mb.user.admin_status == "approved":
                    token= get_tokens_for_user(mb.user)
                    return True, token
                else:
                    return False, "Your account is not approved"
            else:
                return False, None
        else:
            return False, "Invalid code"
    except Exception as e:
        return False, str(e)


def validate_email_code(email, code):
    try:
        mb = MobileVerificationCode.objects.filter(email=email).last()
        if mb.code == code:
            mb.is_verified = True
            mb.save()
            token = None
            if mb.user:
                if mb.user.user_type == "rmj":
                    token= get_tokens_for_user(mb.user)
                    return True, token
                elif mb.user.admin_status == "approved":
                    token= get_tokens_for_user(mb.user)
                    return True, token
                else:
                    return False, "Your account is not approved"
            else:
                return False, None
        else:
            return False, "Invalid code"
    except Exception as e:
        return False, str(e)


def send_email_verification_link(request, user):
    import jwt
    token = jwt.encode({'user_id': user.id}, 'secret', algorithm='HS256').decode('utf-8')
    link = f'{settings.URL_PROTOCOL}://{request.get_host()}/email/verification/{token}/'
    msg_body = get_template('email/email-verification-link.html').render({"link": link, "user": user})
    email_data = {
        "subject": "Howdy! Welcome to JMFL",
        "msg_body": msg_body,
        "emails": user.email
    }
    send_mail(**email_data)


class UserView(viewsets.ViewSet):
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )

    authenticated_function = [
        'save_channel_detail', 
        'check_followers_status', 
        'add_corporate_data',
        'profile', 
        'profile_update',
        'session_login',
        'update_bank_detail',
        'agree_to_term_and_condition',
        'request_call_back',
        'create_short_url'
    ]

    def get_authenticators(self):
        if self.action_map.get('get') in ['profile']:
            return super().get_authenticators()
        elif self.action_map.get('post') in self.authenticated_function:

            return super().get_authenticators()
        return []

    def get_permissions(self):
        if self.action_map.get('get') in ['profile']:
            return super().get_permissions()
        elif self.action_map.get('post') in self.authenticated_function:
            return super().get_permissions()
        return []

    def create_short_url(self, request):
        try:
            data = request.data
            # url = "https://fs.jmfs.ltd/api/CreateShortUrl"
            # headers = {
            #     "UserID": "Digital Referral Associate",
            #     "accesskey": os.environ.get("URL_SHORTNER_ACCESS_KEY"),
            #     "token": os.environ.get("URL_SHORTNER_TOKEN")
            # }
            # payload = {
            #     "LongUrl" : data.get("url", None),
            #     "UserID" : "Digital Referral Associate"
            # }
            # res = requests.post(url, json=payload, headers=headers)
            # res = res.json()
            # print(data.get("url", None),"url")

            import pyshorteners

            # Create an instance of the pyshorteners.Shortener class
            s = pyshorteners.Shortener()

            # Shorten a long URL
            long_url = data.get("url", None)
            short_url = s.tinyurl.short(long_url)

            # Print the short URL
            # print(short_url)


            # url = "https://api.short.io/links"
            # payload = {
            #     "domain": os.environ.get("URL_SHORTNER_DOMAIN"),
            #     "allowDuplicates": True,
            #     "originalURL": data.get("url", None),
            #     "title": "Digital Referral Associate",
            #     "redirectType": 302,
            # }
            # headers = {
            #     "accept": "application/json",
            #     "content-type": "application/json",
            #     "Authorization": os.environ.get("URL_SHORTNER_KEY")
            # }
            # res = requests.post(url, json=payload, headers=headers)
            # res = res.json()

            return Response(data={'status': True, "data": short_url,"shortURL":short_url}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'status': False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def check_username(self, request):
        """
        Get function for checking username
        """
        username = request.data.get('username')
        try:
            user = User.objects.get(username=username)
            if user:
                return Response(data={'success': False, 'msg': 'username already exists'}, status=status.HTTP_200_OK)
            else:
                return Response(data={'success': True, 'msg': 'Username Available'}, status=status.HTTP_200_OK)
        except:
            return Response(data={'success': True, 'msg': 'Username Available'}, status=status.HTTP_200_OK)

    def send_login_otp(self, request):
        """
        Get function for checking username
        """
        mobile = request.data.get('mobile', None)
        email = request.data.get('email', None)
        if mobile is None and email:
            try:
                email =  email.strip()
                user = User.objects.get(email=email)
                if user:
                    send_mobile_verification_code(None, email=email, user=user)
                    return Response(data={'success': True, 'msg': 'otp sent'}, status=status.HTTP_200_OK)
                    # else:
                        # return Response(data={'success': False, 'msg': 'Your account is not approved!'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(data={'success': False, 'msg': 'Invalid Email ID'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response(data={'success': False, 'msg': 'Invalid Email ID'}, status=status.HTTP_400_BAD_REQUEST)

        if mobile is None or mobile =="":
            return Response(data={'success': False, 'msg': 'Invalid Mobile Number'}, status=status.HTTP_400_BAD_REQUEST)


        try:
            mobile =  mobile.strip()
            user = User.objects.get(mobile=mobile)
            if user:
                send_mobile_verification_code(mobile, user=user)
                return Response(data={'success': True, 'msg': 'otp sent'}, status=status.HTTP_200_OK)
                # else:
                    # return Response(data={'success': False, 'msg': 'Your account is not approved!'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data={'success': False, 'msg': 'Invalid Mobile Number'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={'success': False, 'msg': 'Invalid Mobile Number'}, status=status.HTTP_400_BAD_REQUEST)

    def check_mobile(self, request):
        """
        Get function for checking username
        """
        mobile = request.data.get('mobile')
        try:
            user = User.objects.get(mobile=mobile)
            # user and user.is_completed
            if user:
                return Response(data={'success': False, 'msg': 'mobile number already exists'}, status=status.HTTP_200_OK)
            else:
                send_mobile_verification_code(mobile)
                return Response(data={'success': True, 'msg': 'mobile number Available'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            send_mobile_verification_code(mobile)
            return Response(data={'success': True, 'msg': 'mobile number Available'}, status=status.HTTP_200_OK)

    def resend_mobile_verification_code(self, request):
        """
        Function for create user
        """
        data  = request.data
        mobile = data.get("mobile")
        send_mobile_verification_code(mobile)
        return Response(data={'status': True, 'message': 'verification code send'}, status=status.HTTP_200_OK)

    def check_email(self, request):
        """
        Get function for checking email
        """
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            return Response(data={'success': False, 'msg': 'email id already exists'}, status=status.HTTP_200_OK)

        return Response(data={'success': True, 'msg': 'email Available'}, status=status.HTTP_200_OK)

    def login_with_otp(self, request):
        """
        Function for create user
        """
        code = request.data.get('code')
        mobile = request.data.get('mobile', None)
        email = request.data.get('email', None)
        if mobile is None:
            if email:
                st, data = validate_email_code(email, code)
                # print(data)
                if st:
                    return Response(data={'status': True, 'message': 'user authenticated', "data": data }, status=status.HTTP_200_OK)
                else:
                    # print(data)
                    return Response(data={'status': False, 'message': data}, status=status.HTTP_400_BAD_REQUEST)

        st, data = validate_mobile_code(mobile, code)
        if st:
            # print(data)
            return Response(data={'status': True, 'message': 'user authenticated', "data": data }, status=status.HTTP_200_OK)
        else:
            # print(data)
            return Response(data={'status': False, 'message': data}, status=status.HTTP_400_BAD_REQUEST)

    def session_login(self, request):
        """
        Function for session login
        """
        user = request.user
        if user.is_authenticated:
            login(request, user)
        return Response(data={'status': True}, status=status.HTTP_200_OK)

    def signup(self, request):
        """
        Function for create user
        """
        data = request.data
        try:
            email = data.get('email')
            mobile = data.get('mobile')
            name= data.get('name')
            code = data.get('mobile_verification_code', None)
            medium = data.get('registration_medium', None)
            # city = data.get('location', None)
            username = mobile

            if not validate_mobile(mobile):
                return Response(data={'status': False, 'message': "Invalid mobile number"}, status=status.HTTP_400_BAD_REQUEST)

            if not verify_mobile_number(mobile, code):
                return Response(data={'status': False, 'message': "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

            rne_status, dra_status = check_dra_user(mobile)

            if rne_status:
                return Response(data={
                    'status': True, 
                    'message': 'User can not registered', 
                    "is_dra": dra_status, 
                    "is_rne": rne_status}, status=status.HTTP_200_OK)
            # TODO check emails and mobile for already exist.

            dt = {
                "username": mobile,
                "email": email,
                "password": None,
                "mobile": mobile,
                "name": name,
                "medium": medium,
            }
            user = register_users(request, **dt)
            token = get_tokens_for_user(user)
            data = UserSerializer(user, context={"request": request}).data
            return Response(data={'status': True, 'message': 'User registered', 'token': token, "profile": data, "is_dra": dra_status, "is_rne": rne_status}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response(data={'status': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def add_corporate_data(self, request):
        data = request.data
        try:
            user = request.user
            try:
                corporate_detail =  CorporateDetail.objects.get(user=user)
            except CorporateDetail.DoesNotExist:
                corporate_detail =  CorporateDetail(user=user)

            corporate_detail.organisation_name = data.get("organisation_name")
            corporate_detail.nature_of_business = data.get("nature_of_business")
            corporate_detail.website_link = data.get("website_link")
            corporate_detail.company_address = data.get("company_address")
            corporate_detail.company_pancard_number = data.get("company_pancard_number")
            corporate_detail.certificate_of_incorporation = data.get("certificate_of_incorporation")
            corporate_detail.moa = data.get("moa")
            corporate_detail.aoa = data.get("aoa")
            corporate_detail.gst_certificate = data.get("gst_certificate")
            corporate_detail.cancelled_cheque = data.get("cancelled_cheque")
            corporate_detail.save()
            user.is_completed = True
            user.save()
            return Response(data={'status': True, 'message': 'User corporate data updated'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response(data={'status': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def save_channel_detail(self, request):
        user = request.user
        data = request.data
        try:
            account_type = data.get('account_type')
            account_id = data.get('account_id')
            user.account_type = account_type
            user.account_id = account_id
            user.followers = data.get('followers')

            channel_details = {
                "account_type": user.account_type,
                "account_id": user.account_id,
                "followers": user.followers
            }
            request.session['user_channel_details'] = channel_details
            user.save()
            dra_status = False
            res = None
            try:
                platform = Platform.objects.get(key=user.account_type.lower())
                is_satisfied = False
                if user.followers:
                    is_satisfied = int(user.followers) >= platform.minimum_allowed_users

                res = {
                    "platform": user.account_type,
                    "minimum_allowed": platform.minimum_allowed_users,
                    "followers": user.followers,
                    "is_satisfied": is_satisfied
                }

                # if is_satisfied:
                #     dra_status = check_dra_user(user)
                #     profile.is_completed = True
                #     profile.save()

                user.is_completed = True
                user.save()
            except Exception as e:
                res = str(e)

            return Response(data={'status': True, "isDRA": dra_status, "data": res}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'status': False, 'message': str(e)}, status=status.HTTP_200_OK)

    def check_followers_status(self, request):
        user = request.user
        platform = Platform.objects.get(key=user.account_type.lower())
        res = {
            "platform": user.account_type,
            "minimum_allowed": platform.minimum_allowed_users,
            "followers": user.followers
        }
        return Response(data={'status': True, "data": res}, status=status.HTTP_200_OK)

    def profile(self, request):
        """
        user profile
        """
        user = request.user
        data = UserSerializer(user, context={"request": request}).data
        return Response(data={'status': True, "user": data}, status=status.HTTP_200_OK)

    def update_bank_detail(self, request):
        parser_classes = [MultiPartParser, FileUploadParser]
        data = request.data
        user = request.user

        validated, error_list = validate_bank_detail(data)
        if not validated:
            return Response(data={'status': False, "message": error_list}, status=status.HTTP_400_BAD_REQUEST)

        try:
            try:
                bank_detail = user.bank_detail
            except:
                bank_detail = BankDetail(user=user)
            bank_detail.pan_no = data.get("pan_no")
            bank_detail.bank_account_no = data.get("bank_account_no")
            bank_detail.account_type = data.get("account_type")
            bank_detail.account_holder_name = data.get("account_holder_name")
            bank_detail.ifsc_code = data.get("ifsc_code")

            if data.get("pan_card_file"):
                bank_detail.pan_card_file = data.get("pan_card_file")
            if data.get("cancelled_cheque"):
                bank_detail.cancelled_cheque = data.get("cancelled_cheque")
            if data.get("aadhar_card_file"):
                bank_detail.aadhar_card_file = data.get("aadhar_card_file")

            bank_detail.save()
            return Response(data={'status': True, "bank_detail": get_serialized_bank_detail(bank_detail)}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'status': False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def agree_to_term_and_condition(self, request):
        user = request.user
        data = request.data
        is_agree = data.get("is_agreed")
        if is_agree:
            user.is_aggre_term_condition = True
            user.term_condition_agree_time = timezone.now()
            user.save()
            from account.utils import generate_dra_code
            generate_dra_code(user)
            return Response(data={'status': True, "message": "successful"}, status=status.HTTP_200_OK)
        return Response(data={'status': True, "message": "Failed"}, status=status.HTTP_200_OK)

    def profile_update(self, request):
        user = request.user
        data = request.data
        parser_classes = [MultiPartParser, FileUploadParser]
        
        email = data.get('email', None)
        if email is not None:
            if is_email(email):
                if User.objects.filter(email=email).exists() and user.email != email:
                    print("email already exists")
                    return Response(data={'status': False, "message": "Email Already exist"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    print("failed")

                user.email = email
                user.save()
            else:
                return Response(data={'status': False, "message": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)

        # send_email_verification_link(request, user)
        ss = UserSerializer(user, context={"request": request})
        ss.update(user, data)
        return Response(data={'status': True, "user": ss.data}, status=status.HTTP_200_OK)

    def request_call_back(self, request):
        try:
            user = request.user
            rm_user = user.reporting_manager
            msg_body = get_template('email/request-callback.html').render({"user": user, "rm_user": rm_user})
            dict_to_send = {
                "emails": rm_user.email,
                "subject": "JM FINANCIAL- Request Callback !",
                "msg_body": msg_body,
                "cc": ["drasupport@jmfl.com"]
            }
            send_mail(**dict_to_send)
            return Response(data={'status': True, "message": "request sent"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'status': False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PlatformsView(APIView):
    """
    platforms views
    """
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        """
        Return a list of all platform.
        """
        params = request.query_params
        excluded_platforms = ['youtube', 'facebook', 'instagram']
        if params.get('all', None) is not None:
            excluded_platforms = []
        platforms = Platform.active_platform.exclude(key__in=excluded_platforms)
        ss = PlatformsSerializer(platforms, many=True, context={"request": request})
        return Response(data={"status": True, "data": ss.data}, status=status.HTTP_200_OK)

    def post(self, request):
        """
        create platform
        """
        data = request.data
        ss = PlatformsSerializer(data=data, context={"request": request})
        if ss.is_valid():
            ss.save()
            return Response(data={'success': True, 'data': data}, status=status.HTTP_200_OK)
        else:
            return Response(data={'success': False, 'message': ss.errors}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        """
        create platform
        """
        try:
            p = Platform.objects.get(id=pk)
            p.delete()
            return Response(data={'success': True, "message": "Deleted"}, status=status.HTTP_200_OK)
        except Platform.DoesNotExist:
            return Response(data={'success': False, 'message': "This Platform does not exist"}, status=status.HTTP_404_NOT_FOUND)

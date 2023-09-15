from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from django.conf import settings
from core.models import OverviewBanner
from django.template.loader import get_template
from django.utils import timezone
from datetime import datetime, timedelta
import logging
from django.db.models import Q, F
from django.db import models
from .models import *
from account.models import User
from .serializers import *
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from .utils import *
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from account.serializers import *
from django.db.models import Sum
from django.urls import reverse
from .resoureces import *
from tablib import Dataset
logger = logging.getLogger(__name__)


class BanerView(viewsets.ViewSet):

    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )


    def get_latest_banner(self, request):
        """
        Get latest banner detail
        """
        try:
            banner = OverviewBanner.objects.first()
            data = {}
            if banner:
                data = {
                    "id": banner.id,
                    "title": banner.title,
                    "short_description": banner.short_description,
                    "link": banner.link,
                    "image": banner.image.url
                }
            return Response(data={'success': True, 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'success': True, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DashbardView(viewsets.ViewSet):

    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )

    def get_overview(self, request):
        """
        Get overall overview
        """
        try:
            import datetime
            user = request.user
            filter_by = request.query_params.get("days", None)
            to_date=request.query_params.get("to_date", None)
            from_date=request.query_params.get("from_date", None)
            if (filter_by and filter_by.isdigit()) and (filter_by == '30' or filter_by == '60' or filter_by == '90'):
                filter_date = datetime.datetime.today() - datetime.timedelta(days=int(filter_by))
                total_leads_added = Leads.objects.filter(dra=user, created_at__date__gte=filter_date.date()).count()
                pending_mandate = Leads.objects.filter(dra=user, created_at__date__gte=filter_date.date(), mandate_status="In-Process").count()
                rejected_lead = Leads.objects.filter(dra=user, created_at__date__gte=filter_date.date(),mandate_status='Rejected').count()
                successful_mandate= Leads.objects.filter(dra=user, created_at__date__gte=filter_date.date(), mandate_status="Disbursed").count()
                data = {
                    "total_leads_added": total_leads_added,
                    "pending_mandate": pending_mandate,
                    "rejected_lead": rejected_lead,
                    "successful_mandate":successful_mandate,
                    "success_rate": 0 if total_leads_added == 0 else round(successful_mandate/total_leads_added*100, 1),
                }
            elif to_date and from_date:
                # filter_date = datetime.datetime.today() - datetime.timedelta(days=int(filter_by))
                total_leads_added = Leads.objects.filter(dra=user,created_at__date__gte=from_date, created_at__date__lte=to_date).count()
                pending_mandate = Leads.objects.filter(dra=user,created_at__date__gte=from_date, created_at__date__lte=to_date, mandate_status="In-Process").count()
                rejected_lead = Leads.objects.filter(dra=user,created_at__date__gte=from_date, created_at__date__lte=to_date,mandate_status='Rejected').count()
                successful_mandate= Leads.objects.filter(dra=user,created_at__date__gte=from_date, created_at__date__lte=to_date, mandate_status="Disbursed").count()
                data = {
                    "total_leads_added": total_leads_added,
                    "pending_mandate": pending_mandate,
                    "rejected_lead": rejected_lead,
                    "successful_mandate":successful_mandate,
                    "success_rate": 0 if total_leads_added == 0 else round(successful_mandate/total_leads_added*100, 1),
                }  
            else:
                total_leads_added = Leads.objects.filter(dra=user).count()
                pending_mandate = Leads.objects.filter(dra=user,mandate_status="In-Process").count()
                rejected_lead = Leads.objects.filter(dra=user,mandate_status='Rejected').count()
                successful_mandate= Leads.objects.filter(dra=user, mandate_status="Disbursed").count()
                data = {
                    "total_leads_added": total_leads_added,
                    "pending_mandate": pending_mandate,
                    "rejected_lead": rejected_lead,
                    "successful_mandate":successful_mandate,
                    "success_rate": 0 if total_leads_added == 0 else round(successful_mandate/total_leads_added*100, 1),
                    # "activation_percentage": 0 if total_leads_added == 0 else round(total_account_opened/total_leads_added*100, 1),
                    # "total_app_download":Leads.objects.filter(dra=user, app_downloaded=True).count(),
                }
            return Response(data={'success': True, 'data': data}, status=status.HTTP_200_OK)      
        except Exception as e:
            return Response(data={'success': False, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def get_leads(self, request):
        """
        Get overall leads
        """
        try:
            import datetime
            user = request.user
            filter_by = request.query_params.get("days", None)
            to_date=request.query_params.get("to_date", None)
            from_date=request.query_params.get("from_date", None)
            if (filter_by and filter_by.isdigit()) and (filter_by == '30' or filter_by == '60' or filter_by == '90'):
                
                filter_date = datetime.datetime.today() - datetime.timedelta(days=int(filter_by))
                delta = int(filter_by) / 6
                data = []
                start_date = filter_date
                for x in range(6):
                    import random
                    start_date = start_date + datetime.timedelta(days=int(delta))
                    leads_added = Leads.objects.filter(dra=user, lsq_created_on__date__lte=start_date).count()
                    # leads_activated = Leads.objects.filter(dra=user, lsq_created_on__lte=start_date, mx_diy_stage="Migration Complete").count()
                    data.append(
                        {
                            "month": start_date.strftime('%d %b'),
                            "data": {
                                "added": leads_added,
                            }
                        },
                    )
            elif to_date and from_date:
                from datetime import datetime,timedelta
                date_format = "%Y-%m-%d"
                to_dates = datetime.strptime(to_date, date_format).strftime('%d %b')
                from_dates=datetime.strptime(from_date, date_format).strftime('%d %b')
                tos_dates = datetime.strptime(to_date, date_format)
                froms_dates=datetime.strptime(from_date, date_format)
                dates=tos_dates-froms_dates
                data = []
                for x in range(dates.days+1):
                    for_date=froms_dates.strftime('%d %b')
                    leads_added = Leads.objects.filter(dra=user, lsq_created_on__date=froms_dates).count()
                    data.append(
                        {
                            "month": f'{for_date}',
                            "data": {
                                "added": leads_added,
                            }
                        },
                    )
                    froms_dates = froms_dates + timedelta(days=1)
            else:
                import datetime
                data = []
                start_date = datetime.datetime.today()
                for x in range(6):
                    import random
                    start_date = start_date - datetime.timedelta(days=5)
                    leads_added = Leads.objects.filter(dra=user).count()
                    data.append(
                        {
                            "month": start_date.strftime('%d %b'),
                            "data": {
                                "added": leads_added,
                            }
                        },
                    )
            return Response(data={'success': True, 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'success': True, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def get_successful_rate(self, request):
        """
        Get overall successful rate
        """
        try:
            user = request.user
            data = {}
            filter_by = request.query_params.get("days", None)
            to_date=request.query_params.get("to_date", None)
            from_date=request.query_params.get("from_date", None)
            if (filter_by and filter_by.isdigit()) and (filter_by == '30' or filter_by == '60' or filter_by == '90'):
                import datetime
                filter_date = datetime.datetime.today() - datetime.timedelta(days=int(filter_by))
                delta = int(filter_by) / 6
                
                start_date = filter_date
                for x in range(6):
                    import random
                    start_date = start_date + datetime.timedelta(days=int(delta))
                    total_leads_added = Leads.objects.filter(dra=user, lsq_created_on__lte=start_date).count()
                    leads_added = Leads.objects.filter(dra=user, lsq_created_on__lte=start_date,mandate_status="Disbursed").count()
                    success_rate=0 if total_leads_added == 0 else round(leads_added/total_leads_added*100, 1)
                    data[start_date.strftime('%d %b')]=success_rate

            elif to_date and from_date:
                from datetime import datetime,timedelta
                date_format = "%Y-%m-%d"
                to_dates = datetime.strptime(to_date, date_format).strftime('%d %b')
                from_dates=datetime.strptime(from_date, date_format).strftime('%d %b')
                tos_dates = datetime.strptime(to_date, date_format)
                froms_dates=datetime.strptime(from_date, date_format)
                dates=tos_dates-froms_dates
                for x in range(dates.days+1):
                    for_date=froms_dates.strftime('%d %b')
                    total_leads_added = Leads.objects.filter(dra=user, lsq_created_on=froms_dates).count()
                    leads_added = Leads.objects.filter(dra=user, lsq_created_on=froms_dates,mandate_status="Disbursed").count()
                    success_rate=0 if total_leads_added == 0 else round(leads_added/total_leads_added*100)
                    data[for_date]=success_rate
                    froms_dates = froms_dates + timedelta(days=1)

            else:
                import datetime
                start_date = datetime.datetime.today()
                for x in range(6):
                    import random
                    start_date = start_date
                    total_leads_added = Leads.objects.filter(dra=user, lsq_created_on__lte=start_date).count()
                    leads_added = Leads.objects.filter(dra=user, lsq_created_on__lte=start_date,mandate_status="Disbursed").count()
                    success_rate=0 if total_leads_added == 0 else round(leads_added/total_leads_added*100)
                    data[start_date.strftime('%d %b')]=success_rate
                    start_date = start_date - datetime.timedelta(days=1)
            return Response(data={'success': True, 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'success': True, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_successful_disbursed(self, request):
        """
        Get overall successful rate
        """
        try:
            data={}
            user = request.user
            filter_by = request.query_params.get("days", None)
            to_date=request.query_params.get("to_date", None)
            from_date=request.query_params.get("from_date", None)
            if (filter_by and filter_by.isdigit()) and (filter_by == '30' or filter_by == '60' or filter_by == '90'):
                import datetime
                filter_date = datetime.datetime.today() - datetime.timedelta(days=int(filter_by))
                delta = int(filter_by) / 6
                start_date = filter_date
                for x in range(6):
                    import random
                    start_date = start_date + datetime.timedelta(days=int(delta))
                    leads_added = Leads.objects.filter(dra=user, lsq_created_on__lte=start_date,mandate_status="Disbursed").count()
                    data[start_date.strftime('%d %b')]=leads_added

            elif to_date and from_date:
                from datetime import datetime,timedelta
                date_format = "%Y-%m-%d"
                to_dates = datetime.strptime(to_date, date_format).strftime('%d %b')
                from_dates=datetime.strptime(from_date, date_format).strftime('%d %b')
                tos_dates = datetime.strptime(to_date, date_format)
                froms_dates=datetime.strptime(from_date, date_format)
                dates=tos_dates-froms_dates
                for x in range(dates.days+1):
                    for_date=froms_dates.strftime('%d %b')
                    leads_added = Leads.objects.filter(dra=user, lsq_created_on=froms_dates ,mandate_status="Disbursed").count()
                    data[for_date]=leads_added
                    froms_dates = froms_dates + timedelta(days=1)

            else:
                import datetime
                start_date = datetime.datetime.today()
                for x in range(6):
                    import random
                    start_date = start_date
                    leads_added = Leads.objects.filter(dra=user, lsq_created_on__lte=start_date,mandate_status="Disbursed").count()
                    data[start_date.strftime('%d %b')]=leads_added
                    start_date = start_date - datetime.timedelta(days=1)
            return Response(data={'success': True, 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'success': True, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def get_app_downloads(self, request):
        """
        Get overall conversion
        """
        try:
            user = request.user
            filter_by = request.query_params.get("days", None)
            from django.db.models import Count
            if (filter_by and filter_by.isdigit()) and (filter_by == '30' or filter_by == '60' or filter_by == '90'):
                import datetime
                filter_date = datetime.datetime.today() - datetime.timedelta(days=int(filter_by))
                app_downloaded_yes = Leads.objects.filter(dra=user, created_at__date__gte=filter_date.date(),app_downloaded=True).count()
                app_downloaded_no = Leads.objects.filter(dra=user, created_at__date__gte=filter_date.date(), app_downloaded=False).count()
                total_leads = Leads.objects.filter(dra=user).count()
                app_downloaded_yes_percentage = 0 if total_leads == 0 else  round(app_downloaded_yes/total_leads*100, 1)
                app_downloaded_no_percentage = 0 if total_leads == 0 else  round(app_downloaded_no/total_leads*100, 1)
                data = {
                    'yes' : app_downloaded_yes_percentage,
                    'no' : app_downloaded_no_percentage,
                }
            else:
                app_downloaded_yes = Leads.objects.filter(dra=user, app_downloaded=True).count()
                app_downloaded_no = Leads.objects.filter(dra=user, app_downloaded=False).count()
                total_leads = Leads.objects.filter(dra=user).count()
                app_downloaded_yes_percentage = 0 if total_leads == 0 else  round(app_downloaded_yes/total_leads*100, 1)
                app_downloaded_no_percentage = 0 if total_leads == 0 else  round(app_downloaded_no/total_leads*100, 1)
                data = {
                    'yes' : app_downloaded_yes_percentage,
                    'no' : app_downloaded_no_percentage,
                }
            return Response(data={'success': True, 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'success': True, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_total_mandates(self, request):
        """
        Get overall conversion
        """
        try:
            import datetime
            user = request.user
            filter_by = request.query_params.get("days", None)
            to_date=request.query_params.get("to_date", None)
            from_date=request.query_params.get("from_date", None)
            from django.db.models import Count
            if (filter_by and filter_by.isdigit()) and (filter_by == '30' or filter_by == '60' or filter_by == '90'):
                filter_date = datetime.datetime.today() - datetime.timedelta(days=int(filter_by))
                not_initiated = Leads.objects.filter(dra=user, created_at__date__gte=filter_date.date(),mandate_status="Not Initiated").count()
                in_Process = Leads.objects.filter(dra=user, created_at__date__gte=filter_date.date(),mandate_status="In-Process").count()
                rejected = Leads.objects.filter(dra=user, created_at__date__gte=filter_date.date(),mandate_status="Rejected").count()
                disbursed = Leads.objects.filter(dra=user, created_at__date__gte=filter_date.date(),mandate_status="Disbursed").count()
                data = {
                    'Not Initiated' : not_initiated,
                    'In-Process' : in_Process,
                    'Rejected' : rejected,
                    'Disbursed' : disbursed,
                }
            elif to_date and from_date:
                not_initiated = Leads.objects.filter(dra=user, created_at__date__gte=from_date, created_at__date__lte=to_date,mandate_status="Not Initiated").count()
                in_Process = Leads.objects.filter(dra=user, created_at__date__gte=from_date, created_at__date__lte=to_date,mandate_status="In-Process").count()
                rejected = Leads.objects.filter(dra=user, created_at__date__gte=from_date, created_at__date__lte=to_date,mandate_status="Rejected").count()
                disbursed = Leads.objects.filter(dra=user, created_at__date__gte=from_date, created_at__date__lte=to_date,mandate_status="Disbursed").count()
                data = {
                    'Not Initiated' : not_initiated,
                    'In-Process' : in_Process,
                    'Rejected' : rejected,
                    'Disbursed' : disbursed,
                }
            else:
                not_initiated = Leads.objects.filter(dra=user,mandate_status="Not Initiated").count()
                in_Process = Leads.objects.filter(dra=user,mandate_status="In-Process").count()
                rejected = Leads.objects.filter(dra=user,mandate_status="Rejected").count()
                disbursed = Leads.objects.filter(dra=user,mandate_status="Disbursed").count()
                data = {
                    'Not Initiated' : not_initiated,
                    'In-Process' : in_Process,
                    'Rejected' : rejected,
                    'Disbursed' : disbursed,
                }
            return Response(data={'success': True, 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'success': True, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def get_conversion(self, request):
        """
        Get overall conversion
        """
        try:
            user = request.user
            filter_by = request.query_params.get("days", None)
            from django.db.models import Count
            if (filter_by and filter_by.isdigit()) and (filter_by == '30' or filter_by == '60' or filter_by == '90'):
                import datetime
                filter_date = datetime.datetime.today() - datetime.timedelta(days=int(filter_by))
                data = Leads.objects.filter(dra=user, created_at__date__gte=filter_date.date()).values("source_medium").annotate(count=Count("source_medium"))
            else:
                data = Leads.objects.filter(dra=user).values("source_medium").annotate(count=Count("source_medium"))
            data = sorted(data, key=lambda i: i['count'], reverse=True)
            total = 0
            for elem in data:
                total += elem['count']

            for elem in data:
                elem['percentage']=round(elem['count']/total*100)
            return Response(data={'success': True, 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'success': False, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def get_conversion_stage(self, request):
        """
        Get overall incentive stage
        """
        try:
            user = request.user
            filter_by = request.query_params.get("days", None)
            from django.db.models import Count
            if (filter_by and filter_by.isdigit()) and (filter_by == '30' or filter_by == '60' or filter_by == '90'):
                import datetime
                filter_date = datetime.datetime.today() - datetime.timedelta(days=int(filter_by))
                data = Leads.objects.filter(dra=user, created_at__date__gte=filter_date.date()).values("mx_diy_stage").annotate(count=Count("mx_diy_stage"))
            else:
                data = Leads.objects.filter(dra=user).values("mx_diy_stage").annotate(count=Count("mx_diy_stage"))
            data = sorted(data, key=lambda i: i['count'], reverse=True)
            total = 0
            for elem in data:
                total += elem['count']

            for elem in data:
                elem['percentage']=round(elem['count']/total*100)
            return Response(data={'success': True, 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'success': True, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def get_brokerage(self, request):
        """
        Get overall brokarage
        """
        try:
            import datetime
            user = request.user
            filter_by = request.query_params.get("days", 30)

            try:
                from_date = request.query_params.get("from_date", 30)
                to_date = request.query_params.get("to_date", 30)
                if from_date and to_date:
                    from_date  = datetime.datetime.strptime(from_date,"%d-%m-%Y")
                    to_date  = datetime.datetime.strptime(to_date,"%d-%m-%Y")
                    dd = from_date-to_date
                    filter_by = dd.days
                else:
                    from_date = datetime.datetime.today()
            except:
                from_date = datetime.datetime.today()

            filter_date = from_date - datetime.timedelta(days=int(filter_by))
            delta = int(filter_by) / 6
            data = {}
            start_date = filter_date
            for x in range(6):
                start_date = start_date + datetime.timedelta(days=int(delta))
                brokerage = (Brokerage.objects.filter(dra=user, api_updated_date__lte= start_date)).aggregate(Sum('total_cummulative_brokerage'))
                data[start_date.strftime('%d %b')] = brokerage['total_cummulative_brokerage__sum']
                
            return Response(data={'success': True, 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'success': True, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def get_incentive(self, request):
        """
        Get overall incentive
        """
        try:
            user = request.user
            filter_by = request.query_params.get("days", 30)
            import datetime
            try:
                from_date = request.query_params.get("from_date", 30)
                to_date = request.query_params.get("to_date", 30)
                if from_date and to_date:
                    from_date  = datetime.datetime.strptime(from_date,"%d-%m-%Y")
                    to_date  = datetime.datetime.strptime(to_date,"%d-%m-%Y")
                    dd = from_date-to_date
                    filter_by = dd.days
                else:
                    from_date = datetime.datetime.today()
            except:
                from_date = datetime.datetime.today()

            filter_date = from_date - datetime.timedelta(days=int(filter_by))
            delta = int(filter_by) / 6
            data = {}
            start_date = filter_date
            for x in range(6):
                start_date = start_date + datetime.timedelta(days=int(delta))
                incentive = (Incentive.objects.filter(dra=user, created_at__lte= start_date)).aggregate(Sum('incentive_amount'))
                data[start_date.strftime('%d %b')] = incentive['incentive_amount__sum']

            return Response(data={'success': True, 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'success': True, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def send_leads_reminder(self, request):
        try:
            from account.utils import whatsapp_opt_in, send_whatsapp_message, send_mail
            data = request.data
            mobile = data.get("mobile")
            email = data.get("email")
            first_name = data.get("first_name")
            last_name = data.get("last_name")
            whatsapp_opt_in(mobile)
            message = "Dear customer, thank you for choosing JM Financial as your preferred online trading partner. You can start using your account by downloading the BlinkTrade app.\
                \nClick here to download:\
                \nAndroid: Android\
                \niOS: IOS"
            send_whatsapp_message(mobile, message=message)
            msg_body = get_template('email/reminder-dra-leads.html').render({"name": first_name})
            dict_to_send = {
                "emails": email,
                "subject": "JM FINANCIAL- Reminder !",
                "msg_body": msg_body
            }
            send_mail(**dict_to_send)
            return Response(data={'success': True, 'message': "reminder send succesfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_total_brokerage_and_incentive(self, request):
        """
        Get overall incentive
        """
        try:
            user = request.user
            filter_by = request.query_params.get("days", 30)
            import datetime
            try:
                from_date = request.query_params.get("from_date", 30)
                to_date = request.query_params.get("to_date", 30)
                if from_date and to_date:
                    from_date  = datetime.datetime.strptime(from_date,"%d-%m-%Y")
                    to_date  = datetime.datetime.strptime(to_date,"%d-%m-%Y")
                    dd = from_date-to_date
                    filter_by = dd.days
                else:
                    from_date = datetime.datetime.today()
            except:
                from_date = datetime.datetime.today()

            filter_date = from_date - datetime.timedelta(days=int(filter_by))
            delta = int(filter_by) / 6
            data = {}
            start_date = filter_date
            
            for x in range(6):
                start_date = start_date + datetime.timedelta(days=int(delta))
                incentive = (Incentive.objects.filter(dra=user, created_at__lte=start_date)).aggregate(Sum('incentive_amount'))
                brokerage = (Brokerage.objects.filter(dra=user, api_updated_date__lte=start_date)).aggregate(Sum('total_cummulative_brokerage'))
                
                total_incentive = incentive['incentive_amount__sum']
                total_brokerage = brokerage['total_cummulative_brokerage__sum']
                if not total_incentive:
                    total_incentive = 0
                
                if not total_brokerage:
                    total_brokerage = 0

                data[start_date.strftime('%d %b')] = total_incentive + total_brokerage

            return Response(data={'success': True, 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'success': True, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DRALeadsView(ListAPIView):
    """
    DRA Leads list allow only GET method.
    """
    authentication_classes = (SessionAuthentication,JWTAuthentication)
    permission_classes = [IsAuthenticated]

    serializer_class = LeadsSerializer
    pagination_class = DRA_LeadsPagination

    def get_queryset(self):
        query = self.request.GET.get('name',None)
        user = self.request.user
        filter_by = self.request.query_params.get("days", None)
        to_date=self.request.query_params.get("to_date", None)
        from_date=self.request.query_params.get("from_date", None)

        # get all rm of the dra
        all_rm = User.objects.filter(reporting_manager=user)

        if (filter_by and filter_by.isdigit()) and (filter_by == '30' or filter_by == '60' or filter_by == '90'):
            import datetime
            filter_date = datetime.datetime.today() - datetime.timedelta(days=int(filter_by))
            # get all leads of the dra and the rm of the dra
            queryset = Leads.objects.filter(Q(dra=user)|Q(dra__in=all_rm),created_at__date__gte=filter_date).order_by("-created_at")
        elif to_date and from_date:     
            queryset = Leads.objects.filter(Q(dra=user)|Q(dra__in=all_rm),created_at__date__gte=from_date, created_at__date__lte=to_date).order_by("-created_at")
        else:
            queryset = Leads.objects.filter(Q(dra=user)|Q(dra__in=all_rm)).order_by("-created_at")
        
        if query and (query != '' and query != 'null'):
            queryset = queryset.filter(Q(first_name__icontains=query)|Q(last_name__icontains=query)|Q(email__icontains=query)|Q(phone__icontains=query))
        return queryset

class DRA_Add_LeadsView(viewsets.ViewSet):
    """
    DRA add Leads allow only POST method.
    """
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )

    def create_Lead(self, request):
        """
        Get overall overview
        """
        try:
            user = request.user
            data = request.data
            first_name = data.get('name')
            mobile = data.get("mobile")
            email = data.get("email")
            lead = Leads.objects.create(dra=user,first_name=first_name,phone=mobile,email=email)
            lead.save()

            return Response(data={'success': True, 'msg': 'Successfully Created'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'success': True, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

import base64
import json
class DRA_Add_share_LeadsView(viewsets.ViewSet):
    """
    DRA add Leads allow only POST method.
    """
    # authentication_classes = (JWTAuthentication, SessionAuthentication)
    # permission_classes = (IsAuthenticated, )
    
    def create_share_Lead(self, request):
        """
        Get overall overview
        """
        try:
            # user = request.user
            data = request.data
            name = data.get('name')
            mobile = data.get("mobile")
            email = data.get("email")
            data = data.get("data")
            encoded_str = data
            decoded_bytes = base64.b64decode(encoded_str)
            decoded_str = decoded_bytes.decode('utf-8')
            json_dict = json.loads(decoded_str)
            dsa_tag = json_dict["user_tag"]
            dsa_mobile=json_dict['user_mobile']
            user=User.objects.get(dra_tag=dsa_tag,mobile=dsa_mobile)            
            lead = Leads.objects.create(dra=user,first_name=name,phone=mobile,email=email)
            lead.save()

            return Response(data={'success': True, 'msg': 'Successfully Created'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'success': True, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class RMJ_Add_LeadsView(viewsets.ViewSet):
    """
    DRA add Leads allow only POST method.
    """
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )

    def create_Lead(self, request):
        """
        Get overall overview
        """
        try:
            user = request.user
            data = request.data
            first_name = data.get('name')
            mobile = data.get("mobile")
            email = data.get("email")
            lead = Leads.objects.create(dra=user,first_name=first_name,phone=mobile,email=email)
            lead.save()

            return Response(data={'success': True, 'msg': 'Successfully Created'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'success': True, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RMJ_Add(viewsets.ViewSet):
    """
    DSA add rmj allow only POST method.
    """
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )
    # serializer_class=RMaddSerializer

    def create_rmj(self, request):
        """
        Get overall overview
        """
        try:
            user = request.user
            data = request.data
            name = data.get('name')
            mobile = data.get("mobile")
            email = data.get("email")
            user_type="rmj"
            emails=User.objects.filter(email=email).exists()
            mobiles=User.objects.filter(mobile=mobile).exists() 
            if name == None:
                return Response(data={'success': True, 'msg': "Name is required"}, status=status.HTTP_400_BAD_REQUEST)
            if emails and mobiles:
                return Response(data={'success': True, 'msg': "Email and Mobile already exists"}, status=status.HTTP_400_BAD_REQUEST)
            elif emails:
                return Response(data={'success': True, 'msg': "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
            elif mobiles:
                return Response(data={'success': True, 'msg': 'Mobile already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
            users=User.objects.create(username=mobile,reporting_manager=user,user_type=user_type,name=name,mobile=mobile,email=email,admin_status="approved")
            user_id = str(users.id)
            rm_code = f"RM{user_id.zfill(7)}"
            user=User.objects.get(id=users.id)
            user.dra_tag=rm_code
            user.save()
            return Response(data={'success': True, 'msg': 'RM Successfully Created'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'success': True, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RMLeadsView(ListAPIView):
    """
    RM Leads list allow only GET method.
    """
    authentication_classes = (SessionAuthentication,JWTAuthentication)
    permission_classes = [IsAuthenticated]

    serializer_class = LeadsSerializer
    pagination_class = DRA_LeadsPagination

    def get_queryset(self):
        query = self.request.GET.get('name',None)
        user = self.request.user
        filter_by = self.request.query_params.get("days", None)
        to_date=self.request.query_params.get('to_date',None)
        from_date=self.request.query_params.get('from_date',None)
        if (filter_by and filter_by.isdigit()) and (filter_by == '30' or filter_by == '60' or filter_by == '90'):
            import datetime
            filter_date = datetime.datetime.today() - datetime.timedelta(days=int(filter_by))
            queryset = Leads.objects.filter(dra=user, created_at__date__gte=filter_date.date()).order_by("-created_at")
        elif to_date and from_date:
            queryset = Leads.objects.filter(dra=user,created_at__date__gte=from_date, created_at__date__lte=to_date).order_by("-created_at")
        else:
            queryset = Leads.objects.filter(dra=user).order_by("-created_at")
        
        if query and (query != '' and query != 'null'):
            queryset = queryset.filter(Q(first_name__icontains=query)|Q(last_name__icontains=query)|Q(email__icontains=query)|Q(phone__icontains=query))
        return queryset


class RMInformationView(ListAPIView):
    """
    RM Information list allow only GET method.
    """
    authentication_classes = (SessionAuthentication,JWTAuthentication)
    permission_classes = [IsAuthenticated]

    serializer_class = MyRmSerializer
    pagination_class = RM_InfoPagination

    def get_queryset(self):
        user = self.request.user
        filter_by = self.request.query_params.get("days", None)
        to_date=self.request.query_params.get('to_date',None)
        from_date=self.request.query_params.get('from_date',None) 
        if (filter_by and filter_by.isdigit()) and (filter_by == '30' or filter_by == '60' or filter_by == '90'):
            import datetime
            # lsq_created_on
            filter_date = datetime.datetime.today() - datetime.timedelta(days=int(filter_by))
            queryset = User.objects.filter(reporting_manager=user, lsq_created_on__date__gte=filter_date.date())
        elif to_date and from_date:
            queryset = User.objects.filter(reporting_manager=user,lsq_created_on__gte=from_date,lsq_created_on__date__lte=to_date)
        else:
            queryset = User.objects.filter(reporting_manager=user)
        # user filter username and reporting_manager is not none

        queryset = User.objects.filter(reporting_manager=user,reporting_manager__isnull=False)
        return queryset
class KnowlageCenterList(ListAPIView):
    """
    List KnowlageCenter allow only GET method.
    """
    serializer_class = KnowlageCenterSerializer
    pagination_class = KnowlageCenterListNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_field = ['category']

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
        }
    
    def get_queryset(self):
        queryset = KnowlageCenter.objects.all()
        cat_slug = self.request.query_params.get('category__slug')
        if cat_slug:
            queryset = queryset.filter(category__slug=str(cat_slug))
            self.pagination_class.page_size = 3
        else:
            self.pagination_class.page_size = 15
        return queryset


class TrendingKnowlageCenter(ListAPIView):
    """
    List KnowlageCenter allow only GET method.
    """
    serializer_class = KnowlageCenterSerializer
    # pagination_class = KnowlageCenterListNumberPagination

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
        }
    
    def get_queryset(self):
        queryset = KnowlageCenter.objects.filter(is_trending=True)[:3]
        return queryset


class KnowlageCenterdetails(viewsets.ViewSet):
    """
    Get KnowlageCenter details allow only GET method.
    """
    def retrive(self, request, slug=None):
        try:
            knowlage = KnowlageCenter.objects.get(slug=str(slug))
            serializer = KnowlageCenterSerializer(knowlage, many=False, context={"request":request})
            return Response(serializer.data)
        except Exception as e:
            return Response(data={"message":str(e)})


class KnowlageAssetsList(viewsets.ViewSet):
    """
    Get Knowlage Assets list allow only GET method.
    """
    def retrive(self, request, slug=None):
        try:
            queryset = KnowlageAssets.objects.filter(knowlage__slug=slug)
            serializer = KnowlageAssetsSerializer(queryset, many=True, context={"request":request})
            return Response(serializer.data)
        except Exception as e:
            return Response(data={"message":str(e)})

class CategoryList(ListAPIView):
    """
    List Category allow only GET method.
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    # pagination_class = CategoryListNumberPagination

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
        }


class TagsList(ListAPIView):
    """
    List Category allow only GET method.
    """
    queryset = Tags.objects.all()[:15]
    serializer_class = TagsSerializer
    # pagination_class = CategoryListNumberPagination

class DRAUserList(ListAPIView):
    """
    DRA User List allow only GET method.
    """
    authentication_classes = (SessionAuthentication,JWTAuthentication)
    permission_classes = [IsAuthenticated]

    serializer_class = DRAUserListSerializer
    pagination_class = DRA_ActivatedUserListPagination

    def get_queryset(self):
        query = self.request.GET.get('name',None)
        user = self.request.user
        filter_by = self.request.query_params.get("days", None)
        if (filter_by and filter_by.isdigit()) and (filter_by == '30' or filter_by == '60' or filter_by == '90'):
            import datetime
            filter_date = datetime.datetime.today() - datetime.timedelta(days=int(filter_by))
            queryset = Leads.objects.filter(dra=user, created_at__date__gte=filter_date.date()).order_by("-created_at")
        else:
            queryset = Leads.objects.filter(dra=user).order_by("-created_at")

        if query and (query != '' and query != 'null'):
            queryset = queryset.filter(Q(first_name__icontains=query)|Q(last_name__icontains=query)|Q(email__icontains=query)|Q(phone__icontains=query))
        return queryset

class DRA_BrokerList(ListAPIView):
    """
    Broker User List allow only GET method.
    """
    authentication_classes = (SessionAuthentication,JWTAuthentication)
    permission_classes = [IsAuthenticated]

    serializer_class = BrokerUserListSerializer
    # pagination_class = DRA_BrokerListPagination

    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.filter(user_type='dra',is_activated=True, is_staff=False, is_superuser=False).order_by('-total_brokerage')[:15]
        if user in queryset:
            pass
        else:
            queryset = queryset[:14].append(user)
        return queryset


class DRA_TotalEarningList(ListAPIView):
    """
    Broker User List allow only GET method.
    """
    authentication_classes = (SessionAuthentication,JWTAuthentication)
    permission_classes = [IsAuthenticated]

    serializer_class = TotalEarningListSerializer
    # pagination_class = DRA_BrokerListPagination

    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.filter(
            user_type='dra',is_activated=True, is_staff=False, is_superuser=False
        ).annotate(
            my_total_earning=(F('total_brokerage')+F('total_kyc'))
        ).order_by('-my_total_earning')[:15]
        if user in queryset:
            pass
        else:
            queryset = queryset[:14].append(user)
        return queryset


class RM_BrokerList(ListAPIView):
    """
    Broker User List allow only GET method.
    """
    authentication_classes = (SessionAuthentication,JWTAuthentication)
    permission_classes = [IsAuthenticated]

    serializer_class = BrokerUserListSerializer
    # pagination_class = DRA_BrokerListPagination

    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.filter(user_type='dra', reporting_manager=user, is_activated=True, is_staff=False, is_superuser=False).order_by('-total_brokerage')[:5]
        return queryset


class DRAKycList(ListAPIView):
    """
    DRA KYC User List allow only GET method.
    """
    authentication_classes = (SessionAuthentication,JWTAuthentication)
    permission_classes = [IsAuthenticated]

    serializer_class = KYCUserListSerializer
    # pagination_class = DRA_KYCListPagination

    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.filter(user_type='dra',is_activated=True, is_staff=False, is_superuser=False).order_by('-total_kyc')[:15]
        if user in queryset:
            pass
        else:
            queryset = queryset[:14].append(user)
        return queryset


class RMKycList(ListAPIView):
    """
    RM KYC User List allow only GET method.
    """
    authentication_classes = (SessionAuthentication,JWTAuthentication)
    permission_classes = [IsAuthenticated]

    serializer_class = KYCUserListSerializer
    # pagination_class = DRA_KYCListPagination

    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.filter(user_type='dra', reporting_manager=user,is_activated=True, is_staff=False, is_superuser=False).order_by('-total_kyc')[:5]
        return queryset


class ReferralsList(ListAPIView):
    """
    RM Referrals List allow only GET method.
    """
    authentication_classes = (SessionAuthentication,JWTAuthentication)
    permission_classes = [IsAuthenticated]

    serializer_class = KYCUserListSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.filter(reporting_manager=user,is_activated=True, is_staff=False, is_superuser=False).order_by('-total_kyc')[:5]
        return queryset
    

class SettlementList(ListAPIView):
    """
    Settlement List allow only GET method.
    """
    authentication_classes = (SessionAuthentication,JWTAuthentication)
    permission_classes = [IsAuthenticated]
    serializer_class = SettlementListSerializer
    pagination_class = DRA_KYCListPagination

    def get_queryset(self, **kwargs):
        user = self.request.user
        qq = Settlement.objects.filter(dra=user).order_by('-created_at')
        return qq


class PayoutPage(ListAPIView):
    """
    Payout List allow only GET method.
    """
    authentication_classes = (SessionAuthentication,JWTAuthentication)
    permission_classes = [IsAuthenticated]

    serializer_class = PayoutPageSerializer
    pagination_class = DRA_PayOutPagination
    filter_backends = [DjangoFilterBackend]
    filterset_field = ['voucher_date']

    def get_queryset(self):
        user = self.request.user
        day = self.request.query_params.get("days", None)
        to_date=self.request.query_params.get("to_date", None)
        from_date=self.request.query_params.get("from_date", None)
        if (day and day.isdigit()) and (day == '30' or day == '60' or day == '90'):
            import datetime
            filter_date = datetime.datetime.today() - datetime.timedelta(days=int(day))
            queryset = Payout.objects.filter(dra=user, voucher_date__date__gte=filter_date.date()).order_by("-voucher_date")
        elif to_date and from_date:
            queryset = Payout.objects.filter(dra=user, voucher_date__date__gte=from_date,voucher_date__date__lte=to_date,).order_by("-voucher_date")
        else:
            queryset = Payout.objects.filter(dra=user).order_by("-voucher_date")
        return queryset


class PayoutInfo(ListAPIView):
    """
    Payout Info allow only GET method.
    """
    authentication_classes = (SessionAuthentication,JWTAuthentication)
    permission_classes = [IsAuthenticated]

    serializer_class = PayoutInfoSerializer

    def get_queryset(self):
        user = self.request.user
        data = [{
                "incentive": str(user.incentive_perlead),
                "brokerage": str(user.brokerage_percentage)
                }]
        return data

class RMSignUpList(ListAPIView):
    """
    Payout List allow only GET method.
    """
    authentication_classes = (SessionAuthentication,JWTAuthentication)
    permission_classes = [IsAuthenticated]

    serializer_class = RMSignUpListSerializer
    pagination_class = DRA_PayOutPagination

    def get_queryset(self):
        user = self.request.user
        day = self.request.query_params.get("days", None)
        if (day and day.isdigit()) and (day == '30' or day == '60' or day == '90'):
            import datetime
            filter_date = datetime.datetime.today() - datetime.timedelta(days=int(day))
            queryset = User.objects.filter(user_type='dra', reporting_manager=user, is_staff=False, is_superuser=False, date_joined__date__gte=filter_date.date()).order_by("-date_joined")
        else:
            queryset = User.objects.filter(user_type='dra', reporting_manager=user, is_staff=False, is_superuser=False).order_by("-date_joined")
        return queryset




class RMSignupView(viewsets.ViewSet):
    """
    RM dashboard signup page APIs
    """

    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )

    def update_user_incentive_percentage(self, request):
        """
        update user's dra list
        """
        try:
            user = request.user
            data = request.data
            dra_user = None
            try:
                # dra_user = User.objects.get(reporting_manager=user, username=data.get("username"))
                dra_user = User.objects.get(username=data.get("username"))
            except User.DoesNotExist:
                return Response(data={'success': True, 'msg': "this user does not exists"}, status=status.HTTP_404_NOT_FOUND)

            dra_user.incentive_perlead = data.get("incentive_per_lead")
            dra_user.brokerage_percentage = data.get("brokerage_percentage")
            dra_user.remark = data.get("term_condition")
            dra_user.admin_status = 'submitted'
            dra_user.save()
            return Response(data={'success': True, 'message': "dra incentive save successfuly"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'success': True, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# --------------------- RM APIs-------------------------------

class RMActivatedUserList(ListAPIView):
    """
    RM User List allow only GET method.
    """
    authentication_classes = (SessionAuthentication,JWTAuthentication)
    permission_classes = [IsAuthenticated]

    serializer_class = DRAUserListSerializer
    pagination_class = DRA_ActivatedUserListPagination

    def get_queryset(self):
        query = self.request.GET.get('name',None)
        user = self.request.user
        filter_by = self.request.query_params.get("days", None)
        if (filter_by and filter_by.isdigit()) and (filter_by == '30' or filter_by == '60' or filter_by == '90'):
            import datetime
            filter_date = datetime.datetime.today() - datetime.timedelta(days=int(filter_by))
            queryset = Leads.objects.filter(dra__reporting_manager=user, created_at__date__gte=filter_date.date()).order_by("-created_at")
        else:
            queryset = Leads.objects.filter(dra__reporting_manager=user).order_by("-created_at")

        if query and (query != '' and query != 'null'):
            queryset = queryset.filter(Q(first_name__icontains=query)|Q(last_name__icontains=query)|Q(email__icontains=query)|Q(phone__icontains=query))
        return queryset

class RMSettlement(ListAPIView):
    """
    RM Payout List allow only GET method.
    """
    authentication_classes = (SessionAuthentication,JWTAuthentication)
    permission_classes = [IsAuthenticated]

    serializer_class = SettlementListSerializer
    pagination_class = DRA_PayOutPagination
    filter_backends = [DjangoFilterBackend]
    filterset_field = ['voucher_date']

    def get_queryset(self):
        user = self.request.user
        day = self.request.query_params.get("days", None)
        if (day and day.isdigit()) and (day == '30' or day == '60' or day == '90'):
            import datetime
            filter_date = datetime.datetime.today() - datetime.timedelta(days=int(day))
            dra_user_list = User.objects.filter(reporting_manager=user, is_activated=True, is_staff=False, is_superuser=False)
            queryset = Settlement.objects.filter(dra__in=dra_user_list, created_at__date__gte=filter_date.date()).order_by('-created_at')
        else:
            dra_user_list = User.objects.filter(reporting_manager=user, is_activated=True, is_staff=False, is_superuser=False)
            queryset = Settlement.objects.filter(dra__in=dra_user_list).order_by('-created_at')
        return queryset


class RMPayout(ListAPIView):
    """
    RM Payout List allow only GET method.
    """
    authentication_classes = (SessionAuthentication,JWTAuthentication)
    permission_classes = [IsAuthenticated]

    serializer_class = PayoutPageSerializer
    pagination_class = DRA_PayOutPagination
    filter_backends = [DjangoFilterBackend]
    filterset_field = ['voucher_date']

    def get_queryset(self):
        user = self.request.user
        day = self.request.query_params.get("days", None)
        if (day and day.isdigit()) and (day == '30' or day == '60' or day == '90'):
            import datetime
            filter_date = datetime.datetime.today() - datetime.timedelta(days=int(day))
            queryset = Payout.objects.filter(dra__reporting_manager=user, voucher_date__date__gte=filter_date.date()).order_by("-voucher_date")
        else:
            queryset = Payout.objects.filter(dra__reporting_manager=user).order_by("-voucher_date")
        return queryset


class RMOpportunities(ListAPIView):
    """
    opportunities allow only GET method.
    """
    authentication_classes = (SessionAuthentication,JWTAuthentication)
    permission_classes = [IsAuthenticated]

    serializer_class = RMOpportunitiesSerializer
    pagination_class = DRA_PayOutPagination

    def get_queryset(self):
        user = self.request.user
        dra_user_list = User.objects.filter(user_type='dra', reporting_manager=user)
        day = self.request.query_params.get("days", None)
        if (day and day.isdigit()) and (day == '30' or day == '60' or day == '90'):
            import datetime
            filter_date = datetime.datetime.today() - datetime.timedelta(days=int(day))
            queryset = Leads.objects.filter(dra__in=dra_user_list, created_at__date__gte=filter_date.date()).order_by('-created_at')
        else:
            queryset = Leads.objects.filter(dra__in=dra_user_list).order_by('-created_at')
        return queryset


class RMDashbardView(viewsets.ViewSet):

    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )

    def get_overview(self, request):
        """
        Get overall overview
        """
        try:
            user = request.user
            filter_by = request.query_params.get("days", None)
            to_date=request.query_params.get("to_date", None)
            from_date=request.query_params.get("from_date", None)
            if (filter_by and filter_by.isdigit()) and (filter_by == '30' or filter_by == '60' or filter_by == '90'):
                import datetime
                filter_date = datetime.datetime.today() - datetime.timedelta(days=int(filter_by))
                total_leads_added = Leads.objects.filter(dra__reporting_manager=user, created_at__date__gte=filter_date.date()).count()
                pending_mandate = Leads.objects.filter(dra__reporting_manager=user, created_at__date__gte=filter_date.date(),mandate_status="In-Process").count()
                rejected_lead = Leads.objects.filter(dra__reporting_manager=user, created_at__date__gte=filter_date.date(),mandate_status='Rejected').count()
                successful_mandate= Leads.objects.filter(dra__reporting_manager=user, created_at__date__gte=filter_date.date(), mandate_status="Disbursed").count()
                data = {
                    "total_leads_added": total_leads_added,
                    "pending_mandate": pending_mandate,
                    "rejected_lead": rejected_lead,
                    "successful_mandate":successful_mandate,
                    "success_rate": 0 if total_leads_added == 0 else round(successful_mandate/total_leads_added*100, 1),
                }

            elif to_date and from_date:
                total_leads_added = Leads.objects.filter(dra__reporting_manager=user, created_at__date__gte=from_date, created_at__date__lte=to_date).count()
                pending_mandate = Leads.objects.filter(dra__reporting_manager=user, created_at__date__gte=from_date, created_at__date__lte=to_date,mandate_status="In-Process").count()
                rejected_lead = Leads.objects.filter(dra__reporting_manager=user, created_at__date__gte=from_date, created_at__date__lte=to_date,mandate_status='Rejected').count()
                successful_mandate= Leads.objects.filter(dra__reporting_manager=user, created_at__date__gte=from_date, created_at__date__lte=to_date, mandate_status="Disbursed").count()
                data = {
                    "total_leads_added": total_leads_added,
                    "pending_mandate": pending_mandate,
                    "rejected_lead": rejected_lead,
                    "successful_mandate":successful_mandate,
                    "success_rate": 0 if total_leads_added == 0 else round(successful_mandate/total_leads_added*100, 1),
                }
            else:
                total_leads_added = Leads.objects.filter(dra__reporting_manager=user).count()
                pending_mandate = Leads.objects.filter(dra__reporting_manager=user,mandate_status="In-Process").count()
                rejected_lead = Leads.objects.filter(dra__reporting_manager=user,mandate_status='Rejected').count()
                successful_mandate= Leads.objects.filter(dra__reporting_manager=user,mandate_status="Disbursed").count()
                data = {
                    "total_leads_added": total_leads_added,
                    "pending_mandate": pending_mandate,
                    "rejected_lead": rejected_lead,
                    "successful_mandate":successful_mandate,
                    "success_rate": 0 if total_leads_added == 0 else round(successful_mandate/total_leads_added*100, 1),
                }

            return Response(data={'success': True, 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'success': True, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def get_leads(self, request):
        """
        Get overall leads
        """
        try:
            user = request.user
            filter_by = request.query_params.get("days", None)
            to_date=request.query_params.get("to_date", None)
            from_date=request.query_params.get("from_date", None)
            if (filter_by and filter_by.isdigit()) and (filter_by == '30' or filter_by == '60' or filter_by == '90'):
                import datetime
                filter_date = datetime.datetime.today() - datetime.timedelta(days=int(filter_by))
                delta = int(filter_by) / 6
                data = []
                start_date = filter_date
                for x in range(6):
                    import random
                    start_date = start_date + datetime.timedelta(days=int(delta))
                    leads_added = Leads.objects.filter(dra__reporting_manager=user, lsq_created_on__date__lte= start_date).count()
                    # leads_activated = Leads.objects.filter(dra__reporting_manager=user, lsq_created_on__lte= start_date, mx_diy_stage="Migration Complete").count()
                    data.append(
                        {
                            "month": start_date.strftime('%d %b'),
                            "data": {
                                "added": leads_added,
                                # "activated": leads_activated,
                            }
                        },
                    )
            elif to_date and from_date:
                from datetime import datetime,timedelta
                date_format = "%Y-%m-%d"
                to_dates = datetime.strptime(to_date, date_format).strftime('%d %b')
                from_dates=datetime.strptime(from_date, date_format).strftime('%d %b')
                tos_dates = datetime.strptime(to_date, date_format)
                froms_dates=datetime.strptime(from_date, date_format)
                dates=tos_dates-froms_dates
                data = []
                for x in range(dates.days+1):
                    for_date=froms_dates.strftime('%d %b')
                    leads_added = Leads.objects.filter(dra__reporting_manager=user, lsq_created_on__date=froms_dates).count()
                    data.append(
                        {
                            "month": f'{for_date}',
                            "data": {
                                "added": leads_added,
                            }
                        },
                    )
                    froms_dates = froms_dates + timedelta(days=1)
            else:
                import datetime
                data = []
                for x in range(6):
                    leads_added = Leads.objects.filter(dra__reporting_manager=user).count()
                    # leads_activated = Leads.objects.filter(dra=user, lsq_created_on__lte=start_date, mx_diy_stage="Migration Complete").count()
                    data.append(
                        {
                            "month": datetime.datetime.now().strftime('%d %b'),
                            "data": {
                                "added": leads_added,
                                # "activated": leads_activated,
                            }
                        },
                    )            
            return Response(data={'success': True, 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'success': True, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_app_downloads(self, request):
        """
        Get overall app downloads
        """
        try:
            user = request.user
            filter_by = request.query_params.get("days", None)
            from django.db.models import Count
            if (filter_by and filter_by.isdigit()) and (filter_by == '30' or filter_by == '60' or filter_by == '90'):
                import datetime
                filter_date = datetime.datetime.today() - datetime.timedelta(days=int(filter_by))
                app_downloaded_yes = Leads.objects.filter(dra__reporting_manager=user, created_at__date__gte=filter_date.date(),app_downloaded=True).count()
                app_downloaded_no = Leads.objects.filter(dra__reporting_manager=user, created_at__date__gte=filter_date.date(), app_downloaded=False).count()
                total_leads = Leads.objects.filter(dra__reporting_manager=user).count()
                app_downloaded_yes_percentage = 0 if total_leads == 0 else  round(app_downloaded_yes/total_leads*100, 1)
                app_downloaded_no_percentage = 0 if total_leads == 0 else  round(app_downloaded_no/total_leads*100, 1)
                data = {
                    'yes' : app_downloaded_yes_percentage,
                    'no' : app_downloaded_no_percentage,
                }
            else:
                app_downloaded_yes = Leads.objects.filter(dra__reporting_manager=user, app_downloaded=True).count()
                app_downloaded_no = Leads.objects.filter(dra__reporting_manager=user, app_downloaded=False).count()
                total_leads = Leads.objects.filter(dra__reporting_manager=user).count()
                app_downloaded_yes_percentage = 0 if total_leads == 0 else  round(app_downloaded_yes/total_leads*100, 1)
                app_downloaded_no_percentage = 0 if total_leads == 0 else  round(app_downloaded_no/total_leads*100, 1)
                data = {
                    'yes' : app_downloaded_yes_percentage,
                    'no' : app_downloaded_no_percentage,
                }
            return Response(data={'success': True, 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'success': True, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_total_mandates(self, request):
        """
        Get overall conversion
        """
        try:
            user = request.user
            filter_by = request.query_params.get("days", None)
            to_date=request.query_params.get("to_date", None)
            from_date=request.query_params.get("from_date", None)
            from django.db.models import Count
            if (filter_by and filter_by.isdigit()) and (filter_by == '30' or filter_by == '60' or filter_by == '90'):
                import datetime
                filter_date = datetime.datetime.today() - datetime.timedelta(days=int(filter_by))
                not_initiated = Leads.objects.filter(dra__reporting_manager=user, created_at__date__gte=filter_date.date(),mandate_status="Not Initiated").count()
                in_Process = Leads.objects.filter(dra__reporting_manager=user, created_at__date__gte=filter_date.date(),mandate_status="In-Process").count()
                rejected = Leads.objects.filter(dra__reporting_manager=user, created_at__date__gte=filter_date.date(),mandate_status="Rejected").count()
                disbursed = Leads.objects.filter(dra__reporting_manager=user, created_at__date__gte=filter_date.date(),mandate_status="Disbursed").count()
                data = {
                    'Not Initiated' : not_initiated,
                    'In-Process' : in_Process,
                    'Rejected' : rejected,
                    'Disbursed' : disbursed,
                }
            elif to_date and from_date:
                not_initiated = Leads.objects.filter(dra__reporting_manager=user,created_at__date__gte=from_date,created_at__date__lte=to_date,mandate_status="Not Initiated").count()
                in_Process = Leads.objects.filter(dra__reporting_manager=user,created_at__date__gte=from_date, created_at__date__lte=to_date,mandate_status="In-Process").count()
                rejected = Leads.objects.filter(dra__reporting_manager=user,created_at__date__gte=from_date, created_at__date__lte=to_date,mandate_status="Rejected").count()
                disbursed = Leads.objects.filter(dra__reporting_manager=user,created_at__date__gte=from_date, created_at__date__lte=to_date,mandate_status="Disbursed").count()
                data = {
                    'Not Initiated' : not_initiated,
                    'In-Process' : in_Process,
                    'Rejected' : rejected,
                    'Disbursed' : disbursed,
                }   
            else:
                not_initiated = Leads.objects.filter(dra__reporting_manager=user,mandate_status="Not Initiated").count()
                in_Process = Leads.objects.filter(dra__reporting_manager=user,mandate_status="In-Process").count()
                rejected = Leads.objects.filter(dra__reporting_manager=user,mandate_status="Rejected").count()
                disbursed = Leads.objects.filter(dra__reporting_manager=user,mandate_status="Disbursed").count()
                data = {
                    'Not Initiated' : not_initiated,
                    'In-Process' : in_Process,
                    'Rejected' : rejected,
                    'Disbursed' : disbursed,
                }
            return Response(data={'success': True, 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'success': True, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def get_conversion(self, request):
        """
        Get overall conversion
        """
        try:
            user = request.user
            filter_by = request.query_params.get("days", None)
            from django.db.models import Count
            if (filter_by and filter_by.isdigit()) and (filter_by == '30' or filter_by == '60' or filter_by == '90'):
                import datetime
                filter_date = datetime.datetime.today() - datetime.timedelta(days=int(filter_by))
                data = Leads.objects.filter(dra__reporting_manager=user, created_at__date__gte=filter_date.date()).values("source_medium").annotate(count=Count("source_medium"))
            else:
                data = Leads.objects.filter(dra__reporting_manager=user).values("source_medium").annotate(count=Count("source_medium"))
            data = sorted(data, key=lambda i: i['count'], reverse=True)
            total = 0
            for elem in data:
                total += elem['count']

            for elem in data:
                elem['percentage']=round(elem['count']/total*100)
            return Response(data={'success': True, 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'success': True, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_conversion_stage(self, request):
        """
        Get overall incentive stage
        """
        try:
            user = request.user
            filter_by = request.query_params.get("days", None)
            from django.db.models import Count
            if (filter_by and filter_by.isdigit()) and (filter_by == '30' or filter_by == '60' or filter_by == '90'):
                import datetime
                filter_date = datetime.datetime.today() - datetime.timedelta(days=int(filter_by))
                data = Leads.objects.filter(dra__reporting_manager=user, created_at__date__gte=filter_date.date()).values("mx_diy_stage").annotate(count=Count("mx_diy_stage"))
            else:
                data = Leads.objects.filter(dra__reporting_manager=user).values("mx_diy_stage").annotate(count=Count("mx_diy_stage"))
            data = sorted(data, key=lambda i: i['count'], reverse=True)
            total = 0
            for elem in data:
                total += elem['count']

            for elem in data:
                elem['percentage']=round(elem['count']/total*100)
            return Response(data={'success': True, 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'success': True, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_brokerage(self, request):
        """
        Get overall brokarage
        """
        try:
            user = request.user
            filter_by = request.query_params.get("days", 30)
            import datetime
            try:
                from_date = request.query_params.get("from_date", 30)
                to_date = request.query_params.get("to_date", 30)
                if from_date and to_date:
                    from_date  = datetime.datetime.strptime(from_date,"%d-%m-%Y")
                    to_date  = datetime.datetime.strptime(to_date,"%d-%m-%Y")
                    dd = from_date-to_date
                    filter_by = dd.days
                else:
                    from_date = datetime.datetime.today()
            except:
                from_date = datetime.datetime.today()

            filter_date = from_date - datetime.timedelta(days=int(filter_by))
            delta = int(filter_by) / 6
            data = {}
            start_date = filter_date
            for x in range(6):
                start_date = start_date + datetime.timedelta(days=int(delta))
                brokerage = (Brokerage.objects.filter(dra__reporting_manager=user, api_updated_date__lte= start_date)).aggregate(Sum('total_cummulative_brokerage'))
                data[start_date.strftime('%d %b')] = brokerage['total_cummulative_brokerage__sum']
                
            return Response(data={'success': True, 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'success': True, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_incentive(self, request):
        """
        Get overall incentive
        """
        try:
            user = request.user
            filter_by = request.query_params.get("days", 30)
            import datetime

            try:
                from_date = request.query_params.get("from_date", 30)
                to_date = request.query_params.get("to_date", 30)
                if from_date and to_date:
                    from_date  = datetime.datetime.strptime(from_date,"%d-%m-%Y")
                    to_date  = datetime.datetime.strptime(to_date,"%d-%m-%Y")
                    dd = from_date-to_date
                    filter_by = dd.days
                else:
                    from_date = datetime.datetime.today()
            except:
                from_date = datetime.datetime.today()

            filter_date = from_date - datetime.timedelta(days=int(filter_by))
            delta = int(filter_by) / 6
            data = {}
            start_date = filter_date
            for x in range(6):
                start_date = start_date + datetime.timedelta(days=int(delta))
                incentive = (Incentive.objects.filter(dra__reporting_manager=user, created_at__lte= start_date)).aggregate(Sum('incentive_amount'))
                data[start_date.strftime('%d %b')] = incentive['incentive_amount__sum']

            return Response(data={'success': True, 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'success': True, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_successful_rate(self, request):
        """
        Get overall successful rate
        """
        try:
            user = request.user
            filter_by = request.query_params.get("days", None)
            to_date=request.query_params.get("to_date", None)
            from_date=request.query_params.get("from_date", None)
            if (filter_by and filter_by.isdigit()) and (filter_by == '30' or filter_by == '60' or filter_by == '90'):
                data = {}
                import datetime
                filter_date = datetime.datetime.today() - datetime.timedelta(days=int(filter_by))
                delta = int(filter_by) / 6
                
                start_date = filter_date
                for x in range(6):
                    import random
                    start_date = start_date + datetime.timedelta(days=int(delta))
                    total_leads_added = Leads.objects.filter(dra__reporting_manager=user, lsq_created_on__lte=start_date).count()
                    leads_added = Leads.objects.filter(dra__reporting_manager=user, lsq_created_on__lte=start_date,mandate_status="Disbursed").count()
                    success_rate=0 if total_leads_added == 0 else round(leads_added/total_leads_added*100, 1)
                    data[start_date.strftime('%d %b')]=success_rate

            elif to_date and from_date:
                data = {}
                from datetime import datetime,timedelta
                date_format = "%Y-%m-%d"
                to_dates = datetime.strptime(to_date, date_format).strftime('%d %b')
                from_dates=datetime.strptime(from_date, date_format).strftime('%d %b')
                tos_dates = datetime.strptime(to_date, date_format)
                froms_dates=datetime.strptime(from_date, date_format)
                dates=tos_dates-froms_dates
                for x in range(dates.days+1):
                    for_date=froms_dates.strftime('%d %b')
                    total_leads_added = Leads.objects.filter(dra__reporting_manager=user, lsq_created_on=froms_dates).count()
                    leads_added = Leads.objects.filter(dra__reporting_manager=user, lsq_created_on=froms_dates,mandate_status="Disbursed").count()
                    success_rate=0 if total_leads_added == 0 else round(leads_added/total_leads_added*100, 1)
                    data[for_date]=success_rate
                    froms_dates = froms_dates + timedelta(days=1)

            else:
                data = {}
                import datetime
                start_date = datetime.datetime.today()
                for x in range(6):
                    import random
                    start_date = start_date
                    total_leads_added = Leads.objects.filter(dra__reporting_manager=user, lsq_created_on__lte=start_date).count()
                    leads_added = Leads.objects.filter(dra__reporting_manager=user, lsq_created_on__lte=start_date,mandate_status="Disbursed").count()
                    success_rate=0 if total_leads_added == 0 else round(leads_added/total_leads_added*100, 1)
                    data[start_date.strftime('%d %b')]=success_rate
                    start_date = start_date - datetime.timedelta(days=1)
            return Response(data={'success': True, 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'success': True, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_successful_disbursed(self, request):
        """
        Get overall successful rate
        """
        try:
            data={}
            user = request.user
            filter_by = request.query_params.get("days", None)
            to_date=request.query_params.get("to_date", None)
            from_date=request.query_params.get("from_date", None)
            if (filter_by and filter_by.isdigit()) and (filter_by == '30' or filter_by == '60' or filter_by == '90'):
                import datetime
                filter_date = datetime.datetime.today() - datetime.timedelta(days=int(filter_by))
                delta = int(filter_by) / 6
                start_date = filter_date
                for x in range(6):
                    import random
                    start_date = start_date + datetime.timedelta(days=int(delta))
                    leads_added = Leads.objects.filter(dra__reporting_manager=user, lsq_created_on__lte=start_date,mandate_status="Disbursed").count()
                    data[start_date.strftime('%d %b')]=leads_added

            elif to_date and from_date:
                from datetime import datetime,timedelta
                date_format = "%Y-%m-%d"
                to_dates = datetime.strptime(to_date, date_format).strftime('%d %b')
                from_dates=datetime.strptime(from_date, date_format).strftime('%d %b')
                tos_dates = datetime.strptime(to_date, date_format)
                froms_dates=datetime.strptime(from_date, date_format)
                dates=tos_dates-froms_dates
                for x in range(dates.days+1):
                    for_date=froms_dates.strftime('%d %b')
                    leads_added = Leads.objects.filter(dra__reporting_manager=user, lsq_created_on=froms_dates ,mandate_status="Disbursed").count()
                    data[for_date]=leads_added
                    froms_dates = froms_dates + timedelta(days=1)

            else:
                import datetime
                start_date = datetime.datetime.today()
                for x in range(6):
                    import random
                    start_date = start_date
                    leads_added = Leads.objects.filter(dra__reporting_manager=user, lsq_created_on__lte=start_date,mandate_status="Disbursed").count()
                    data[start_date.strftime('%d %b')]=leads_added
                    start_date = start_date - datetime.timedelta(days=1)
            return Response(data={'success': True, 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'success': True, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class KeywordList(ListAPIView):
    """
    Keyword listing allow only GET method.
    """
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
        }


class TDSView(viewsets.ViewSet):

    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )

    def get_financial_year(self, request):
        """
        Get financial year list
        """
        try:
            res = FinancialYear.objects.all()
            data = [
                {
                    "id": i.id,
                    "name": i.name
                } for i in res
            ]
            return Response(data={'success': True, 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'success': True, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_segments(self, request):
        """
        Get segment lists
        """
        try:
            res = Segment.objects.all()
            data = [
                {
                    "id": i.id,
                    "name": i.name,
                    "slug": i.slug
                } for i in res
            ]
            return Response(data={'success': True, 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'success': True, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_quarters(self, request):
        try:
            res = QUARTER_CHOICES
            data = [
                {
                    "value": i[0],
                    "text": i[1],
                } for i in res
            ]
            return Response(data={'success': True, 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'success': True, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def download_tds(self, request):
        """
        download tds link
        """
        try:
            data = request.data
            financial_year = data.get("financial_year")
            segment = data.get("segment")
            quarter = data.get("quarter")
            fy = FinancialYear.objects.get(name=financial_year)
            seg = Segment.objects.get(slug=segment)
            tds_obj = TDSCertificate.objects.get(financial_year=fy, segment=seg, quarter=quarter)
            download_link = tds_obj.tds_certificate.url
            data = {
                "download_link": download_link
            }
            return Response(data={'success': True, 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'success': True, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RMDetailView(viewsets.ViewSet):

    # authentication_classes = (JWTAuthentication, SessionAuthentication)
    # permission_classes = (IsAuthenticated, )


    def get_rm_details(self, request):
        """
        Get latest banner detail
        """
        try:
            data = request.data
            lead = Leads.objects.filter(prospect_id=data.get("lead_prospect_id")).last()
            lead_dra = lead.dra
            rm = lead_dra.reporting_manager
            if rm:
                res = {
                    "name": rm.name,
                    "email": rm.email,
                    "mobile": rm.mobile
                }
            else:
                res = "RM not assigned"
            return Response(data={'success': True, 'data': res}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'success': True, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RMOpportunitiesTabs(viewsets.ViewSet):
    """
    opportunities allow only GET method.
    """
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )

    def get_dra_inactive_lead_generation(self, request, **kwargs):
        """
        Get inactive lead generations
        """
        try:
            from django.db.models.functions import ExtractMonth, ExtractYear
            from django.db.models import Count
            import calendar
            user = request.user
            dras = User.objects.filter(user_type='dra', reporting_manager=user, admin_status='approved')
            results = []
            current_month = datetime.now()
            previous_month = current_month.replace(day=1) - timedelta(days=1)
            previous_previous_month = previous_month.replace(day=1) - timedelta(days=1)
            current_month_name = f"{calendar.month_name[current_month.month][:3]}-{str(current_month.year)[2:]}"
            previous_month_name = f"{calendar.month_name[previous_month.month][:3]}-{str(previous_month.year)[2:]}"
            previous_previous_month_name = f"{calendar.month_name[previous_previous_month.month][:3]}-{str(previous_previous_month.year)[2:]}"


            headers = [
                "DRA Code", 
                "DRA Name", 
                f"{current_month_name}", 
                f"{previous_month_name}",
                f"{previous_previous_month_name}", 
                "Total Lead Generated", 
                "Average of Quarter"
            ]

            for dra in dras:
                leads = Leads.objects.filter(dra=dra).annotate(
                    month=ExtractMonth('created_at'),
                    year=ExtractYear("created_at")).values("month", "year").annotate(
                        total=Count('id')).values("month", "year", "total").order_by('month')[:3]
                n = {
                    "dra_code": dra.dra_tag,
                    "dra_name": dra.name,
                    f"{current_month_name.replace('-', '_').lower()}": 0,
                    f"{previous_month_name.replace('-', '_').lower()}": 0,
                    f"{previous_previous_month_name.replace('-', '_').lower()}": 0,
                    "total_lead_generated": 0,
                    "average_of_quarter": 0
                }
                t = 0
                for l in leads:
                    n.update({
                        f"{calendar.month_name[l.get('month')][:3].lower()}_{str(l.get('year'))[2:]}": l.get("total")
                    })
                    t = t+l.get("total")
                n.update({
                    "total_lead_generated": t,
                    "average_of_quarter": round(t/3, 0)
                })
                results.append(n)
            data = {
                "headers": headers,
                "data": results
            }
            return Response(data={'success': True, 'data': data}, status=status.HTTP_200_OK)      
        except Exception as e:
            return Response(data={'success': False, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_dra_inactive_account_activation(self, request, **kwargs):
        """
        Get inactive lead generations
        """
        try:
            from django.db.models.functions import ExtractMonth, ExtractYear
            from django.db.models import Count
            import calendar
            user = request.user
            dras = User.objects.filter(user_type='dra', reporting_manager=user, admin_status='approved')
            results = []
            current_month = datetime.now()
            previous_month = current_month.replace(day=1) - timedelta(days=1)
            previous_previous_month = previous_month.replace(day=1) - timedelta(days=1)
            current_month_name = f"{calendar.month_name[current_month.month][:3]}-{str(current_month.year)[2:]}"
            previous_month_name = f"{calendar.month_name[previous_month.month][:3]}-{str(previous_month.year)[2:]}"
            previous_previous_month_name = f"{calendar.month_name[previous_previous_month.month][:3]}-{str(previous_previous_month.year)[2:]}"
            headers = [
                "DRA Code", 
                "DRA Name", 
                f"{current_month_name}", 
                f"{previous_month_name}",
                f"{previous_previous_month_name}",
                "Total Account Activated", 
                "Average of Quarter"
            ]

            for dra in dras:
                leads = Leads.objects.filter(
                    dra=dra,
                    mx_diy_stage="Migration Complete").annotate(
                    month=ExtractMonth('created_at'),
                    year=ExtractYear("created_at")).values("month", "year").annotate(
                        total=Count('id')).values("month", "year", "total").order_by('total')[:3]
                n = {
                    "dra_code": dra.dra_tag,
                    "dra_name": dra.name,
                    f"{current_month_name.replace('-', '_').lower()}": 0,
                    f"{previous_month_name.replace('-', '_').lower()}": 0,
                    f"{previous_previous_month_name.replace('-', '_').lower()}": 0,
                    "total_account_activated": 0,
                    "average_of_quarter": 0
                }
                t = 0
                for l in leads:
                    n.update({
                        f"{calendar.month_name[l.get('month')][:3].lower()}_{str(l.get('year'))[2:]}": l.get("total")
                    })
                    t = t+l.get("total")
                n.update({
                    "total_account_activated": t,
                    "average_of_quarter": round(t/3, 0)
                })
                results.append(n)
            data = {
                "headers": headers,
                "data": results
            }
            return Response(data={'success': True, 'data': data}, status=status.HTTP_200_OK)      
        except Exception as e:
            return Response(data={'success': False, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_dra_inactive_brokerage_generation(self, request, **kwargs):
        """
        Get inactive lead generations
        """
        try:
            from django.db.models.functions import ExtractMonth, ExtractYear
            from django.db.models import Count
            import calendar
            user = request.user
            dras = User.objects.filter(user_type='dra', reporting_manager=user, admin_status='approved')
            results = []
            current_month = datetime.now()
            previous_month = current_month.replace(day=1) - timedelta(days=1)
            previous_previous_month = previous_month.replace(day=1) - timedelta(days=1)
            current_month_name = f"{calendar.month_name[current_month.month][:3]}-{str(current_month.year)[2:]}"
            previous_month_name = f"{calendar.month_name[previous_month.month][:3]}-{str(previous_month.year)[2:]}"
            previous_previous_month_name = f"{calendar.month_name[previous_previous_month.month][:3]}-{str(previous_previous_month.year)[2:]}"
            headers = [
                "DRA Code", 
                "DRA Name", 
                f"{current_month_name}", 
                f"{previous_month_name}",
                f"{previous_previous_month_name}", 
                "Total Brokerage Generated", 
                "Average of Quarter"
            ]
            for dra in dras:
                brokarage_data = Brokerage.objects.filter(dra=dra).annotate(
                month=ExtractMonth('created_at'), year=ExtractYear("created_at")
                ).values("month", "year").annotate(
                    total=Sum('total_cumulative_net_brokerage')).values("month", "year", "total").order_by("month")[:3]
                n = {
                    "dra_code": dra.dra_tag,
                    "dra_name": dra.name,
                    f"{current_month_name.replace('-', '_').lower()}": 0,
                    f"{previous_month_name.replace('-', '_').lower()}": 0,
                    f"{previous_previous_month_name.replace('-', '_').lower()}": 0,
                    "total_brokerage_generated": 0,
                    "average_of_quarter": 0
                }
                t = 0
                for b in brokarage_data:
                    n.update({
                        f"{calendar.month_name[b.get('month')][:3].lower()}_{str(b.get('year'))[2:]}": b.get("total")
                    })
                    t = t+b.get("total")
                n.update({
                    "total_brokerage_generated": t,
                    "average_of_quarter": round(t/3, 0)
                })
                results.append(n)
            data = {
                "headers": headers,
                "data": results
            }
            return Response(data={'success': True, 'data': data}, status=status.HTTP_200_OK)      
        except Exception as e:
            return Response(data={'success': False, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_dra_downfall_account_activation(self, request, **kwargs):
        """
        Get inactive lead generations
        """
        try:
            from django.db.models.functions import ExtractMonth, ExtractYear
            from django.db.models import Count
            import calendar
            user = request.user
            dras = User.objects.filter(user_type='dra', reporting_manager=user, admin_status='approved')
            results = []
            current_month = datetime.now()
            previous_month = current_month.replace(day=1) - timedelta(days=1)
            previous_previous_month = previous_month.replace(day=1) - timedelta(days=1)
            current_month_name = f"{calendar.month_name[current_month.month][:3]}-{str(current_month.year)[2:]}"
            previous_month_name = f"{calendar.month_name[previous_month.month][:3]}-{str(previous_month.year)[2:]}"
            previous_previous_month_name = f"{calendar.month_name[previous_previous_month.month][:3]}-{str(previous_previous_month.year)[2:]}"
            headers = [
                "DRA Code", 
                "DRA Name", 
                f"{current_month_name}", 
                f"{previous_month_name}",
                f"{previous_previous_month_name}",
                "Total Account Activated", 
                "Average of Quarter"
            ]

            for dra in dras:
                leads = Leads.objects.filter(
                    dra=dra,
                    mx_diy_stage="Migration Complete").annotate(
                    month=ExtractMonth('created_at'),
                    year=ExtractYear("created_at")).values("month", "year").annotate(
                        total=Count('id')).values("month", "year", "total").order_by('total')[:3]
                n = {
                    "dra_code": dra.dra_tag,
                    "dra_name": dra.name,
                    f"{current_month_name.replace('-', '_').lower()}": 0,
                    f"{previous_month_name.replace('-', '_').lower()}": 0,
                    f"{previous_previous_month_name.replace('-', '_').lower()}": 0,
                    "total_account_activated": 0,
                    "average_of_quarter": 0
                }
                t = 0
                for l in leads:
                    n.update({
                        f"{calendar.month_name[l.get('month')][:3].lower()}_{str(l.get('year'))[2:]}": l.get("total")
                    })
                    t = t+l.get("total")
                n.update({
                    "total_account_activated": t,
                    "average_of_quarter": round(t/3, 0)
                })
                results.append(n)
            data = {
                "headers": headers,
                "data": results
            }
            return Response(data={'success': True, 'data': data}, status=status.HTTP_200_OK)      
        except Exception as e:
            return Response(data={'success': False, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_dra_downfall_brokerage_generation(self, request, **kwargs):
        """
        Get inactive lead generations
        """
        try:
            from django.db.models.functions import ExtractMonth, ExtractYear
            from django.db.models import Count
            import calendar
            user = request.user
            dras = User.objects.filter(user_type='dra', reporting_manager=user, admin_status='approved')
            results = []
            current_month = datetime.now()
            previous_month = current_month.replace(day=1) - timedelta(days=1)
            previous_previous_month = previous_month.replace(day=1) - timedelta(days=1)
            current_month_name = f"{calendar.month_name[current_month.month][:3]}-{str(current_month.year)[2:]}"
            previous_month_name = f"{calendar.month_name[previous_month.month][:3]}-{str(previous_month.year)[2:]}"
            previous_previous_month_name = f"{calendar.month_name[previous_previous_month.month][:3]}-{str(previous_previous_month.year)[2:]}"
            headers = [
                "DRA Code", 
                "DRA Name", 
                f"{current_month_name}", 
                f"{previous_month_name}",
                f"{previous_previous_month_name}", 
                "Total Brokerage Generated", 
                "Average of Quarter"
            ]
            for dra in dras:
                brokarage_data = Brokerage.objects.filter(dra=dra).annotate(
                month=ExtractMonth('created_at'), year=ExtractYear("created_at")
                ).values("month", "year").annotate(
                    total=Sum('total_cumulative_net_brokerage')).values("month", "year", "total").order_by("-total")[:3]
                n = {
                    "dra_code": dra.dra_tag,
                    "dra_name": dra.name,
                    f"{current_month_name.replace('-', '_').lower()}": 0,
                    f"{previous_month_name.replace('-', '_').lower()}": 0,
                    f"{previous_previous_month_name.replace('-', '_').lower()}": 0,
                    "total_brokerage_generated": 0,
                    "average_of_quarter": 0
                }
                t = 0
                for b in brokarage_data:
                    n.update({
                        f"{calendar.month_name[b.get('month')][:3].lower()}_{str(b.get('year'))[2:]}": b.get("total")
                    })
                    t = t+b.get("total")
                n.update({
                    "total_brokerage_generated": t,
                    "average_of_quarter": round(t/3, 0)
                })
                results.append(n)
            data = {
                "headers": headers,
                "data": results
            }
            return Response(data={'success': True, 'data': data}, status=status.HTTP_200_OK)      
        except Exception as e:
            return Response(data={'success': False, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_dra_degrowth_lead(self, request, **kwargs):
        """
        Get inactive lead generations
        """
        try:
            from django.db.models.functions import ExtractMonth, ExtractYear
            from django.db.models import Count
            import calendar
            user = request.user
            dras = User.objects.filter(user_type='dra', reporting_manager=user, admin_status='approved')
            results = []
            current_month = datetime.now()
            previous_month = current_month.replace(day=1) - timedelta(days=1)
            previous_previous_month = previous_month.replace(day=1) - timedelta(days=1)
            current_month_name = f"{calendar.month_name[current_month.month][:3]}-{str(current_month.year)[2:]}"
            previous_month_name = f"{calendar.month_name[previous_month.month][:3]}-{str(previous_month.year)[2:]}"
            previous_previous_month_name = f"{calendar.month_name[previous_previous_month.month][:3]}-{str(previous_previous_month.year)[2:]}"

            headers = [
                "DRA Code", 
                "DRA Name", 
                f"{current_month_name}", 
                f"{previous_month_name}",
                f"{previous_previous_month_name}",
                "Total Leads", 
                "Average of Quarter"
            ]
            for dra in dras:
                leads = Leads.objects.filter(
                    dra=dra).annotate(
                    month=ExtractMonth('created_at'),
                    year=ExtractYear("created_at")).values("month", "year").annotate(
                        total=Count('id')).values("month", "year", "total").order_by('total')[:3]
                n = {
                    "dra_code": dra.dra_tag,
                    "dra_name": dra.name,
                    f"{current_month_name.replace('-', '_').lower()}": 0,
                    f"{previous_month_name.replace('-', '_').lower()}": 0,
                    f"{previous_previous_month_name.replace('-', '_').lower()}": 0,
                    "total_leads": 0,
                    "average_of_quarter": 0
                }
                t = 0
                for l in leads:
                    n.update({
                        f"{calendar.month_name[l.get('month')][:3].lower()}_{str(l.get('year'))[2:]}": l.get("total")
                    })
                    t = t+l.get("total")
                n.update({
                    "total_leads": t,
                    "average_of_quarter": round(t/3, 0)
                })
                results.append(n)
            data = {
                "headers": headers,
                "data": results
            }
            return Response(data={'success': True, 'data': data}, status=status.HTTP_200_OK)      
        except Exception as e:
            return Response(data={'success': False, 'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class Leadimport(viewsets.ViewSet):
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )

    
    def import_data(self, request, **kwar):
        """
        Import data
        """
        file = request.FILES['file']
        # print(dir(file))
        if file.content_type == 'text/csv' or file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' or file.content_type == 'application/vnd.ms-excel':
            # print('csv')

            user = request.user
            data = request.data
            dry_run = data.get('dry_run')
            data=Dataset()
            decoded_file = request.FILES['file']
            # imported_data = data.load(decoded_file.read().decode('utf-8'), format='csv')
            imported_data = None
            if file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                imported_data = data.load(decoded_file.read(), format='xlsx')
            elif file.content_type == 'application/vnd.ms-excel':
                imported_data = data.load(decoded_file.read(), format='xls')
            elif file.content_type == 'text/csv':
                imported_data = data.load(decoded_file.read().decode('utf-8'), format='csv')
                
            if dry_run == "False":
                resource=LeadResource(user)
                result = resource.import_data(imported_data,dry_run=False,raise_errors=False,validate=True,skip_unchanged=True,collect_failed_rows=True,report_skipped=False,raise_validation_errors=False)
                results = result.totals
                success_rows = []
                error_rows=[]
                if result.has_errors() or result.has_validation_errors():
                    for reo in result.failed_dataset.dict:
                        error = reo['Error']
                        error_message = ''.join(error).replace("'", "").replace("[", "").replace("]", "")
                        del reo['Error']
                        error_rows.append({'row':reo,'error':error_message})
                    return Response({'success':False,'failed_rows':error_rows,'result':results},status=status.HTTP_400_BAD_REQUEST)
                
                imported_rows = resource.imported_rows
                for row in imported_rows:
                    #append the row and message to success_rows
                    success_rows.append({'row':row,'message':'Successfully Imported'})
                return Response({'success':True,'result':results,'success_row':success_rows},status=status.HTTP_200_OK)
            elif dry_run == "True":
                resource=LeadResource(user)
                result = resource.import_data(imported_data,dry_run=True,raise_errors=False,validate=True,skip_unchanged=True,collect_failed_rows=True,report_skipped=False,raise_validation_errors=False)
                results = result.totals
                success_rows = []
                error_rows=[]
                if result.has_errors() or result.has_validation_errors():
                    for reo in result.failed_dataset.dict:
                        error = reo['Error']
                        error_message = ''.join(error).replace("'", "").replace("[", "").replace("]", "")
                        if ',' in error_message:
                            error_message = error_message.split(',')

                        del reo['Error']
                        error_rows.append({'row':reo,'error':error_message})
                    return Response({'success':False,'failed_rows':error_rows,'result':results},status=status.HTTP_400_BAD_REQUEST)
                
                imported_rows = resource.imported_rows
                for row in imported_rows:
                    #append the row and message to success_rows
                    success_rows.append({'row':row,'message':'Success'})
                return Response({'success':True,'result':results,'success_row':success_rows},status=status.HTTP_200_OK)
        else:
            return Response({'success':False,'message':'File type not supported'},status=status.HTTP_400_BAD_REQUEST)

class LeadRMimport(viewsets.ViewSet):
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )

    
    def import_data(self, request, **kwar):
        """
        Import data
        """
        #  validate the file type
        file = request.FILES['file']
        if file.content_type == 'text/csv' or file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' or file.content_type == 'application/vnd.ms-excel':
            # print('csv')
            user = request.user
            data = request.data
            dry_run = data.get('dry_run')
            data=Dataset()
            decoded_file = request.FILES['file']
            # define a global variable to store the imported data
            imported_data = None
            if file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
                imported_data = data.load(decoded_file.read(), format='xlsx')
            elif file.content_type == 'application/vnd.ms-excel':
                imported_data = data.load(decoded_file.read(), format='xls')
            elif file.content_type == 'text/csv':
                imported_data = data.load(decoded_file.read().decode('utf-8'), format='csv')
                
            if dry_run == "False":
                resource=LeadResource(user)
                result = resource.import_data(imported_data,dry_run=False,raise_errors=False,validate=True,skip_unchanged=True,collect_failed_rows=True,report_skipped=False,raise_validation_errors=False)
                results = result.totals
                success_rows = []
                error_rows=[]
                if result.has_errors() or result.has_validation_errors():
                    for reo in result.failed_dataset.dict:
                        error = reo['Error']
                        error_message = ''.join(error).replace("'", "").replace("[", "").replace("]", "")
                        del reo['Error']
                        error_rows.append({'row':reo,'error':error_message})
                    return Response({'success':False,'failed_rows':error_rows,'result':results},status=status.HTTP_400_BAD_REQUEST)
                
                imported_rows = resource.imported_rows
                for row in imported_rows:
                    #append the row and message to success_rows
                    success_rows.append({'row':row,'message':'Successfully Imported'})
                return Response({'success':True,'result':results,'success_row':success_rows},status=status.HTTP_200_OK)
            elif dry_run == "True":
                resource=LeadResource(user)
                result = resource.import_data(imported_data,dry_run=True,raise_errors=False,validate=True,skip_unchanged=True,collect_failed_rows=True,report_skipped=False,raise_validation_errors=False)
                results = result.totals
                success_rows = []
                error_rows=[]
                if result.has_errors() or result.has_validation_errors():
                    for reo in result.failed_dataset.dict:
                        error = reo['Error']
                        error_message = ''.join(error).replace("'", "").replace("[", "").replace("]", "")
                        if ',' in error_message:
                            error_message = error_message.split(',')

                        del reo['Error']
                        error_rows.append({'row':reo,'error':error_message})
                    return Response({'success':False,'failed_rows':error_rows,'result':results},status=status.HTTP_400_BAD_REQUEST)
                
                imported_rows = resource.imported_rows
                for row in imported_rows:
                    #append the row and message to success_rows
                    success_rows.append({'row':row,'message':'Success'})
                return Response({'success':True,'result':results,'success_row':success_rows},status=status.HTTP_200_OK)
        else:
            return Response({'success':False,'message':'File type not supported'},status=status.HTTP_400_BAD_REQUEST)
class faq_view(viewsets.ViewSet):
    # authentication_classes = (JWTAuthentication, SessionAuthentication)
    # permission_classes = (IsAuthenticated, )

    def get_faq(self, request, **kwargs):
        """
        Get FAQ
        """
        faq = Faq.objects.all()
        # faq_data = FaqSerializer(faq, many=True)
        return Response({'success':True,'data':faq},status=status.HTTP_200_OK)
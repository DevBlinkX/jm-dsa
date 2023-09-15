from urllib.parse import quote
from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from .forms import *
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django import forms
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from account.utils import send_mail
from django.template.loader import get_template
from django.core.exceptions import ValidationError
from django.contrib import messages
from account.models import *
from django.contrib.auth import get_user_model
from django.conf import settings
UserModel = get_user_model()
from campaign.models import Campaign, CampaignInfluencer, PaymentMethod, Payout
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.utils import timezone
from django.http import Http404, JsonResponse, HttpResponse
from account.models import *
from campaign.models import *
from campaign.utils import overall_stats
from .utils import (
    platform_report,
    campaign_wise_report,
    single_campaign_details,
    platform_wise_report,
    youtube_detail_report,
    influencer_report,
    upload_file,
    get_influ_profile_campaign_stats,
    get_month_wise_report_headers
)
from django.db.models import Sum, Q, Count
import pandas as pd
from django.views.decorators.http import require_http_methods
import json


def index(request, **kwargs):
    """
    index page
    """
    return render(request, 'web/index.html.j2', {"title": "Welcome to Amplifiers"})



from rest_framework.pagination import PageNumberPagination
from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template
from django.conf import settings


#Django rest Pagination
class KnowlageCenterListNumberPagination(PageNumberPagination):
    page_size = 15

class KnowlageAssetsListNumberPagination(PageNumberPagination):
    page_size = 15

class CategoryListNumberPagination(PageNumberPagination):
    page_size = 15

class DRA_ActivatedUserListPagination(PageNumberPagination):
    page_size = 10

class DRA_BrokerListPagination(PageNumberPagination):
    page_size = 10

class DRA_KYCListPagination(PageNumberPagination):
    page_size = 10

class DRA_PayOutPagination(PageNumberPagination):
    page_size = 10    

class DRA_LeadsPagination(PageNumberPagination):
    page_size = 10   

class RM_InfoPagination(PageNumberPagination):
    page_size = 10   


def send_email(*args, **kwargs):
    """function to handle the email sending"""
    try:
        subject = kwargs.get('subject')
        email = kwargs.get('email')
        template_name = kwargs.get('template_name')
        plaintext = get_template('email/email.txt')
        htmly = get_template(template_name)
        user_context = kwargs
        text_content = plaintext.render(user_context)
        html_content = htmly.render(user_context)
        email = EmailMultiAlternatives(subject, text_content,from_email=settings.USE_EMAIL, to=[email])
        email.attach_alternative(html_content, "text/html")
        email.send()
        return True
    except Exception as e:
        print(e)
        return False

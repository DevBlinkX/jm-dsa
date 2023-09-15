from jinja2 import Environment
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import template_localtime as django_localtime
import datetime


def natural_datetime(value):
    """return the human readable time format"""
    if value is None:
        return 'NA'
    try:
        return datetime.datetime.strftime(timezone.localtime(value), "%d %b %Y, %I:%M %p")
    except:
        return 'NA'


def natural_date(value):
    """return the human readable time format"""
    return datetime.datetime.strftime(value, "%d %b %Y")
    if value is None:
        return 'NA'
    try:
        return datetime.datetime.strftime(value, "%d %b %Y")
    except:
        return 'NA'

def indian_date_format(value):
    """return the human readable time format dd/mm/yyyy"""
    # return datetime.datetime.strftime(value, "%d/%m/%Y")
    if value is None:
        return 'NA'
    try:
        return datetime.datetime.strftime(value, "%d/%m/%Y")
    except:
        return 'NA'


def localtime(value):
    return django_localtime(value)


def ampmtime(value):
    return value.strftime("%I:%M %p")


def ampmdate(value):
    return value.strftime("%d %b. %I:%M %p")



def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    env.filters['naturaldatetime'] = natural_datetime
    env.filters['naturaldate'] = natural_date
    env.filters['localtime']=localtime
    env.filters['ampmtime']=ampmtime
    env.filters['ampmdate']=ampmdate

    return env

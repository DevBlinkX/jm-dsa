from django.db.models.signals import pre_save, post_save
from core.models import *
from account.models import *
from django.db import connection
import copy
from account.utils import send_mail
from django.template.loader import get_template
from django.conf import settings

def user_tracker(sender, instance, **kwargs):
    tracker = copy.deepcopy(instance.tracker)
    user_profile(tracker, instance)


def user_profile(tracker, instance, **kwargs):
    try:
        print('Thread start')
        uu = User.objects.get(id=instance.id)
        status_has_changed = False
        if tracker.has_changed('admin_status') and instance.admin_status =='approved':
            # 
            msg_body = get_template('email/profile-activated.html').render(
                    {"user": instance, "login_url": settings.BASE_URL})
            dict_to_send = {
                "emails": instance.email,
                "subject": "JM FINANCIAL- Welcome !",
                "msg_body": msg_body
            }

            send_mail(**dict_to_send)
            uu.is_activated = True
            status_has_changed = True
        else:
            print("else")
            pass

        if tracker.has_changed("incentive_perlead"):
            uu.previous_incentive_perlead = tracker.previous('incentive_perlead')
            status_has_changed = True
        if tracker.has_changed("brokerage_percentage"):
            uu.previous_brokerage_percentage = tracker.previous('brokerage_percentage')
            status_has_changed = True

        if status_has_changed:
            uu.save()

    except Exception as e:
        print(e)
        pass

post_save.connect(user_tracker, sender=User)


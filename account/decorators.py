from threading import Thread
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


# Logger for Thread
class LogThread(Thread):
    """LogThread should always e used in preference to threading.Thread.

    The interface provided by LogThread is identical to that of threading.Thread,
    however, if an exception occurs in the thread the error will be logged
    (using logging.exception) rather than printed to stderr.

    This is important in daemon style applications where stderr is redirected
    to /dev/null.

    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._real_run = self.run
        self.run = self._wrap_run

    def _wrap_run(self):
        try:
            self._real_run()
        except Exception as e:
            print(e)


# Decorator for Multithreading support
def postpone(function):
    def decorator(*args, **kwargs):
        t = LogThread(target=function, args=args, kwargs=kwargs)
        t.setName('Send mail')
        t.daemon = True
        t.start()

    return decorator


def has_dra_dashboard_access(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.user_type == 'dra':
            if user.is_aggre_term_condition and user.is_activated:
                return function(request, *args, **kwargs)
            else:
                return redirect("terms-and-conditions")
        else:
            raise PermissionDenied("permission denied")
    return wrap


def has_rm_dashboard_access(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.user_type == 'rm':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied("permission denied")
    return wrap

def has_dsa_dashboard_access(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.user_type == 'dsa':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied("permission denied")
    return wrap

def has_rmj_dashboard_access(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.user_type == 'rmj':
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied("permission denied")
    return wrap

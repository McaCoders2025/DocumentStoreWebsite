





from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test


def user_has_permission(permission):
    def check_permission(user):
        return user.has_perm(permission)
    return user_passes_test(check_permission)

def is_in_group(group_name):
    def check_group(user):
        return user.groups.filter(name=group_name).exists()
    return user_passes_test(check_group)

def admin_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.groups.filter(name='Admin').exists():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap

def acadmission_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.groups.filter(name='Acadmission').exists():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap


def students_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.groups.filter(name='Students').exists():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap




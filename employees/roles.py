"""Role-based access control: Admin > HR Manager > Employee."""
from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

HR_GROUP = "HR Manager"


def get_role(user):
    if not user.is_authenticated:
        return "anonymous"
    if user.is_superuser:
        return "admin"
    if user.groups.filter(name=HR_GROUP).exists():
        return "hr"
    return "employee"


def can_manage(user):
    return get_role(user) in ("admin", "hr")


def manager_required(view):
    @wraps(view)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not can_manage(request.user):
            raise PermissionDenied
        return view(request, *args, **kwargs)
    return wrapper

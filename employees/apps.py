from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_roles(sender, **kwargs):
    from django.contrib.auth.models import Group
    from .roles import HR_GROUP
    Group.objects.get_or_create(name=HR_GROUP)


class EmployeesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "employees"

    def ready(self):
        post_migrate.connect(create_roles, sender=self)

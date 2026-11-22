from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from employees.models import Department, Employee
from employees.roles import HR_GROUP

User = get_user_model()


class Command(BaseCommand):
    help = "Create demo users and sample employees for local development."

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@techsolutions.test", "Admin12345!")
        hr, _ = User.objects.get_or_create(username="hr_manager", defaults={"email": "hr@techsolutions.test"})
        hr.set_password("HrManager123!"); hr.save()
        hr.groups.add(Group.objects.get_or_create(name=HR_GROUP)[0])
        staff, _ = User.objects.get_or_create(username="ada", defaults={"email": "ada@techsolutions.test"})
        staff.set_password("Employee123!"); staff.save()

        depts = {n: Department.objects.get_or_create(name=n)[0] for n in ("Engineering", "Finance", "Human Resources", "Operations")}
        rows = [
            ("Ada", "Okafor", "ada@techsolutions.test", "Engineering", "Backend Developer", staff),
            ("Tunde", "Bello", "tunde@techsolutions.test", "Engineering", "Frontend Developer", None),
            ("Ngozi", "Eze", "ngozi@techsolutions.test", "Finance", "Accountant", None),
            ("Ibrahim", "Musa", "ibrahim@techsolutions.test", "Operations", "Operations Lead", None),
            ("Chidi", "Nwosu", "chidi@techsolutions.test", "Human Resources", "HR Officer", None),
        ]
        for first, last, email, dept, title, user in rows:
            Employee.objects.get_or_create(email=email, defaults=dict(
                first_name=first, last_name=last, department=depts[dept], job_title=title,
                hire_date=date(2025, 1, 15), salary=450000, user=user))
        self.stdout.write(self.style.SUCCESS(
            "Demo data ready. Logins: admin/Admin12345!  hr_manager/HrManager123!  ada/Employee123!"))

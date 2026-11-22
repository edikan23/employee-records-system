from datetime import date

from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from .models import Employee
from .roles import HR_GROUP


def make_employee(email="a@x.com", first="Ada", user=None):
    return Employee.objects.create(first_name=first, last_name="Okafor", email=email,
                                   job_title="Dev", hire_date=date(2025, 1, 1), user=user)


class AccessControlTests(TestCase):
    def setUp(self):
        self.ada = User.objects.create_user("ada", password="pw-12345-x")
        self.hr = User.objects.create_user("hr", password="pw-12345-x")
        self.hr.groups.add(Group.objects.get(name=HR_GROUP))
        self.mine = make_employee(user=self.ada)
        self.other = make_employee("b@x.com", "Tunde")

    def test_home_is_public(self):
        r = self.client.get(reverse("home"))
        self.assertContains(r, "Employee Records Management System")
        self.assertContains(r, "Welcome to TechSolutions Inc.")

    def test_anonymous_redirected_to_login(self):
        self.assertEqual(self.client.get(reverse("employee_list")).status_code, 302)

    def test_employee_role_limits(self):
        self.client.force_login(self.ada)
        self.assertEqual(self.client.get(reverse("employee_list")).status_code, 403)
        self.assertEqual(self.client.get(reverse("employee_create")).status_code, 403)
        self.assertEqual(self.client.get(self.mine.get_absolute_url()).status_code, 200)
        self.assertEqual(self.client.get(self.other.get_absolute_url()).status_code, 403)
        self.assertEqual(self.client.post(reverse("employee_delete", args=[self.other.pk])).status_code, 403)

    def test_hr_can_crud_search_and_link(self):
        self.client.force_login(self.hr)
        data = dict(first_name="Ngozi", last_name="Eze", email="n@x.com", job_title="Accountant",
                    hire_date="2025-02-02", status="active")
        self.assertEqual(self.client.post(reverse("employee_create"), data).status_code, 302)
        e = Employee.objects.get(email="n@x.com")
        self.assertTrue(e.employee_id.startswith("EMP-"))
        free = User.objects.create_user("ngozi", password="pw-12345-x")
        self.client.post(reverse("employee_update", args=[e.pk]), {**data, "user": free.pk})
        e.refresh_from_db()
        self.assertEqual(e.user, free)
        self.assertContains(self.client.get(reverse("employee_list"), {"q": "Ngozi"}), "Ngozi")
        self.assertNotContains(self.client.get(reverse("employee_list"), {"q": "Ngozi"}), "Tunde")
        self.client.post(reverse("employee_delete", args=[e.pk]))
        self.assertFalse(Employee.objects.filter(pk=e.pk).exists())

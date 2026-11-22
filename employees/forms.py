from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q

from .models import Employee

User = get_user_model()


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ["first_name", "last_name", "email", "phone", "department", "job_title",
                  "hire_date", "salary", "status", "user"]
        widgets = {"hire_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d")}
        labels = {"user": "Linked login account"}
        help_texts = {"user": "Optional. Lets this person sign in and view their own record."}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        free = Q(employee__isnull=True)
        if self.instance.pk and self.instance.user_id:
            free |= Q(pk=self.instance.user_id)
        self.fields["user"].queryset = User.objects.filter(free).order_by("username")
        self.fields["user"].required = False

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EmployeeForm, SignUpForm
from .models import Department, Employee
from .roles import can_manage, manager_required


def home(request):
    ctx = {}
    user = request.user
    if user.is_authenticated:
        if can_manage(user):
            ctx["total"] = Employee.objects.count()
            ctx["active"] = Employee.objects.filter(status="active").count()
            ctx["on_leave"] = Employee.objects.filter(status="leave").count()
            ctx["by_department"] = Department.objects.annotate(n=Count("employees")).filter(n__gt=0).order_by("-n")
            ctx["recent"] = Employee.objects.order_by("-created_at")[:5]
        else:
            ctx["my_record"] = Employee.objects.filter(user=user).first()
    return render(request, "employees/home.html", ctx)


def signup(request):
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.save())
        messages.success(request, "Account created. An HR manager can link it to your employee record.")
        return redirect("home")
    return render(request, "registration/signup.html", {"form": form})


@manager_required
def employee_list(request):
    qs = Employee.objects.select_related("department")
    q = request.GET.get("q", "").strip()
    dept = request.GET.get("department", "")
    status = request.GET.get("status", "")
    if q:
        qs = qs.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(email__icontains=q)
                       | Q(employee_id__icontains=q) | Q(job_title__icontains=q))
    if dept.isdigit():
        qs = qs.filter(department_id=dept)
    if status in Employee.Status.values:
        qs = qs.filter(status=status)
    page = Paginator(qs, 10).get_page(request.GET.get("page"))
    params = request.GET.copy()
    params.pop("page", None)
    return render(request, "employees/employee_list.html", {
        "page": page, "q": q, "dept": dept, "status": status, "querystring": params.urlencode(),
        "departments": Department.objects.all(), "statuses": Employee.Status.choices,
    })


@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee.objects.select_related("department", "user"), pk=pk)
    if not (can_manage(request.user) or employee.user_id == request.user.id):
        raise PermissionDenied
    return render(request, "employees/employee_detail.html", {"employee": employee})


@manager_required
def employee_create(request):
    form = EmployeeForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        employee = form.save()
        messages.success(request, f"{employee.full_name} was registered as {employee.employee_id}.")
        return redirect(employee)
    return render(request, "employees/employee_form.html", {"form": form, "title": "Register employee"})


@manager_required
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    form = EmployeeForm(request.POST or None, instance=employee)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"{employee.full_name} was updated.")
        return redirect(employee)
    return render(request, "employees/employee_form.html",
                  {"form": form, "title": f"Edit {employee.full_name}", "employee": employee})


@manager_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == "POST":
        name = employee.full_name
        employee.delete()
        messages.success(request, f"{name} was deleted.")
        return redirect("employee_list")
    return render(request, "employees/employee_confirm_delete.html", {"employee": employee})


SAMPLE_EMPLOYEES = [
    {"name": "Ada Okafor", "email": "ada@techsolutions.test", "department": "Engineering", "title": "Backend Developer"},
    {"name": "Tunde Bello", "email": "tunde@techsolutions.test", "department": "Engineering", "title": "Frontend Developer"},
    {"name": "Ngozi Eze", "email": "ngozi@techsolutions.test", "department": "Finance", "title": "Accountant"},
]
DEPARTMENTS = ["Engineering", "Finance", "Human Resources", "Operations"]


def dashboard(request):
    """Client-side practice dashboard: JavaScript handles the form and the list."""
    return render(request, "employees/dashboard.html",
                  {"employees": SAMPLE_EMPLOYEES, "departments": DEPARTMENTS})
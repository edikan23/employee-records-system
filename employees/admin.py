from django.contrib import admin

from .models import Department, Employee


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["employee_id", "full_name", "email", "department", "job_title", "status", "user"]
    list_filter = ["status", "department"]
    search_fields = ["first_name", "last_name", "email", "employee_id", "job_title"]
    autocomplete_fields = ["department", "user"]

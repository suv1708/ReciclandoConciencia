from django.contrib import admin
from .models import CustomUser as User
from django.contrib.auth.admin import UserAdmin

# Register your models here.


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Campos adicionales", {
         "fields": ("document_number", "phone", "birth_date", "role")}),
    )

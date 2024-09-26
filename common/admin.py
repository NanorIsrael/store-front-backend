from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AdminUser
from .models import User
# Register your models here.

@admin.register(User)
class UserAdmin(AdminUser):
	add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", 'email', 'first_name', 'last_name'),
            },
        ),
    )
	list_editable = ['first_name']
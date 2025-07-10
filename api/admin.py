from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User, Profile

class UserAdmin(BaseUserAdmin):
    filter_vertical = ("groups", "user_permissions")
    ordering = ["email"]
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_editable = ["is_active", "is_manager"]  # Added is_manager
    list_display = ["email", "first_name", "last_name", "is_staff", "is_manager", "is_active"]  # Added is_manager
    list_display_links = ["email"]
    list_filter = ["email", "is_staff", "is_manager", "is_active"]  # Added is_manager
    search_fields = ["email", "first_name", "last_name"]
    fieldsets = (
        (
            _("Login Credentials"), {
                "fields": ("email", "password",)
            }, 
        ),
        (
            _("Personal Information"),
            {
                "fields": ('first_name', 'last_name',)
            },
        ),
        (
            _("Permissions and Groups"),
            {
                "fields": ("is_active", "is_staff", "is_manager", "is_superuser", "groups", "user_permissions"),  # Added is_manager
                "classes": ("wide", "extrapretty",)  
            },
        ),
        (
            _("Important Dates"),
            {
                "fields": ("last_login", "date_joined")
            },
        ),
    )
    
    readonly_fields = ("last_login", "date_joined")
    
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", 
                "first_name", 
                "last_name", 
                "password1", 
                "password2", 
                "is_staff", 
                "is_manager",  # Added is_manager
                "is_active"
            ),
        }),
    )
    
    
class ProfileAdmin(admin.ModelAdmin):
    list_editable = ["verified"]
    list_display = ["user", "full_name", "verified"]


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
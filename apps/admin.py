from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    admin.site.unregister(Group)
    model = User
    list_display = ("email", "fullname", "phone_number", "is_active", "subscription_end")
    ordering = ("email",)
    search_fields = ("email", "fullname", "phone_number")
    fieldsets = (
        (None, {"fields": ("email", "fullname", "password")}),
        ("Personal info", {"fields": ("phone_number", "subscription_end")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "fullname", "phone_number",
                "password1", "password2",
                "is_active", "is_staff", "is_superuser"
            ),
        }),
    )

    # --- ACTIONS ---
    actions = ["extend_1m", "extend_3m", "extend_6m", "extend_1y"]

    def extend_1m(self, request, queryset):
        for user in queryset:
            user.activate_subscription(period="1m")

        self.message_user(request, f"{queryset.count()} user(s) extended by 1 month")
    extend_1m.short_description = "Extend subscription by 1 month"

    def extend_3m(self, request, queryset):
        for user in queryset:
            user.activate_subscription(period="3m")
        self.message_user(request, f"{queryset.count()} user(s) extended by 3 months")
    extend_3m.short_description = "Extend subscription by 3 months"

    def extend_6m(self, request, queryset):
        for user in queryset:
            user.activate_subscription(period="6m")
        self.message_user(request, f"{queryset.count()} user(s) extended by 6 months")
    extend_6m.short_description = "Extend subscription by 6 months"

    def extend_1y(self, request, queryset):
        for user in queryset:
            user.activate_subscription(period="1y")
        self.message_user(request, f"{queryset.count()} user(s) extended by 1 year")
    extend_1y.short_description = "Extend subscription by 1 year"

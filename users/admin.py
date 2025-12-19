# admin.py
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from unfold.admin import ModelAdmin

from users.models import User

admin.site.unregister(Group)

def superuser_only_perms(admin_cls):
    """Декоратор: скрывает модель в админке и запрещает доступ не-суперам."""
    class Wrapped(admin_cls):
        def get_model_perms(self, request):
            if request.user.is_superuser:
                return super().get_model_perms(request)
            return {}

        def has_module_permission(self, request):
            return request.user.is_superuser

        def has_view_permission(self, request, obj=None):
            return request.user.is_superuser

        def has_add_permission(self, request):
            return request.user.is_superuser

        def has_change_permission(self, request, obj=None):
            return request.user.is_superuser

        def has_delete_permission(self, request, obj=None):
            return request.user.is_superuser

    return Wrapped


@admin.register(User)
class UserAdmin(DjangoUserAdmin, ModelAdmin):
    actions_on_top = True
    actions_on_bottom = False

    # убираем группы/права и даты
    exclude = ("groups", "user_permissions", "date_joined", "last_login")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Персональные данные", {"fields": ("first_name", "last_name", "email")}),        
        ("Статус", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )

    # форма создания пользователя
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username",
                "password1", "password2",
                "first_name", "last_name", "email",
                "is_staff", "is_superuser", "is_active",
            ),
        }),
    )

    list_display = ("username", "email","is_active")
    search_fields = ("username", "email", "first_name", "last_name")
    list_filter = ()
    # удобно, если компаний много (включи search_fields в CompanyAdmin)

    filter_horizontal = ()

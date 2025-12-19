# yourapp/admin.py
from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

from projects.forms import CompanyProjectAdminForm
from .models import CompanyProject, ProjectImage


class ProjectImageInline(TabularInline):
    model = ProjectImage
    extra = 1
    fields = ("image", "caption", "sort_order")
    ordering = ("sort_order", "id")


@admin.register(CompanyProject)
class CompanyProjectAdmin(ModelAdmin):
    form = CompanyProjectAdminForm
    inlines = [ProjectImageInline]

    list_display = ("title", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("title", "summary", "description")
    ordering = ("sort_order", "-updated_at")
    list_editable = ("is_active",)  # удобно быстро включать/выключать

    fieldsets = (
        ("Основное", {
            "fields": (
                "title",
                "is_active",
                "sort_order",
                "hero_image",
            )
        }),
        ("Основное", {"fields": ("customer", "location", "project_type", "power_mw")}),
        ("Описание", {"fields": ("summary",)}),
        ("Блоки страницы", {"fields": ("task", "goal", "features")}),
        ("Наша роль в проекте", {"fields": ("role_in_project",)}),
        ("Карта", {"fields": ("map_point",)}),
    )
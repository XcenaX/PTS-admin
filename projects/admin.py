# yourapp/admin.py
import json
from django.contrib import admin
import requests
from unfold.admin import ModelAdmin, TabularInline
from modeltranslation.admin import TabbedTranslationAdmin
from projects.forms import CompanyProjectAdminForm
from pts_admin.settings import DEEPL_KEY
from .models import CompanyProject, ProjectImage

from django.http import JsonResponse, HttpResponseBadRequest
from django.urls import path
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator

def deepl_translate(text: str, source: str, target: str, *, is_html: bool) -> str:
    # DeepL language codes: RU, EN, KK (Kazakh) :contentReference[oaicite:2]{index=2}
    lang_map = {"ru": "RU", "kk": "KK", "en": "EN"}

    payload = {
        "text": [text],  # для JSON-формата DeepL ждёт массив строк :contentReference[oaicite:3]{index=3}
        "source_lang": lang_map[source],
        "target_lang": lang_map[target],
    }
    if source == "kk" or target == "kk":
        payload["enable_beta_languages"] = True
        
    if is_html:
        payload["tag_handling"] = "html"
        payload["tag_handling_version"] = "v2"  # улучшенный алгоритм (Oct 2025) :contentReference[oaicite:4]{index=4}

    headers = {
        "Authorization": f"DeepL-Auth-Key {DEEPL_KEY}",  # вместо auth_key в body :contentReference[oaicite:5]{index=5}
        "Content-Type": "application/json",
    }

    r = requests.post("https://api-free.deepl.com/v2/translate", headers=headers, json=payload, timeout=20)
    r.raise_for_status()
    return r.json()["translations"][0]["text"]


class ProjectImageInline(TabularInline):
    model = ProjectImage
    extra = 1
    fields = ("image", "caption", "sort_order")
    ordering = ("sort_order", "id")


@admin.register(CompanyProject)
class CompanyProjectAdmin(ModelAdmin, TabbedTranslationAdmin):
    form = CompanyProjectAdminForm
    inlines = [ProjectImageInline]

    list_display = ("title", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("title", "summary", "description")
    ordering = ("sort_order", "-updated_at")
    list_editable = ("is_active",)  # удобно быстро включать/выключать
    group_fieldsets = True

    fieldsets = (
        ("Основное", {
            "fields": (
                "title",
                "is_active",
                "sort_order",
                "hero_image",
                "hero_video",
            )
        }),
        ("Основное", {"fields": ("customer", "location", "project_type", "power_mw")}),
        ("Описание", {"fields": ("summary",)}),
        ("Блоки страницы", {"fields": ("task", "goal", "features")}),
        ("Наша роль в проекте", {"fields": ("role_in_project",)}),
        ("Карта", {"fields": ("map_point",)}),
    )

    class Media:
        js = ("admin/companyproject_translate.js",)

    def get_urls(self):
        urls = super().get_urls()
        return [
            path("translate/", self.admin_site.admin_view(self.translate_view), name="companyproject_translate"),
        ] + urls
    
    
    @method_decorator(require_POST)
    def translate_view(self, request):
        try:
            payload = json.loads(request.body.decode("utf-8"))
        except Exception:
            return HttpResponseBadRequest("Invalid JSON")

        text = (payload.get("text") or "").strip()
        source = payload.get("source")          # "ru" | "kk" | "en"
        targets = payload.get("targets", [])    # ["kk", "en"] и т.п.
        is_html = bool(payload.get("is_html", False))

        if source not in ("ru", "kk", "en") or not isinstance(targets, list):
            return HttpResponseBadRequest("Bad payload")

        result = {}
        for t in targets:
            if t not in ("ru", "kk", "en") or t == source:
                continue
            result[t] = "" if not text else deepl_translate(text, source, t, is_html=is_html)

        return JsonResponse({"translations": result})
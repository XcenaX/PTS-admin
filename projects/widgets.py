# yourapp/widgets.py
import json
from django import forms
from django.templatetags.static import static

class ImagePointWidget(forms.Widget):
    template_name = "widgets/image_point.html"

    def __init__(self, image_url=None, attrs=None):
        super().__init__(attrs)
        self.image_url = image_url or static("img/kz_map.png")

    def get_context(self, name, value, attrs):
        # value может быть dict или JSON-строкой
        if isinstance(value, str) and value:
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                value = {}

        value = value or {}
        x = value.get("x")
        y = value.get("y")

        ctx = super().get_context(name, value, attrs)
        ctx["widget"]["image_url"] = self.image_url
        ctx["widget"]["x"] = x
        ctx["widget"]["y"] = y
        return ctx

    class Media:
        js = ("admin/image_point.js",)
        css = {"all": ("admin/image_point.css",)}

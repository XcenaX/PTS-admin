# yourapp/forms.py
from django import forms
from projects.models import CompanyProject
from projects.widgets import ImagePointWidget
from django_ckeditor_5.widgets import CKEditor5Widget

class CompanyProjectAdminForm(forms.ModelForm):
    map_point = forms.JSONField(
        required=False,
        widget=ImagePointWidget(),  # можно передать image_url=... если нужно
        label="Точка на карте",
    )

    class Meta:
        model = CompanyProject
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Прокидываем текущие значения в виджет
        self.initial["map_point"] = {
            "x": str(self.instance.map_x) if self.instance.map_x is not None else None,
            "y": str(self.instance.map_y) if self.instance.map_y is not None else None,
        }

        rich_fields = ("summary", "task", "goal", "features", "role_in_project")
        langs = ("ru", "kk", "en")

        for base in rich_fields:
            for lang in langs:
                name = f"{base}_{lang}"
                if name in self.fields:
                    self.fields[name].widget = CKEditor5Widget(
                        attrs={"class": "django_ckeditor_5"},
                        config_name="default",
                    )

    def clean_map_point(self):
        data = self.cleaned_data.get("map_point") or {}
        x = data.get("x")
        y = data.get("y")
        if x is None or y is None:
            return {"x": None, "y": None}

        x = float(x); y = float(y)
        if not (0 <= x <= 1 and 0 <= y <= 1):
            raise forms.ValidationError("Координаты должны быть в диапазоне 0..1")
        return {"x": x, "y": y}

    def save(self, commit=True):
        obj = super().save(commit=False)
        p = self.cleaned_data.get("map_point") or {}
        obj.map_x = p.get("x")
        obj.map_y = p.get("y")
        if commit:
            obj.save()
            self.save_m2m()
        return obj

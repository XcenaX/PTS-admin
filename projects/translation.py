from modeltranslation.translator import register, TranslationOptions
from .models import CompanyProject

@register(CompanyProject)
class CompanyProjectTR(TranslationOptions):
    fields = (
        "title",
        "summary",
        "customer",
        "location",
        "project_type",
        "task",
        "goal",
        "features",
        "role_in_project",
    )

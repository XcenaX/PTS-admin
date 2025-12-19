from django.db import models
from django.utils.text import slugify
import uuid
from django_ckeditor_5.fields import CKEditor5Field


class CompanyProject(models.Model):
    """
    Проект внутри компании (на первом сайте в админке создаём/настраиваем проекты).    
    """
    id = models.UUIDField(
        verbose_name="ID",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    title = models.CharField("Название проекта", max_length=200)
    summary = CKEditor5Field("Короткое описание", config_name="default", blank=True)

    customer = models.CharField("Заказчик", max_length=200, blank=True)  # Energy China
    location = models.CharField("Расположение", max_length=300, blank=True)  # Туркестанская область...
    project_type = models.CharField("Тип проекта", max_length=250, blank=True)  # Солнечная электростанция, EPC
    power_mw = models.IntegerField("Мощность, МВт", blank=True, null=True)  # 300.00

    task = CKEditor5Field("Задача",config_name="default", blank=True)
    goal = CKEditor5Field("Цель проекта", config_name="default", blank=True)
    features = CKEditor5Field("Особенности проекта", config_name="default", blank=True)

    hero_image = models.ImageField("Главное изображение", upload_to="projects/hero/%Y/%m/", blank=True, null=True)
    is_active = models.BooleanField("Показывать на сайте", default=True)
    sort_order = models.PositiveIntegerField("Порядок", default=0)

    role_in_project = CKEditor5Field("Наша роль в проекте", config_name="default", blank=True)

    map_x = models.DecimalField("Точка на карте X (0..1)", max_digits=9, decimal_places=6, blank=True, null=True)
    map_y = models.DecimalField("Точка на карте Y (0..1)", max_digits=9, decimal_places=6, blank=True, null=True)

    created_at = models.DateTimeField("Создан", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлён", auto_now=True)

    class Meta:
        verbose_name = "Проект компании"
        verbose_name_plural = "Проекты компании"        
        indexes = [
            models.Index(fields=["is_active"]),
        ]

    def __str__(self) -> str:
        return f"{self.title}"
    

class ProjectImage(models.Model):
    project = models.ForeignKey(CompanyProject, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField("Картинка", upload_to="projects/images/%Y/%m/")
    caption = models.CharField("Подпись", max_length=255, blank=True)
    sort_order = models.PositiveIntegerField("Порядок", default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Картинка проекта"
        verbose_name_plural = "Картинки проекта"    
        ordering = ("sort_order", "id")

    def __str__(self):
        return f"Картинка #{self.id} для проекта {self.project}"
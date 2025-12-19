import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
   
    class Meta:
        verbose_name = "Сайт"
        verbose_name_plural = "Сайты"  

    def __str__(self) -> str:
        return f"{self.name}"

class CompanyModel(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, db_index=True)

    class Meta:
        abstract = True

class User(AbstractUser):
    """
    Кастомный пользователь с UUID и телефоном.
    """
    id = models.UUIDField(
        verbose_name="ID",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    company = models.ForeignKey(Company, on_delete=models.PROTECT, verbose_name="Сайт", related_name="users", null=True, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username or self.phone
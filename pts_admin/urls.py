from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="PTS API",
      default_version='v1',
      description="Апи для PTS",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('docs/',  schema_view.with_ui( cache_timeout=0)),

    path("api/", include("projects.urls")),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("i18n/", include("django.conf.urls.i18n")),

    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
] + i18n_patterns(
    path("", admin.site.urls),
)

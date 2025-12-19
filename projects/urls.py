
# projects/urls.py
from django.urls import path
from .views import (
    CompanyProjectListView,
    CompanyProjectDetailView,
    CompanyProjectPointsView,
)

urlpatterns = [
    path("projects/", CompanyProjectListView.as_view(), name="projects-list"),
    path("projects/<uuid:id>/", CompanyProjectDetailView.as_view(), name="projects-detail"),
    path("projects/points/", CompanyProjectPointsView.as_view(), name="projects-points"),
]

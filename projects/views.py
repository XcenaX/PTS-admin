# projects/views.py
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import CompanyProject
from .serializers import (
    CompanyProjectListSerializer,
    CompanyProjectDetailSerializer,
    CompanyProjectRelatedSerializer,
)


class CompanyProjectListView(generics.ListAPIView):
    """
    1) Список проектов: hero картинка, имя, summary
    """
    permission_classes = [AllowAny]
    serializer_class = CompanyProjectListSerializer

    def get_queryset(self):
        return CompanyProject.objects.filter(is_active=True).order_by("sort_order", "-updated_at")


class CompanyProjectDetailView(generics.RetrieveAPIView):
    """
    2) Вся инфа проекта по id + 3 случайных проекта
    """
    permission_classes = [AllowAny]
    serializer_class = CompanyProjectDetailSerializer
    lookup_field = "id"

    def get_queryset(self):
        return CompanyProject.objects.filter(is_active=True).prefetch_related("images")

    def retrieve(self, request, *args, **kwargs):
        project = self.get_object()

        # 3 случайных проекта той же компании
        related_qs = CompanyProject.objects.filter(is_active=True).exclude(id=project.id).order_by("?")[:3]

        project_data = CompanyProjectDetailSerializer(project, context={"request": request}).data
        related_data = CompanyProjectRelatedSerializer(related_qs, many=True, context={"request": request}).data

        return Response({
            "project": project_data,
            "related": related_data,
        })


class CompanyProjectPointsView(APIView):
    """
    3) Все точки: один проект = одна точка (x,y в 0..1)
    """
    permission_classes = [AllowAny]

    def get(self, request):
        qs = CompanyProject.objects.filter(
            is_active=True,
            map_x__isnull=False,
            map_y__isnull=False,
        )

        points = [
            {
                "id": p.id,
                "title": p.title,
                "customer": p.customer,
                "location": p.location,
                "project_type": p.project_type,
                "power_mw": p.power_mw,
                "x": float(p.map_x),
                "y": float(p.map_y),
            }
            for p in qs.only("id", "title", "customer", "location", "project_type", "power_mw", "map_x", "map_y")
        ]
        return Response({"points": points})

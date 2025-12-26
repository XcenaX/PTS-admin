# projects/views.py
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.template.loader import render_to_string
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from pts_admin.settings import EMAIL_HOST_USER
from .models import CompanyProject
from rest_framework.throttling import AnonRateThrottle
from django.core.mail import EmailMultiAlternatives
from .serializers import (
    CompanyProjectListSerializer,
    CompanyProjectDetailSerializer,
    CompanyProjectPointSerializer,
    CompanyProjectRelatedSerializer,
    ContactRequestSerializer,
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

        serializer = CompanyProjectPointSerializer(qs, many=True, context={"request": request})
        return Response({"points": serializer.data})


class ContactRateThrottle(AnonRateThrottle):
    # 10 запросов в час на IP
    rate = "10/hour"


class ContactRequestView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ContactRateThrottle]

    @swagger_auto_schema(
        operation_summary="Отправить заявку с формы «Связаться с нами»",
        operation_description=(
            "Принимает данные формы и отправляет письмо"            
        ),
        tags=["Contact"],
        request_body=ContactRequestSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Письмо отправлено",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"ok": openapi.Schema(type=openapi.TYPE_BOOLEAN)},
                ),
                examples={"application/json": {"ok": True}},
            ),
            status.HTTP_429_TOO_MANY_REQUESTS: openapi.Response(
                description="Слишком много запросов (rate limit)",
                examples={"application/json": {"detail": "Слишком много запросов!"}},
            ),
        },
    )
    def post(self, request):
        serializer = ContactRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        subject = "Заявка с сайта: Связаться с нами"

        context = {
            "full_name": data["full_name"],
            "email": data["email"],
            "phone": data.get("phone") or "—",
            "company": data.get("company") or "—",
            "comment": data.get("comment") or "—",
            "ip": request.META.get("REMOTE_ADDR"),
            "user_agent": request.META.get("HTTP_USER_AGENT"),
        }

        text_body = (
            "Новая заявка с сайта\n\n"
            f"ФИО: {context['full_name']}\n"
            f"Email: {context['email']}\n"
            f"Телефон: {context['phone']}\n"
            f"Компания: {context['company']}\n\n"
            f"Комментарий:\n{context['comment']}\n\n"
            f"IP: {context['ip']}\n"
            f"User-Agent: {context['user_agent']}\n"
        )

        html_body = render_to_string("emails/contact_request.html", context)

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=EMAIL_HOST_USER,
            to=[EMAIL_HOST_USER],            
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send(fail_silently=False)

        return Response({"ok": True})
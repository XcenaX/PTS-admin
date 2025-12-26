# projects/serializers.py
from rest_framework import serializers

from projects.fields import ModelTranslationDictField
from .models import CompanyProject, ProjectImage


class ProjectImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProjectImage
        fields = ("id", "caption", "sort_order", "image_url")

    def get_image_url(self, obj):
        if not obj.image:
            return None
        request = self.context.get("request")
        url = obj.image.url
        return request.build_absolute_uri(url) if request else url


class CompanyProjectListSerializer(serializers.ModelSerializer):
    hero_image_url = serializers.SerializerMethodField()
    title = ModelTranslationDictField("title", source="*", required=False)
    summary = ModelTranslationDictField("summary", source="*", required=False)

    class Meta:
        model = CompanyProject
        fields = ("id", "title", "summary", "hero_image_url")

    def get_hero_image_url(self, obj):
        if not obj.hero_image:
            return None
        request = self.context.get("request")
        url = obj.hero_image.url
        return request.build_absolute_uri(url) if request else url


class CompanyProjectRelatedSerializer(serializers.ModelSerializer):
    hero_image_url = serializers.SerializerMethodField()
    title = ModelTranslationDictField("title", source="*", required=False)
    summary = ModelTranslationDictField("summary", source="*", required=False)
    
    class Meta:
        model = CompanyProject
        fields = ("id", "title", "summary", "hero_image_url")

    def get_hero_image_url(self, obj):
        if not obj.hero_image:
            return None
        request = self.context.get("request")
        url = obj.hero_image.url
        return request.build_absolute_uri(url) if request else url


class CompanyProjectDetailSerializer(serializers.ModelSerializer):
    hero_image_url = serializers.SerializerMethodField()
    images = ProjectImageSerializer(many=True, read_only=True)

    title = ModelTranslationDictField("title", source="*", required=False)
    summary = ModelTranslationDictField("summary", source="*", required=False)

    customer = ModelTranslationDictField("customer", source="*", required=False)
    location = ModelTranslationDictField("location", source="*", required=False)
    project_type = ModelTranslationDictField("project_type", source="*", required=False)

    task = ModelTranslationDictField("task", source="*", required=False)
    goal = ModelTranslationDictField("goal", source="*", required=False)
    features = ModelTranslationDictField("features", source="*", required=False)

    role_in_project = ModelTranslationDictField("role_in_project", source="*", required=False)
    
    class Meta:
        model = CompanyProject
        fields = (
            "id", "title", "summary", 
            "customer", "location", "project_type", "power_mw", 
            "task", "goal", "features", "role_in_project", 
            "hero_image_url", "images", 
            "map_x", "map_y", 
            "created_at", "updated_at",
        )

    def get_hero_image_url(self, obj):
        if not obj.hero_image:
            return None
        request = self.context.get("request")
        url = obj.hero_image.url
        return request.build_absolute_uri(url) if request else url


class ContactRequestSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=120)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=40, required=False, allow_blank=True)
    company = serializers.CharField(max_length=120, required=False, allow_blank=True)
    comment = serializers.CharField(max_length=5000, required=False, allow_blank=True)


class CompanyProjectPointSerializer(serializers.ModelSerializer):
    title = ModelTranslationDictField("title", source="*", required=False)
    customer = ModelTranslationDictField("customer", source="*", required=False)
    location = ModelTranslationDictField("location", source="*", required=False)
    project_type = ModelTranslationDictField("project_type", source="*", required=False)

    x = serializers.FloatField(source="map_x")
    y = serializers.FloatField(source="map_y")

    class Meta:
        model = CompanyProject
        fields = (
            "id",
            "title",
            "customer",
            "location",
            "project_type",
            "power_mw",
            "x",
            "y",
        )
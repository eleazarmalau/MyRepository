from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Education, Project


class ProjectSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id", "title", "description", "tech_stack",
            "project_url", "project_image_url",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value)

    def validate_tech_stack(self, value):
        return strip_tags(value)

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())


class EducationSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()

    class Meta:
        model = Education
        fields = [
            "id", "title", "institution", "major", "description", "thumbnail",
            "start_year", "end_year", "created_at", "updated_at",
            "star_count", "is_starred",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def _validate_text(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError(
                "Isian tidak boleh kosong atau hanya berisi tag HTML.",
            )
        return value

    def validate_title(self, value):
        return self._validate_text(value)

    def validate_institution(self, value):
        return self._validate_text(value)

    def validate_major(self, value):
        return self._validate_text(value)

    def validate_description(self, value):
        return self._validate_text(value)

    def validate_thumbnail(self, value):
        if value and not value.lower().startswith(("http://", "https://")):
            raise serializers.ValidationError(
                "URL gambar harus menggunakan HTTP atau HTTPS.",
            )
        return value

    def validate(self, attrs):
        # PATCH may supply only one year; compare it with the saved counterpart.
        start_year = attrs.get("start_year", getattr(self.instance, "start_year", None))
        end_year = attrs.get("end_year", getattr(self.instance, "end_year", None))
        if start_year is not None and end_year is not None and end_year < start_year:
            raise serializers.ValidationError({
                "end_year": "Tahun selesai tidak boleh sebelum tahun mulai.",
            })
        return attrs

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

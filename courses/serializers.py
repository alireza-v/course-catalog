from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()


class VideoSer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ("title", "video_file")


class CategorySer(serializers.ModelSerializer):
    """Category model serializer with parent-child relationship"""

    parent = serializers.CharField(source="parent.name", read_only=True)
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("id", "name", "parent", "subcategories")

    def get_subcategories(self, obj):
        subcategories = obj.subcategories.all()
        return CategorySer(subcategories, many=True).data


class CourseSer(serializers.ModelSerializer):
    """Course model serializer"""

    category = serializers.CharField(source="category.name", read_only=True)
    hierarchy = serializers.SerializerMethodField()
    category_name = serializers.CharField(write_only=True)
    # user_email = serializers.EmailField(source="user.email",read_only=True)

    class Meta:
        model = Course
        fields = (
            "id",
            "category",
            "title",
            "description",
            "video",
            # "user_email",
            "category_name",
            "hierarchy",
        )

    def get_hierarchy(self, obj):
        hierarchy = []
        category = obj.category
        while category:
            hierarchy.insert(
                0, category.name
            )  # Insert at the beginning for top-down order
            category = category.parent  # Move up the parent chain
        return " > ".join(hierarchy)

    def validate_video(self, video):
        """Limit video size"""

        # maxSize = 100 * 1024 * 1024
        # if video.size >= maxSize:
        #     raise serializers.ValidationError(
        #         f"video file size can not be greater than {maxSize}"
        #     )
        return video

    def create(self, validated_data):
        category_name = validated_data.pop("category_name", None)
        category = Category.objects.get(name=category_name)
        return Course.objects.create(category=category, **validated_data)


class CommentSer(serializers.ModelSerializer):
    # course = serializers.CharField(source="course.title")
    course = serializers.SlugRelatedField(
        queryset=Course.objects.all(),
        slug_field="title",
    )

    class Meta:
        model = Comment
        fields = ("id", "course", "description", "score")


class FavoriteSer(serializers.ModelSerializer):
    # course = serializers.CharField(write_only=True)
    course = serializers.SlugRelatedField(
        queryset=Course.objects.all(),
        slug_field="title",
    )

    class Meta:
        model = Favorite
        fields = ["id", "course"]
        extra_kwargs = {"user": {"read_only": True}}

    def validate(self, data):
        user = self.context["request"].user
        course = data["course"]
        if Favorite.objects.filter(user=user, course=course).exists():
            raise serializers.ValidationError(
                "This course is already in your favorites"
            )
        return data

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

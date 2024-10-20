from rest_framework import serializers
from .models import *


class VideoSer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ("title", "video_file")


class Category(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("title", "parent")


class Course(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("user", "title", "description", "video", "category")


class Comment(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("course", "description", "score")

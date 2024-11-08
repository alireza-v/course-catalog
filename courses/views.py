from django.contrib.auth import get_user_model
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *

User = get_user_model()


class CategoryList(generics.ListAPIView):
    """Category lists"""

    permission_classes = (permissions.IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategorySer


class CourseListCreate(generics.ListCreateAPIView):
    """List/Create Course view api"""

    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)
    queryset = Course.objects.all().order_by("-timestamp")
    serializer_class = CourseSer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CourseRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """get/update/delete the Fovorite instance model"""

    permission_classes = (permissions.IsAuthenticated,)
    queryset = Course.objects.all()
    serializer_class = CourseSer


class CommentListCreate(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Comment.objects.all()
    serializer_class = CommentSer


class FavoriteListCreate(generics.ListCreateAPIView):
    """list/create Favotite model model instance"""

    permission_classes = (permissions.IsAuthenticated,)
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSer

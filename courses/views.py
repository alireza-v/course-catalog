from django.contrib.auth import get_user_model
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import *

from .models import *
from .serializers import *

User = get_user_model()


class CategoryList(generics.ListAPIView):
    """Category lists"""

    permission_classes = (permissions.AllowAny,)
    queryset = Category.objects.all()
    serializer_class = CategorySer

    @swagger_auto_schema(
        operation_summary="List of available categories",
        operation_description="List of available categories",
        responses={200: CategorySer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CourseListCreate(generics.ListCreateAPIView):
    """List/Create Course view api"""

    # permission_classes = (IsMentorPerm,)
    parser_classes = (MultiPartParser, FormParser)
    queryset = Course.objects.all().order_by("-timestamp")
    serializer_class = CourseSer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsMentorPerm()]
        elif self.request.method == "GET":
            # Both student and mentor can access data through GET method
            return [IsStudentOrMentor()]

    @swagger_auto_schema(
        operation_summary="Retrieve available courses",
        operation_description="Retrieve available courses",
        responses={200: CourseSer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create course instance using the predefined categories",
        operation_description="Create course instance using the predefined categories",
        request_body=CourseSer,
        responses={201: CourseSer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CourseRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """get/update/delete the Fovorite instance model"""

    # permission_classes = (permissions.IsAuthenticated,)
    queryset = Course.objects.all()
    serializer_class = CourseSer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsStudentOrMentor()]
        elif self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsMentorPerm()]

    @swagger_auto_schema(
        operation_summary="Get a course using the pk lookup field",
        operation_description="Get a course using the pk lookup field",
        responses={200: CourseSer},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update the course data with pk",
        operation_description="Update the course data with pk",
        request_body=CourseSer,
        responses={200: CourseSer},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete course instance using the pk",
        operation_description="Delete course instance using the pk",
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(dict(message="Course instance deleted successfully"), 204)


class CommentListCreate(generics.ListCreateAPIView):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = Comment.objects.all()
    serializer_class = CommentSer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsStudentOrMentor()]
        elif self.request.method == "POST":
            return [IsStudentPerm()]

    @swagger_auto_schema(
        operation_summary="Retrieve comments on courses",
        operation_description="Retrieve comments on courses",
        responses={200: CommentSer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Post a comment on a course",
        operation_description="Post a comment on a course",
        request_body=CommentSer,
        responses={201: CommentSer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class FavoriteListCreate(generics.ListCreateAPIView):
    """list/create Favotite model model instance"""

    queryset = Favorite.objects.all()
    serializer_class = FavoriteSer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsStudentOrMentor()]
        if self.request.method == "POST":
            return [IsStudentPerm()]

    @swagger_auto_schema(
        operation_summary="Retrieve lists of favorite courses",
        operation_description="Retrieve lists of favorite courses",
        responses={200: FavoriteSer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Add a course to the user favorite list",
        operation_description="Add a course to the user favorite list",
        request_body=FavoriteSer,
        responses={201: FavoriteSer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

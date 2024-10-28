from django.urls import path
from .views import *

urlpatterns = [
    path("category/", CategoryList.as_view(), name="category-l"),
    path("course/", CourseListCreate.as_view(), name="course-lc"),
    path(
        "course/<int:pk>/", CourseRetrieveUpdateDestroy.as_view(), name="course-lookup"
    ),
    path("comment/", CommentListCreate.as_view(), name="comment"),
    path(
        "list-create-favorite/",
        FavoriteListCreate.as_view(),
        name="list-create-favorite",
    ),
]

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
import pytest
from faker import Faker
from ..models import *

faker = Faker()
User = get_user_model()


@pytest.fixture
def user(db):
    """Create CustomUser instance"""
    user = User.objects.create_user(
        email="test@email.com",
        password="123!@#",
    )
    return user


@pytest.mark.django_db
class TestCourseModel:
    """test suite for course(app) models
    fixture made for creating model instances
    """

    @pytest.fixture
    def video(db):
        """Create temporary video file for testing"""
        video_file = SimpleUploadedFile(
            name="test_video.mp4",
            content=b"video_content",
            content_type="video/mp4",
        )
        return video_file

    @pytest.fixture
    def category(db):
        """Category data implementation"""
        parentCategory = Category.objects.create(name="programming")
        childCategory = Category.objects.create(name="python", parent=parentCategory)

        return parentCategory, childCategory

    @pytest.fixture
    def course(self, db, user, video, category):
        """Course fixture"""
        parent, child = category
        return Course.objects.create(
            user=user,
            title=faker.sentence(nb_words=4),
            description=faker.text(),
            video=video,
            category=parent,
        )

    @pytest.fixture
    def comment(self, db, course, user):
        """Comment fixture"""
        return Comment.objects.create(
            user=user,
            course=course,
            description=faker.text(),
            score=ScoreChoices.GOOD,
        )

    @pytest.fixture
    def favorite(db, user, course):
        """Favorite instance test"""
        return Favorite.objects.create(
            user=user,
            course=course,
        )

    def testVideo(self, video):
        video = Video.objects.create(title=faker.word(), video_file=video)
        assert video.title
        # assert video.video_file== "videos/test_video.mp4"

    def testCategory(self, category):
        parent, child = category
        assert child.name == "python"
        assert child.parent == parent
        assert parent.subcategories.filter(id=child.id).exists()

    def testCourse(self, course, user, video, category):
        assert course.user == user
        assert course.title
        assert course.video
        assert course.category
        assert Course.objects.count() == 1

    def testComment(self, comment, course):
        assert comment.course == course
        assert comment.description
        assert comment.score == ScoreChoices.GOOD

    def testString(self, course, video, comment):
        assert str(course) is not None
        assert str(video) is not None
        assert str(comment) == "Good"

    def testFavorite(self, favorite):
        assert favorite.user
        assert favorite.course

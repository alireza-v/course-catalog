import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from faker import Faker
from rest_framework.test import APIClient

from ..models import *

faker = Faker()
User = get_user_model()


@pytest.fixture
def user_student(db):
    """CustomUser instance with student role"""
    user = User.objects.create_user(
        email="student@email.com", password="123!@#", role="student"
    )
    return user


@pytest.fixture
def user_mentor(db):
    """CustomUser instance with mentor role"""
    user = User.objects.create_user(
        email="mentor@email.com", password="123!@#", role="mentor"
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
    def course(db, user_mentor, video, category):
        """Course fixture"""
        parent, child = category
        return Course.objects.create(
            user=user_mentor,
            title=faker.sentence(nb_words=4),
            description=faker.text(),
            video=video,
            category=parent,
        )

    @pytest.fixture
    def comment(self, db, course, user_student):
        """Comment fixture"""
        return Comment.objects.create(
            user=user_student,
            course=course,
            description=faker.text(),
            score=ScoreChoices.GOOD,
        )

    @pytest.fixture
    def favorite(db, user_student, course):
        """Favorite instance test"""
        return Favorite.objects.create(
            user=user_student,
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

    def testCourse(self, course, user_mentor, video, category):
        assert course.user == user_mentor
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

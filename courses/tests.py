from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
import pytest
from faker import Faker
from .models import Category, Comment, Course, Video

faker = Faker()
User = get_user_model()


@pytest.mark.django_db
class TestCourseModel:
    """
    test suite for course(app) models
    fixture made for creating model instances
    """

    @pytest.fixture
    def user(self):
        raw_password = "123!@#QWE"
        user = User.objects.create_user(
            email=faker.email(),
            password=raw_password,
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            phone=faker.phone_number(),
            role="student",
        )
        user.raw_password = raw_password
        return user

    @pytest.fixture
    def video(self):
        video_file = SimpleUploadedFile(
            "test_video.mp4",
            b"file_content",
            content_type="video/mp4",
        )
        return Video.objects.create(
            title=faker.sentence(nb_words=3),
            video_file=video_file,
        )

    @pytest.fixture
    def category(self):
        return Category.objects.create(title=faker.word())

    @pytest.fixture
    def course(self, user, video, category):
        return Course.objects.create(
            user=user,
            title=faker.sentence(nb_words=4),
            description=faker.text(),
            video=video,
            category=category,
        )

    @pytest.fixture
    def comment(self, course):
        return Comment.objects.create(
            course=course,
            description=faker.text(),
            score=Comment.Score.GOOD,
        )

    def testVideo(self, video):
        assert video.title
        # assert video.video_file== "videos/test_video.mp4"

    def testCategory(self, category):
        assert category.title
        assert category.parent is None

    def testCourse(self, course, user, video, category):
        assert course.user == user
        assert course.title
        assert course.video
        assert course.category == category

    def testComment(self, comment, course):
        assert comment.course == course
        assert comment.description
        assert comment.score == Comment.Score.GOOD

    def testString(self, course, video, comment):
        assert str(course) is not None
        assert str(video) is not None
        assert str(comment) == "Good"

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
import pytest
from faker import Faker

from ..models import *
from ..views import *
from .testModel import *

faker = Faker()
User = get_user_model()


@pytest.mark.django_db
class TestCoursesView:
    @pytest.fixture
    def client(self):
        """Api client fixture for making http requests"""
        return APIClient()

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
            score=course.Score.GOOD,
        )

    @pytest.fixture
    def jwt(self, client, user):
        """Send a post request to get access and refresh token for protected views"""
        url = reverse("apiToken")
        response = client.post(
            url,
            data=dict(
                email=user.email,
                password="123!@#",
            ),
        )
        tokens = response.json()
        return (tokens["access"], tokens["refresh"])

    def testCategory(self, client, jwt):
        """test list group of categories"""
        ...

    def testCourseGET(self, client, jwt):
        """Test GET request courses"""
        access, refresh = jwt
        url = reverse("course-lc")
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        response = client.get(url)
        assert response.status_code == 200

    def testCoursePOST(self, client, jwt, video, category):
        """Test POST request courses"""
        access, refresh = jwt
        parent, child = category
        url = reverse("course-lc")
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        data = dict(
            title=faker.word(),
            description=faker.text(),
            video=video,
            category_name=parent.name,

        )
        response = client.post(url, data, format="multipart")
        assert response.status_code == 201

    def testCourseRetrieve(self, jwt, client, course):
        """Test Course view with pk"""
        access, refresh = jwt
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        url = reverse("course-lookup", kwargs=dict(pk=course.id))
        response = client.get(url)
        assert response.status_code == 200

    def testCourseUpdatePUT(self, jwt, client, course, category):
        """Test update(PUT) Course view with pk"""
        access, refresh = jwt
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        parent, child = category
        updatedData = dict(
            title=faker.word(),
            description=faker.sentence(),
            category_name=parent.name,
            subcategory_name=child.name,
        )
        url = reverse("course-lookup", kwargs=dict(pk=course.id))
        response = client.put(url, updatedData)
        assert response.status_code == 200

    def testCourseDestroy(self, jwt, client, course):
        """Test destroy Course view with pk"""
        access, refresh = jwt
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        url = reverse("course-lookup", kwargs=dict(pk=course.id))
        response = client.delete(url)
        assert response.status_code == 204
        assert not Course.objects.filter(pk=course.id).exists()

    def testCommentGET(self, jwt, client):
        """Test comment get request"""
        access, refresh = jwt
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        url = reverse("comment")
        response = client.get(url)
        assert response.status_code == 200

    def testCommentPOST(self, course, jwt, client):
        """Comment test post request"""
        access, refresh = jwt
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        url = reverse("comment")
        data = dict(
            course=course.title,
            description=faker.sentence(),
            score=1,
        )
        response = client.post(url, data)
        assert response.status_code == 201

    def testListFavorite(self, jwt, client, course):
        """Test list/create favorite courses"""
        access, refresh = jwt
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        url = reverse("list-create-favorite")
        data = dict(
            course=course.title,
        )
        response = client.get(url)
        responsePOST = client.post(url, data)
        assert response.status_code == 200
        assert responsePOST.status_code == 201

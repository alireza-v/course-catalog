from django.test import TestCase
import pytest
from .models import *

@pytest.fixture
def createVideo(db):
    """ create Video instance """

    return Video.objects.create(
        title="videoTitle",
        video_file="somePath/videos/video.mp4",
    )

@pytest.fixture
def parentCategory(db):
    """ create parent category """

    return Category.objects.create(
        title="programming",
    )

@pytest.fixture
def subcategory(db, parentCategory):
    """ create subcategory """

    return Category.objects.create(
        title="backend",
        parent=parentCategory,
    )

@pytest.fixture
def createCourse(db, createVideo, parentCategory):
    """ create course """

    userProfile=UserProfile.objects.create(
        email="testUser@email.com",
        first_name="john",
        last_name="doe",
        phone="6821567754362",
        role=UserProfile.Roll.STUDENT,
    )
    return Course.objects.create(
        user=userProfile,
        title="basics of Python",
        description="Python is a versatile programming language that could be used in different areas such as web-development, data-science, machince-learning and many more.",
        video=createVideo,
        category=parentCategory,
    )

@pytest.mark.django_db
class TestVideo:

    def testVideo(self, createVideo):
        """ video test creation """

        video=createVideo
        assert video.title=="videoTitle"
        assert video.video_file=="somePath/videos/video.mp4"
        assert str(video)=="videoTitle"

@pytest.mark.django_db
class TestCategory:

    def testCategoryCreation(self, parentCategory):
        """ category test creation without the parent """

        category=parentCategory
        assert category.title=="programming"
        assert category.parent is None
        assert category.subcategories.count()==0
        assert str(category)=="programming"

    def testCategoryWithSubcategory(self, subcategory, parentCategory):
        """ category test creation with the subcategory """

        assert subcategory.title=="backend"
        assert subcategory.parent==parentCategory
        assert parentCategory.subcategories.count()==1
        assert parentCategory.subcategories.first()==subcategory
        assert str(parentCategory)=="programming"

@pytest.mark.django_db
class TestCourse:

    def testCourse(self, createCourse):
        course=createCourse
        assert str(course)=="basics of Python"
        assert course.user.email=="testUser@email.com"
        assert course.video.title=="videoTitle"
        assert course.category.title=="programming"


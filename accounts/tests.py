from django.test import TestCase
import pytest
from django.contrib.auth import get_user_model
from .models import *

UserProfile=get_user_model()

@pytest.fixture
def createUser():
    """ fixture to create student user """
    def makeUser(roll=UserProfile.Roll.STUDENT):
        return UserProfile.objects.create_user(
            email="testuser@email.com",
            password="testpassword123",
            first_name="alex",
            last_name="green",
            phone="123456789",
            role=roll,
        )
    return makeUser
@pytest.fixture
def createMentor():
    """ fixture to create mentor user """
    return UserProfile.objects.create_user(
        email="mentor@email.com",
        password="mentorpassword123",
        first_name="john",
        last_name="doe",
        phone="9873654198",
        role=UserProfile.Roll.MENTOR,
    )

@pytest.mark.django_db
class TestUserProfile:

    def testCreateStudentUser(self, createUser):
        """ test creation student user """

        user=createUser()
        assert user.email=="testuser@email.com"
        assert user.first_name=="alex"
        assert user.last_name=="green"
        assert user.role==UserProfile.Roll.STUDENT

    def testCreateMentorUser(self, createMentor):
        """ test creation of mentor user """

        mentor=createMentor
        assert mentor.email=="mentor@email.com"
        assert mentor.role==UserProfile.Roll.MENTOR

    def testUserHasPerm(self, createUser):
        """ test default permission """

        user=createUser()
        assert user.has_perm("any_perm") is True

    def testMentorHasPerm(self, createMentor):
        """ test if mentor has permission """

        mentor=createMentor
        assert mentor.has_perm("create_course") is True

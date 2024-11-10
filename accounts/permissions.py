from rest_framework.permissions import BasePermission

from .models import *


class IsMentorPerm(BasePermission):
    """Mentorship role permission"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == Role.MENTOR


class IsStudentPerm(BasePermission):
    """Student role permission"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == Role.STUDENT


class IsStudentOrMentor(BasePermission):
    """Permission for both student and mentor role"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == Role.STUDENT or request.user.role == Role.MENTOR
        )


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser

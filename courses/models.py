from django.db import models

from accounts.models import BaseModel, UserProfile

from .validators import validateVideoFormat


class Video(BaseModel):
    """represent video uploaded by users"""

    title = models.CharField(max_length=20, null=True)
    video_file = models.FileField(
        upload_to="videos/", null=True, blank=True, validators=[validateVideoFormat]
    )
    # length=models.DurationField(help_text="duration of the video")

    def __str__(self):
        return self.title


class Category(BaseModel):
    """represent category for organizing courses"""

    name = models.CharField(max_length=50, null=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subcategories",
    )

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        if self.parent:
            return f"{self.parent.name}: {self.name}"
        return self.name


class Course(BaseModel):
    """represent course uploaded by users"""

    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="courses"
    )
    title = models.CharField(max_length=50, null=True, blank=True, unique=True)
    description = models.TextField(null=True, blank=True)
    video = models.FileField(upload_to="videos/", null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class ScoreChoices(models.IntegerChoices):
    BAD = 1, "Bad"
    AVERAGE = 2, "Average"
    GOOD = 3, "Good"


class Comment(BaseModel):
    """represent comment, rating on courses by verified users"""

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, null=True, related_name="comments"
    )
    description = models.TextField()
    score = models.IntegerField(choices=ScoreChoices.choices, null=True, blank=True)

    def __str__(self):
        return self.get_score_display()


class Favorite(BaseModel):
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="favorites_user"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="favorites_course"
    )

    class Meta:
        """ensure every user can favorite a course only once"""

        unique_together = ("course", "user")

    def __str__(self):
        return self.course.title


class Wallet(models.Model):
    # """represent users's wallet for transactions and balance"""

    ...

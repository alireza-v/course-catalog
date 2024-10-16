from django.db import models
from django.core.exceptions import ValidationError

from accounts.models import *
from .validators import *

class BaseModel(models.Model):
    timestamp=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True

class Video(BaseModel):
    title=models.CharField(max_length=20, null=True)
    video_file=models.FileField(upload_to="videos/", null=True, blank=True, validators=[validateVideoFormat])
    # length=models.DurationField(help_text="duration of the video")

    def __str__(self):
        return self.title

class Category(BaseModel):
    title=models.CharField(max_length=50)
    parent=models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="subcategories")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural="Categories"

class Course(BaseModel):
    user=models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="courses")
    title=models.CharField(max_length=50, null=True, blank=True)
    description=models.TextField(null=True, blank=True)
    video=models.ForeignKey(Video, on_delete=models.CASCADE, blank=True)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Comment(BaseModel):

    class Score(models.IntegerChoices):
        BAD=1, "Bad"
        AVERAGE=2, "Average"
        GOOD=3, "Good"

    course=models.ForeignKey(Course, on_delete=models.CASCADE, null=True, related_name="comments")
    description=models.TextField()
    score=models.IntegerField(choices=Score.choices, null=True, blank=True)

    def __str__(self):
        return f"{self.get_score_display()}"

class Wallet(models.Model):
    ...


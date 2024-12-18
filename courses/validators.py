from django.core.exceptions import ValidationError


def validateVideoFormat(file):
    """Validate video file format"""
    if not file.name.endswith(".mp4"):
        raise ValidationError("only mp4 video format is accepted")

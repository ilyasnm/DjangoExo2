from django.db import models

from contextvars import Token
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from exo2 import migrations

class Video(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    analysis_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title


class VideoAnalysis(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    transcription = models.TextField()

    def __str__(self):
        return f"Analysis for {self.video.title}"







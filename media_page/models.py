from django.db import models
from django.utils import timezone
from django.urls import reverse
from .fields import *
# Create your models here.


class Photo(models.Model):
    uid = models.CharField(max_length=500, blank=True, null=True)
    file = RestrictedFileField(
        upload_to='image/', blank=True, null=True, content_types=['image/jpg', 'image/png'], max_upload_size=20971520, min_upload_size=0)
    type = models.CharField(max_length=500, blank=True,
                            null=True, default=file.content_types)
    media_filename = models.CharField(max_length=500, blank=True, null=True)
    upload_timestamp = models.DateTimeField(auto_now_add=True)

    # def get_absolute_url(self):
    #     return reverse('media_filename', kwargs={str: self.str})

    class Meta:
        db_table = "image"


class Video(models.Model):
    uid = models.CharField(max_length=500, blank=True,
                           null=True, default='uid')
    type = models.CharField(max_length=500, blank=True,
                            null=True, default='video')
    file = RestrictedFileField(
        upload_to='video/', blank=True, null=True, content_types=['video/mp4', 'video/mkv'], max_upload_size=20971520, min_upload_size=1572864)
    media_filename = models.CharField(max_length=500, blank=True, null=True)
    upload_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "video"

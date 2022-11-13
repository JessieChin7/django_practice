from rest_framework import serializers
from .fields import *
from .models import *
from django.core.exceptions import ValidationError


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = '__all__'

    def validate_file(self, image):
        MAX_IMAGE_SIZE = 20971520
        MIN_IMAGE_SIZE = 0
        ALLOW_TYPES = ['image/jpg', 'image/png', 'image/jpeg']
        file = image
        if file.size > MAX_IMAGE_SIZE:
            raise ValidationError("File size too big!")
        elif file.size < MIN_IMAGE_SIZE:
            raise ValidationError("File size too big!")

        if file.content_type not in ALLOW_TYPES:
            raise ValidationError("Wrong file type!")


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

    def validate_file(self, video):
        MAX_IMAGE_SIZE = 20971520
        MIN_IMAGE_SIZE = 1572864
        ALLOW_TYPES = ['video/mp4', 'video/mkv']
        file = video
        if file.size > MAX_IMAGE_SIZE:
            raise ValidationError("File size too big!")
        elif file.size < MIN_IMAGE_SIZE:
            raise ValidationError("File size too big!")
        if file.content_type not in ALLOW_TYPES:
            raise ValidationError("Wrong file type!")

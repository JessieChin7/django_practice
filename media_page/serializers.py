from .models import Photo, Video
from rest_framework.serializers import ModelSerializer, ValidationError


class DynamicFieldsModelSerializer(ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class PhotoSerializer(DynamicFieldsModelSerializer):
    def validate(self, data):
        content_type = data['file'].content_type
        if content_type in ['image/jpg', 'image/jpeg', 'image/png']:
            if data['file'].size > 20971520:
                raise ValidationError(
                    'Doesn\'t fit max file size')
            if data['file'].size < 0:
                raise ValidationError(
                    'Doesn\'t fit min file size')
        else:
            print(content_type)
            raise ValidationError(
                'This file type is not allowed')
        return data

    class Meta:
        model = Photo
        # fields = '__all__'
        fields = ['id', 'uid', 'type', 'file', 'media_filename']


class VideoSerializer(DynamicFieldsModelSerializer):
    def validate(self, data):
        content_type = data['file'].content_type
        if content_type in ['video/mp4', 'video/mkv']:
            if data['file'].size > 20971520:
                raise ValidationError(
                    'Doesn\'t fit max file size')
            if data['file'].size < 1572864:
                raise ValidationError(
                    'Doesn\'t fit min file size')
        else:
            raise ValidationError(
                'This file type is not allowed')
        return data

    class Meta:
        model = Video
        # fields = '__all__'
        fields = ['id', 'uid', 'type', 'file', 'media_filename']

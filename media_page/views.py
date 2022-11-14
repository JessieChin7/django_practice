from dataclasses import field
from urllib import request
from django.shortcuts import render, redirect
from django.http import FileResponse, HttpResponseRedirect, HttpResponse
from .models import Photo, Video
import os
###API###
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import renderers
from django.shortcuts import get_object_or_404
from pracsite import settings
###API###


class PassthroughRenderer(renderers.BaseRenderer):
    """
        Return data as-is. View should supply a Response.
    """
    media_type = ''
    format = ''

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


class PhotoViewSet(viewsets.ModelViewSet):
    lookup_value_regex = r"[\w.]+"
    lookup_field = "media_filename"
    """
    A viewset that provides the standard actions
    """
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def overwrite(self, serializer, instance):
        new_instance = self.request.data
        dot = new_instance['file'].name.index('.')
        new_instance['file'].name = str(
            new_instance['uid'])+(new_instance['file'].name[dot:])
        instance.file = new_instance['file']
        instance.media_filename = new_instance['file'].name
        instance.save(update_fields=['file', 'media_filename'])

        serializer = PhotoSerializer(instance, data=self.request.data)
        if serializer.is_valid():
            serializer.save()

        return serializer

    def perform_create(self, serializer):
        instance = self.request.data
        if instance['uid'] == None:
            instance['uid'] = self.request.user
        dot = instance['file'].name.index('.')
        instance['file'].name = str(
            instance['uid'])+(instance['file'].name[dot:])
        if (serializer.is_valid(raise_exception=True)):
            serializer.save(uid=instance['uid'], type='image',
                            file=instance['file'],
                            media_filename=instance['file'].name)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid(raise_exception=True)):
            old = Photo.objects.filter(uid=request.data['uid'])
            if old:
                old_data = Photo.objects.get(uid=request.data['uid'])
                serializer = self.overwrite(serializer, old_data)
            else:
                self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        response_serializer = {'id': serializer.data['id'], 'uid': serializer.data['uid'],
                               'type': serializer.data['type'], 'media_filename': serializer.data['media_filename']}
        response_data = {
            "success": "200 OK",
            # "user": response_serializer
        }
        return Response(response_data, headers=headers)
        # return HttpResponse(response_data)

    def clear(self, request, *args, **kwargs):
        Photo.objects.all().delete()

    @action(methods=['get'], detail=False, renderer_classes=(PassthroughRenderer,), url_path="<media_filename>",)
    def download(self, request, *args, **kwargs):
        # filename = request.GET.get('media_filename')
        filename = self.kwargs['media_filename'][1:-1]
        # instance = self.get_object()
        print("filename:", filename)
        print(type(filename))
        instance = Photo.objects.get(
            media_filename=filename)
        print("instance:", instance)
        img = instance.file
        path = img.path
        response = FileResponse(open(path, 'rb'),
                                content_type='image/*')
        response['Content-Length'] = os.path.getsize(path)
        response['Content-Disposition'] = "attachment; filename=%s" % img.name
        return response


class VideoViewSet(viewsets.ModelViewSet):
    lookup_value_regex = r"[\w.]+"
    lookup_field = "media_filename"
    """
    A viewset that provides the standard actions
    """
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['media_filename']

    def overwrite(self, serializer, instance):
        new_instance = self.request.data
        dot = new_instance['file'].name.index('.')
        new_instance['file'].name = str(
            new_instance['uid'])+(new_instance['file'].name[dot:])
        instance.file = new_instance['file']
        instance.media_filename = new_instance['file'].name
        instance.save(update_fields=['file', 'media_filename'])

        serializer = VideoSerializer(instance, data=self.request.data)
        if serializer.is_valid():
            serializer.save()

        return serializer

    def perform_create(self, serializer):
        instance = self.request.data
        if instance['uid'] == None:
            instance['uid'] = self.request.user
        dot = instance['file'].name.index('.')
        instance['file'].name = str(
            instance['uid'])+(instance['file'].name[dot:])
        if (serializer.is_valid(raise_exception=True)):
            serializer.save(uid=instance['uid'], type='video',
                            file=instance['file'],
                            media_filename=instance['file'].name)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if (serializer.is_valid(raise_exception=True)):
            old = Video.objects.filter(uid=request.data['uid'])
            if old:
                old_data = Video.objects.get(uid=request.data['uid'])
                serializer = self.overwrite(serializer, old_data)
            else:
                self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        response_serializer = {'id': serializer.data['id'], 'uid': serializer.data['uid'],
                               'type': serializer.data['type'], 'media_filename': serializer.data['media_filename']}
        response_data = {
            "success": "200 OK",
            # "user": response_serializer
        }
        return Response(response_data, headers=headers)
        # return HttpResponse(status=200)

    def clear(self, request, *args, **kwargs):
        Photo.objects.all().delete()

    @action(methods=['get'], detail=False, renderer_classes=(PassthroughRenderer,))
    def download(self, request, *args, **kwargs):
        # filename = request.GET.get('media_filename')
        filename = self.kwargs['media_filename'][1:-1]
        # instance = self.get_object()
        print("filename:", filename)
        print(type(filename))
        instance = Video.objects.get(
            media_filename=filename)
        img = instance.file
        path = img.path
        response = FileResponse(open(path, 'rb'),
                                content_type='video/*')
        response['Content-Length'] = os.path.getsize(path)
        response['Content-Disposition'] = "attachment; filename=%s" % img.name
        return response

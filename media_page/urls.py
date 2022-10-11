from media_page import views
from rest_framework.routers import DefaultRouter
from django.urls import path, include, re_path
from .views import *
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
### API ###
from rest_framework import renderers
lookup_value_regex = r"[\w.]+"
router = DefaultRouter()
router.register(r'api/face/upload/image', views.PhotoViewSet, basename="photo")
router.register(r'api/face/upload/video', views.VideoViewSet, basename="video")
router.register(r'api/face/image', views.PhotoViewSet,
                basename="photo_download")
router.register(r'api/face/video', views.VideoViewSet,
                basename="video_download")


urlpatterns = [
    path('', include(router.urls)),
    path('api/face/image/<media_filename>',
         views.PhotoViewSet.as_view({'get': 'download', })),
    path('api/face/video/<media_filename>',
         views.VideoViewSet.as_view({'get': 'download', })),
]


# urlpatterns = format_suffix_patterns([
#     path('api/face/upload/image/', photo_list, name='photo-list'),
#     path('api/face/image/', photo_detail, name='photo-list'),
#     path('api/face/image/<str:media_filename>',
#          photo_download, name='photo-download'),
# ])
###

# urlpatterns = [

#     # path('', views.index, name='Index'),
#     # path('download/', views.download, name='Download'),
#     # path('register/', views.sign_up, name='Register'),
#     # path('login/', views.sign_in, name='Login'),
#     # path('logout/', views.log_out, name='Logout'),
# ]

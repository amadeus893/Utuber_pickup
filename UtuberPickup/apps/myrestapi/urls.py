from django.urls import path

from .views import views

# app_name = 'myrestapi'
urlpatterns = [
    # 動画切り抜き画面
    path('', views.index, name='index'),
    path('execute/', views.execute, name='execute'),

    # 動画ランキング画面
    path('vtuberPhotoFramesIndex/', views.vtuberPhotoFramesIndex, name='vtuberPhotoFramesIndex'),
    path('vtuberPhotoFramesIndex/getVtuberPhotoFrames/', views.getVtuberPhotoFrames, name='getVtuberPhotoFrames'),
]

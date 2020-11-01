import jsonfield
from django.db import models


class ChatCacheModel(models.Model):
    video_id = models.CharField(max_length=255, primary_key=True)
    channel_id = models.CharField(max_length=255)
    published_at = models.DateTimeField()
    time_list = jsonfield.JSONField()
    moderator_chat_list = jsonfield.JSONField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class M_Vtuber_InformationModel(models.Model):
    channel_id = models.CharField(max_length=255, primary_key=True)
    # affiliation = models.IntegerField(default=0, primary_key=True, editable=False)
    channel_name = models.CharField(max_length=255)
    vtuber_name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

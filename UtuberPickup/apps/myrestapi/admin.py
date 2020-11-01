# Register your models here.
from django.contrib import admin

from apps.myrestapi.models import ChatCacheModel
from apps.myrestapi.models import M_Vtuber_InformationModel

admin.site.register(ChatCacheModel)
admin.site.register(M_Vtuber_InformationModel)

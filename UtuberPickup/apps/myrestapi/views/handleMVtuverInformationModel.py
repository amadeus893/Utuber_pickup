import logging
import os
import django


def __init__():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    django.setup()


# @database_sync_to_async
def getMVtuberInformationModel():
    model = MVtuberInformationModel.objects.all().distinct('channel_id')
    logging.info(model)
    return model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
from apps.myrestapi.models import M_Vtuber_InformationModel as MVtuberInformationModel

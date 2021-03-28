import logging
import os
import django


def __init__():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    django.setup()


# @database_sync_to_async
def insertChatCacheData(video_id, channelId, publishedAt, time_list, moderator_chat_list):
    model = ChatCacheModel(video_id=video_id
                           , channel_id=channelId
                           , published_at=publishedAt
                           , time_list=time_list
                           , moderator_chat_list=moderator_chat_list)
    model.save()


# @database_sync_to_async
def deleteChatCacheData(video_id):
    model = ChatCacheModel.objects.get(video_id=video_id)
    model.delete()


# @database_sync_to_async
def getChatCacheData(video_id):
    model = ChatCacheModel.objects.get(video_id=video_id)
    logging.info(model)
    return model.time_list, model.moderator_chat_list


# @database_sync_to_async
def getRankData(start_date, end_date, channel_id):

    try:
        if channel_id != 'NoFilter':
            models = list(ChatCacheModel.objects
                          .filter(published_at__range=(start_date, end_date))
                          .filter(channel_id=channel_id)
                          .values('video_id', 'time_list'))
        else:
            models = list(ChatCacheModel.objects
                          .filter(published_at__range=(start_date, end_date))
                          .values('video_id', 'time_list'))

        models.sort(key=lambda x: int(x['time_list']['0']['commentCnt']), reverse=True)
        # 取得する動画は最大コメント数の多い順10件
        return models[:10]
    except Exception as e:
        print(e)
        e.with_traceback()


# @database_sync_to_async
def existChatCacheData(video_id):
    try:
        model = ChatCacheModel.objects.get(video_id=video_id)
        logging.info(model)
        return True
    except ChatCacheModel.DoesNotExist:
        logging.info("Cache does not exist.")
        return None


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
from apps.myrestapi.models import ChatCacheModel
# print(getChatCacheData('KEMHmwTzXkI'))
# deleteChatCacheData('KEMHmwTzXkI')
# print(getChatCacheData('KEMHmwTzXkI'))

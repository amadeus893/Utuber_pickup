import logging
import json
from django.http import HttpResponse
from django.template import loader
from apps.myrestapi.views.getYoutubeLiveComments import getYoutubeLiveComments as gylc
from apps.myrestapi.views.evaluateLiveChat import evaluateLiveChat as evl
from apps.myrestapi.views.handleYoutubeAPI import handleYoutubeAPI as hndlYt
import apps.myrestapi.views.handleChatCacheModel as hccm
import apps.myrestapi.views.handleMVtuverInformationModel as hmvi


def index(request):
    try:
        # HTMLテンプレートオブジェクトを取得
        template = loader.get_template('myrestapi/index.html')
        context = {
        }

        return HttpResponse(template.render(context, request))

    except Exception as e:
        logging.exception(e)


def execute(request):
    try:
        result = {}
        if request.method == 'POST':
            target_url = request.POST['target_url']
            video_id = target_url.split('/')[3]

            # 動画のダウンロード
            # dlv.downloadVideo(target_url)

            # スクレイピング
            # if cache.get(video_id) is None:
            #     comment_data = gylc.getYoutubeLiveComments(video_id)
            #     cache.set(video_id, comment_data, 60 * 60 * 24 * 7)
            # else:
            #     comment_data = cache.get(video_id)
            if hccm.existChatCacheData(video_id) is None:
                comment_data = gylc.getYoutubeLiveComments(video_id)
                if len(comment_data) is not 0:
                    time_list, moderator_chat_list = evl.evaluateLiveChat(comment_data)
                    video_info = hndlYt.getVideoInfoFromVideoID(video_id)
                    channelId = video_info['items'][0]['snippet']['channelId']
                    # published_at = video_info['items'][0]['snippet']['publishedAt']
                    published_at = video_info['items'][0]['liveStreamingDetails']['actualEndTime']
                    hccm.insertChatCacheData(video_id, channelId, published_at, time_list, moderator_chat_list)
            else:
                time_list, moderator_chat_list = hccm.getChatCacheData(video_id)

            # 画面への戻り値設定
            dict_responce = {'result': time_list, 'moderator_chat_list': moderator_chat_list}

            # 動画の切り抜き
            # cyv.clipVideo(video_id)

        return HttpResponse(json.dumps(dict_responce), content_type='application/json')

    except Exception as e:
        print(e)
        logging.exception(e)


def vtuberPhotoFramesIndex(request):
    try:
        # HTMLテンプレートオブジェクトを取得
        template = loader.get_template('myrestapi/vtuber_photo_frames.html')
        context = {
        }

        return HttpResponse(template.render(context, request))

    except Exception as e:
        logging.exception(e)


def getVtuberPhotoFrames(request):
    try:
        result = {}
        if request.method == 'POST':
            if request.POST['func'] == 'getVtuberPhotoFrames':
                target_date = request.POST['target_date']

                # 検索開始日
                start_date = target_date + ' 00:00:00'

                # 検索終了日
                end_date = target_date + ' 23:59:59'

                # チャンネルID
                channel_id = request.POST['channel_id']

                # 指定期間, チャンネルIDの動画取得
                result = hccm.getRankData(start_date, end_date, channel_id)

            elif request.POST['func'] == 'getVtuberList':

                # マスタから全Vtuber氏名取得
                result = list((hmvi.getMVtuberInformationModel()).values('channel_id', 'vtuber_name'))

            return HttpResponse(json.dumps(result), content_type='application/json')

    except Exception as e:
        print(e)
        logging.exception(e)



import os

import django
import apps.myrestapi.views.handleMVtuverInformationModel as hmvi
from django.core.management.base import BaseCommand
from apps.myrestapi.views.getYoutubeLiveComments import getYoutubeLiveComments as gylc
from apps.myrestapi.views.evaluateLiveChat import evaluateLiveChat as evl
from apps.myrestapi.views.handleYoutubeAPI import handleYoutubeAPI as hndlYt
from datetime import datetime, timedelta
from googleapiclient.discovery import build

from config.settings import env


class Command(BaseCommand):
    help = 'Get Youtube Live Chat Comments by regular batch process.'

    def add_arguments(self, parser):
        parser.add_argument('key_id', nargs='+', type=int)

    def handle(self, *args, **options):
        API_KEY = [
            env('API_KEY2')
            , env('API_KEY3')
            , env('API_KEY4')
            , env('API_KEY5')
        ]
        API_SERVICE_NAME = "youtube"
        API_VERSION = "v3"

        # マスタから全チャンネルID取得
        entList = list((hmvi.getMVtuberInformationModel()).values('channel_id'))

        # チャンネルIDのみ抽出
        CHANNEL_ID_LIST = []
        for ent in entList:
            CHANNEL_ID_LIST.append(ent['channel_id'])

        # youtubeAPIオブジェクト生成
        youtube = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY[options['key_id'][0]])

        # 3日前〜1日前の範囲で動画IDを取得
        for i in range(2):
            targetDate = datetime.strftime((datetime.today() - timedelta(days=(i + 1))), '%Y-%m-%d')
            videoInfoList = []
            # 動画ID一覧を取得
            for channelId in CHANNEL_ID_LIST:
                search_response = youtube.search().list(
                    part='id,snippet',
                    channelId=channelId,
                    publishedAfter=targetDate + 'T00:00:00Z',
                    publishedBefore=targetDate + 'T23:59:00Z',
                    maxResults=50
                ).execute()

                for res in search_response.get('items', []):
                    if 'videoId' in res['id']:
                        resDict = {
                            'videoId': res['id']['videoId']
                            , 'channelId': res['snippet']['channelId']
                            , 'publishedAt': res['snippet']['publishedAt']
                        }
                    else:
                        resDict = {
                            'videoId': res['snippet']['thumbnails']['default']['url'].split("/")[4]
                            , 'channelId': res['snippet']['channelId']
                            , 'publishedAt': res['snippet']['publishedAt']
                        }
                    videoInfoList.append(resDict)

            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
            django.setup()
            import apps.myrestapi.views.handleChatCacheModel as hccm

            # 削除処理 TODO 一定期間を過ぎた動画に関してはキャッシュを削除する
            # hccm.deleteChatCacheData(video_id)

            # スクレイピング＆キャッシュテーブルに保存
            for videoInfo in videoInfoList:
                print('-----------------------------------------')
                print('videoId = ' + videoInfo['videoId'])
                print('channelId = ' + videoInfo['channelId'])
                print('publishedAt = ' + videoInfo['publishedAt'])
                if hccm.existChatCacheData(videoInfo['videoId']) is None:
                    comment_data = gylc.getYoutubeLiveComments(videoInfo['videoId'])
                    if comment_data.__sizeof__() is not 0:
                        timeList, moderatorChatList = evl.evaluateLiveChat(comment_data)
                        if timeList is not None:
                            # videoIdから配信終了日時を取得
                            video_info = hndlYt.getVideoInfoFromVideoID(videoInfo['videoId'])
                            publishedAt = video_info['items'][0]['liveStreamingDetails']['actualEndTime']
                            print('actualEndTime = ' + publishedAt)
                            hccm.insertChatCacheData(videoInfo['videoId']
                                                     , videoInfo['channelId']
                                                     , publishedAt
                                                     , timeList
                                                     , moderatorChatList
                                                     )
                        else:
                            print('Evaluation Error.')
                    else:
                        print('Comment Data is not found.')
                else:
                    print('Target VideoId is already exist.')
            # else:
            #     timeList, moderatorChatList = hccm.getChatCacheData(videoId)
            #     print(timeList)
            #     print(moderatorChatList)

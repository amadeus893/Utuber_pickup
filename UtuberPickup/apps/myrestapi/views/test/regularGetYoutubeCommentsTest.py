from datetime import datetime, timedelta
from googleapiclient.discovery import build

# API_KEY = 'AIzaSyB2FtPUdnvWaUudQHrH18ecP5MQvpXPbfE'
API_KEY = 'AIzaSyA-BDWStA_gcgeXrSi5j1xlICurp548wiU'
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
# CHANNEL_ID_LIST = ['UCvaTdHTWBGv3MKj3KVqJVCw',
#                    'UChAnqc_AY5_I3Px5dig3X1Q',
#                    'UC1DCedRgGHBdm81E1llLhOQ',
#                    'UCqm3BQLlJfvkTsX_hvm0UmA']
CHANNEL_ID_LIST = ['UCvaTdHTWBGv3MKj3KVqJVCw']
videoIDList = []

# youtubeAPIオブジェクト生成
youtube = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)
# 現在日付の前日を設定
for i in range(3):
    targetDate = datetime.strftime((datetime.today() - timedelta(days=i)), '%Y-%m-%d')
    print(targetDate)

# 動画ID一覧を取得
# for channelId in CHANNEL_ID_LIST:
#     search_response = youtube.search().list(
#         part='id,snippet',
#         channelId=channelId,
#         publishedAfter=targetDate + 'T00:00:00Z',
#         publishedBefore=targetDate + 'T23:59:00Z',
#         # eventType='completed',
#         maxResults=50
#     ).execute()

# videos_response = youtube.videos().list(
#     part="id,liveStreamingDetails",
#     id='MDSrDjJEJeA'
# ).execute()
# print(videos_response['items'][0]['liveStreamingDetails']['actualEndTime'])

    # for res in search_response.get('items', []):
    #     videoIDList.append(res['id']['videoId'])
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
# django.setup()
# import myrestapi.views.handleChatCacheModel as hccm
#
# # 削除処理 TODO 一定期間を過ぎた動画に関してはキャッシュを削除する
# # hccm.deleteChatCacheData(video_id)
#
# # スクレイピング＆キャッシュテーブルに保存
# for videoId in videoIDList:
#     print('videoId :' + videoId)
#     if hccm.existChatCacheData(videoId) is None:
#         comment_data = gylc.getYoutubeLiveComments(videoId)
#         if len(comment_data) is not 0:
#             timeList, moderatorChatList = evl.evaluateLiveChat(comment_data)
#             hccm.insertChatCacheData(videoId, timeList, moderatorChatList)
    # else:
    #     timeList, moderatorChatList = hccm.getChatCacheData(videoId)
    #     print(timeList)
    #     print(moderatorChatList)

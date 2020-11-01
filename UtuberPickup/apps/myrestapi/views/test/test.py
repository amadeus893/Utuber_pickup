from apps.myrestapi.views.handleYoutubeAPI import *

if __name__ == '__main__':
    # 動画のURLを入れてください
    target_url = 'https://youtu.be/Fmn3VdPdzR4'
    video_id = target_url.split('/')[3]

    video_info = handleYoutubeAPI.getVideoInfoFromVideoID(video_id)
    channelId = video_info['items'][0]['snippet']['channelId']
    published_at = video_info['items'][0]['snippet']['publishedAt']
    actualEndTime = video_info['items'][0]['liveStreamingDetails']['actualEndTime']
    print(channelId)
    print(published_at)
    print(actualEndTime)
    # 動画のダウンロード
    # dlv.downloadVideo(target_url)

    # スクレイピング
    # gylc.getYoutubeLiveComments(video_id)

    # チャット評価S
    # evl.evaluateLiveChat(video_id)

    # 動画の切り抜き
    # cyv.clipVideo(video_id)

    # settings.configure(CACHES={
    #     'default': {
    #         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
    #         'LOCATION': '127.0.0.1:11211',
    #         'TIMEOUT': 60 * 60 * 24 * 7,
    #         'OPTIONS': {
    #             'server_max_value_length': 1024 * 1024 * 2,
    #         }
    #     }
    # })
    # cache.set('boo', 'baa')
    # print(cache.get('foo'))
    # print(cache.get('boo'))

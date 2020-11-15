import json
import requests
import config.settings as settings

class handleYoutubeAPI:
    def getVideoInfoFromVideoID(videoId):
        options = {
            'key': settings.API_KEY1
            , 'id': videoId
            , 'part': 'id,snippet,contentDetails,statistics,liveStreamingDetails'
        }

        r = requests.get('https://www.googleapis.com/youtube/v3/videos', params=options)
        # videoInfo = json.dumps(r.json(), indent=2, ensure_ascii=False)
        videoInfo = r.json()
        # print('videoInfo:' + videoInfo)
        return videoInfo


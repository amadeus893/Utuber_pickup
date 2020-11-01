import json
import requests

from config.settings import env


class handleYoutubeAPI:
    def getVideoInfoFromVideoID(videoId):
        API_KEY = env('API_KEY1');
        options = {
            'key': API_KEY
            , 'id': videoId
            , 'part': 'id,snippet,contentDetails,statistics,liveStreamingDetails'
        }

        r = requests.get('https://www.googleapis.com/youtube/v3/videos', params=options)
        # videoInfo = json.dumps(r.json(), indent=2, ensure_ascii=False)
        videoInfo = r.json()
        # print('videoInfo:' + videoInfo)
        return videoInfo


import os
import sys
import time
import requests
import pandas as pd
import httplib2
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

API_KEY = 'AIzaSyB2FtPUdnvWaUudQHrH18ecP5MQvpXPbfE'
CHANNEL_ID = 'UC3G0P5a2spWXN5Jq5K3EGNA'
base_url = 'https://www.googleapis.com/youtube/v3'
url = base_url + '/subscriptions?&channelId=%s&part=snippet'
headers = {'authorization': 'Bearer ya29.a0AfH6SMC0bYEt9oSGTwM1fI9h99lo9376FuBhmB-UJxu9q2KR6j9n3iriB3eIASmpsm1BjsSev7uI7Uqh8ZonniwN70o-hg406APfpWhNrmkAcJfMI2-S8tgTjH2KNPtY2zWjKSnzmbJMtunifmFxLAEre7XvRE64Vhs'}
infos = []

# oauth_url = 'https://oauth2.googleapis.com/token?' \
#             'code=4%2F1AEauAdI62JqsVUa-tbE81vXdgpDhu9o14DcThQAzjI_FMGD0rg9QGZUOVxB2CgCVxUeGMeFDeCeoEDnz3O6A6I&' \
#             'client_id=439506546659-i7jt1ts4lld1tq76h8d71l28gs7do8nc.apps.googleusercontent.com&' \
#             'client_secret=UYYgIe5W2KDhWQyIAaLkov0l&' \
#             'redirect_uri=http://www.google.com&' \
#             'grant_type=authorization_code'
#
# headers2 = {
#     'Content-Type':'application/x-www-form-urlencoded',
# }
#
# payload = {
#     'code': '4%2F1AH2fb6KQjFuCQTAvKQyFUCC7hPsCBGPafs6X_Pi_OSSB0aUCXoBATJcMaoZ8u6FsiOhpEc0CtrtP7X0xPUG3PI',
#     'client_id': '439506546659-i7jt1ts4lld1tq76h8d71l28gs7do8nc.apps.googleusercontent.com',
#     'client_secret': 'UYYgIe5W2KDhWQyIAaLkov0l',
#     'redirect_uri': 'http://www.google.com',
#     'grant_type': 'authorization_code'
# }

# oauth_url = 'https://accounts.google.com/o/oauth2/auth?' \
#             'client_id=439506546659-i7jt1ts4lld1tq76h8d71l28gs7do8nc.apps.googleusercontent.com&  \
#               redirect_uri=http://www.google.com& \
#               scope=https://www.googleapis.com/auth/youtube.read-only& \
#               response_type=code& \
#               access_type=offline'

CLIENT_SECRETS_FILE = "../../../data/client_secret.json"
MISSING_CLIENT_SECRETS_MESSAGE = "UYYgIe5W2KDhWQyIAaLkov0l"
YOUTUBE_READONLY_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def get_authenticated_service(args):
  flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
  scope=YOUTUBE_READONLY_SCOPE)

  storage = Storage("%s-oauth2.json" % sys.argv[0])
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
             http=credentials.authorize(httplib2.Http()))
# while True:
    # time.sleep(30)
# response = requests.Session().post('https://oauth2.googleapis.com/token', data=payload, headers=headers2)
# response = requests.Session().post(oauth_url)
# print(oauth_url)
# print(response)
# response = requests.Session().get(url % (CHANNEL_ID), headers=headers)
# if response.status_code != 200:
#     print('エラーで終わり')
#     break
# result = response.json()
# print(result)
    # infos.extend([
    #     [item['id']['videoId'], item['snippet']['title'], item['snippet']['description'], item['snippet']['publishedAt']]
    #     for item in result['items'] if item['id']['kind'] == 'youtube#video'
    # ])
    #
    # if 'nextPageToken' in result.keys():
    #     if 'pageToken' in url:
    #         url = url.split('&pageToken')[0]
    #     url += f'&pageToken={result["nextPageToken"]}'
    # else:
    #     print('正常終了')
    #     break

def get_subscription(youtube, channel_id):
  get_subscription_response = youtube.subscriptions().list(
    part='snippet',
    body=dict(
      snippet=dict(
        resourceId=dict(
          channelId=channel_id
        )
      )
    )).execute()

  return get_subscription_response["snippet"]

if __name__ == "__main__":
  argparser.add_argument("--channel-id", help="ID of the channel to subscribe to.",
                         default="UC3G0P5a2spWXN5Jq5K3EGNA")
  args = argparser.parse_args()
  youtube = get_authenticated_service('args')
  try:
    channel_title = get_subscription(youtube, args.channel_id)
    print(channel_title)
  except HttpError as e:
    print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
  else:
    print("A subscription to '%s' was added." % channel_title)
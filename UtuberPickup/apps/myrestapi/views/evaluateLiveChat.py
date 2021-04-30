import math

import pandas as pd
import matplotlib.pyplot as plt
import re
import datetime
from datetime import datetime as dt
import apps.myrestapi.views.extractFeatureWords as extFW
from apps.myrestapi.views.util import *

class evaluateLiveChat:
    def evaluateLiveChat(comment_data):

        # チャット投稿時間をHH:MM:SS形式に直して返却する
        def formatedTime(time_str):
            if re.match('^[0-9]:[0-9][0-9]$', time_str):
                time_str = '00:0' + time_str
            elif re.match('^[0-9][0-9]:[0-9][0-9]$', time_str):
                time_str = '00:' + time_str
            return dt.strptime(time_str, '%H:%M:%S')

        # チャット投稿時間を秒単位に直して返却する
        def formatedTime2Seconds(time):
            return time.hour * 3600 + time.minute * 60 + time.second

        # 時間形式が正しいかどうかを判定する
        def checkTimeFormat(time_str):
            if re.match('^[0-9]:[0-9][0-9]$', time_str):
                return True
            if re.match('^[0-9][0-9]:[0-9][0-9]$', time_str) :
                return True
            if re.match('^[0-9]:[0-9][0-9]:[0-9][0-9]$', time_str):
                return True
            if re.match('^[0-9][0-9]:[0-9][0-9]:[0-9][0-9]$', time_str):
                return True
            return False

        try:
            count = 0
            dict_time_text = []
            moderator_chat_list = []
            for line in comment_data:
                time_text = {}
                dict = eval(line)
                dict_item_action = dict['replayChatItemAction']['actions'][0]
                del dict

                if 'addChatItemAction' in dict_item_action:
                    dict_item = dict_item_action['addChatItemAction']['item']
                    # ノーマルチャットパターン
                    if 'liveChatTextMessageRenderer' in dict_item:
                        time_str = str(dict_item['liveChatTextMessageRenderer']['timestampText']['simpleText'])
                        # 時間が正しくない場合対象のコメントはスルー
                        if not checkTimeFormat(time_str):
                            continue
                        # ライブ配信開始前じゃない場合処理
                        if '-' not in time_str:
                            dict_runs = dict_item['liveChatTextMessageRenderer']['message']['runs'][0]
                            # 絵文字だけじゃない場合処理
                            if 'text' in dict_runs:
                                time_text['time'] = formatedTime(time_str)
                                time_text['text'] = str(dict_runs['text'])
                                dict_time_text.append(time_text)
                                # モデレーターの情報であれば保持
                                if 'authorBadges' in dict_item['liveChatTextMessageRenderer']:
                                    if 'モデレーター' == dict_item['liveChatTextMessageRenderer']['authorBadges'][0]['liveChatAuthorBadgeRenderer']['tooltip']:
                                        dict_moderator_chat = {
                                            'authorName': dict_item['liveChatTextMessageRenderer']['authorName']['simpleText']
                                            , 'authorPhoto': dict_item['liveChatTextMessageRenderer']['authorPhoto']['thumbnails'][0]['url']
                                            , 'time': time_str
                                            , 'text': str(dict_runs['text'])
                                        }
                                        moderator_chat_list.append(dict_moderator_chat)
                    # スーパーチャットパターン
                    elif 'liveChatPaidMessageRenderer' in dict_item:
                        time_str = str(dict_item['liveChatPaidMessageRenderer']['timestampText']['simpleText'])
                        # 時間が正しくない場合対象のコメントはスルー
                        if not checkTimeFormat(time_str):
                            continue
                        # ライブ配信開始前じゃない場合処理
                        if '-' not in time_str:
                            # メッセージつきの場合処理
                            if 'message' in dict_item['liveChatPaidMessageRenderer']:
                                dict_runs = dict_item['liveChatPaidMessageRenderer']['message']['runs'][0]
                                # 絵文字だけじゃない場合処理
                                if 'text' in dict_runs:
                                    time_text['time'] = formatedTime(time_str)
                                    time_text['text'] = str(dict_runs['text'])
                                    dict_time_text.append(time_text)

            # コメントを取得できなかった場合は処理終了
            if len(dict_time_text) == 0:
                return None, None

            # コメントを時間でソート
            df = pd.DataFrame(dict_time_text)
            df['time'] = pd.to_datetime(df['time'])
            df = df.sort_values(by='time', ascending=True)
            dfOrgn = df

            # コメントの開始・終了時間を保持
            start_limit_time = datetime.datetime(1900, 1, 1, 0, 0, 0)
            end_limit_time = df.tail(1).values[0][0]

            # 時間をインデックスに指定
            df.index = df['time']
            df['count'] = 1

            # 10分以下の動画は除外
            videoMin = (abs(end_limit_time - start_limit_time)).seconds / 60
            if videoMin < 10:
                return None, None
            # 開始終了3分以内は除外
            fIndexNames = df[df['time'] <= (start_limit_time + datetime.timedelta(minutes=3))].index
            eIndexNames = df[df['time'] >= (end_limit_time - datetime.timedelta(minutes=3))].index
            df.drop(fIndexNames, inplace=True)
            df.drop(eIndexNames, inplace=True)

            # 10分割してグループ化
            limit = datetime.timedelta(minutes=int((videoMin - 6) / 10))
            df['GroupID'] = (abs(df.index - start_limit_time) / limit).astype(int)
            grouped_df = df.groupby('GroupID')

            # グループ単位で上位1位を抽出
            df = pd.DataFrame()
            for id, sub_df in grouped_df:
                sub_df = pd.DataFrame(sub_df)
                sub_df.index = sub_df['time']
                sub_df = sub_df.resample('10S').sum()
                sub_df = sub_df.sort_values(by='count', ascending=False).head(1)
                df = pd.concat([df, sub_df])

            # グラフで盛り上がりを可視化
            # df.plot()
            # plt.show()

            # グループ結合後にコメント数が多い順に、上位10位を抽出
            df = df.sort_values(by='count', ascending=False).head(10)

            # 動画の開始、終了時刻を返却
            result = {}
            count = 0
            for time, row in df.iterrows():
                timeDict = {}
                start_time = time - datetime.timedelta(minutes=1)
                end_time = time + datetime.timedelta(minutes=1)

                # バイアスを調整
                if start_time < start_limit_time:
                    start_time = start_limit_time
                if end_time > end_limit_time:
                    end_time = end_limit_time

                timeDict['start'] = str(start_time).split(' ')[1]
                timeDict['end'] = str(end_time).split(' ')[1]
                timeDict['commentCnt'] = int(row['count'])

                # 開始〜終了時間までのコメントデータ取得
                dfTerm = dfOrgn[((dfOrgn['time'] >= datetime.datetime.strptime(str(start_time), '%Y-%m-%d %H:%M:%S'))
                                 & (dfOrgn['time'] <= datetime.datetime.strptime(str(end_time), '%Y-%m-%d %H:%M:%S')))]

                # この期間の重要単語を取得
                docList = getDocList(dfTerm)
                wdList = getWdList(dfTerm)
                timeDict['tags'] = extFW.extractFeatureWords(docList, wdList)

                # 結果リストに格納
                result[str(count)] = timeDict
                count += 1

            return result, moderator_chat_list

        except Exception as e:
            print(e)
            e.with_traceback()
            result = None
            moderator_chat_list = None
            return result, moderator_chat_list

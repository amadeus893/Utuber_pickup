import pandas as pd
import matplotlib.pyplot as plt
import re
import datetime
from datetime import datetime as dt

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

            # 10秒ごとのコメント総数を集計
            df = pd.DataFrame(dict_time_text)
            df = df.sort_values(by='time', ascending=True)

            # コメントの開始・終了時間を保持
            start_limit_time = datetime.datetime(1900, 1, 1, 0, 0, 0)
            end_limit_time = df.tail(1).values[0][0]

            df.index = df['time'] # 時間をインデックスに指定
            df['count'] = 1
            df = df.resample('10S').sum()

            # # グラフで盛り上がりを可視化
            # df.plot()
            # plt.show()

            # コメント数が多い順に、上位10位を抽出
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
                result[str(count)] = timeDict
                count += 1

            return result, moderator_chat_list

        except Exception as e:
            print(e)
            result = None
            moderator_chat_list = None
            return result, moderator_chat_list

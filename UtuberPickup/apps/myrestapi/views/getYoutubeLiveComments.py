from bs4 import BeautifulSoup
import json
import requests
import logging
import requests_cache

class getYoutubeLiveComments:
    def getYoutubeLiveComments(videoid):
        try:
            # target_url = 'https://www.youtube.com/watch?v=' + videoid
            target_url = 'https://youtu.be/' + videoid
            dict_str = ""
            next_url = ""
            comment_data = []
            count = 0
            session = requests.Session()
            headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

            # キャッシュ生成
            # requests_cache.install_cache('example', backend='sqlite', expire_after=60 * 60 * 24 * 7)

            # まず動画ページにrequestsを実行しhtmlソースを手に入れてlive_chat_replayの先頭のurlを入手
            html = requests.get(target_url)
            soup = BeautifulSoup(html.text, "html.parser")
            # for iframe in soup.find_all("iframe"):
            #     if("live_chat_replay" in iframe["src"]):
            #         next_url = iframe["src"]
            for scrp in soup.find_all("script"):
                if "ytInitialData = " in str(scrp):
                    dict_str = str(scrp).split("ytInitialData = ")[1]

                    # javascript表記なので更に整形. falseとtrueの表記を直す
                    dict_str = dict_str.replace("false", "False")
                    dict_str = dict_str.replace("true", "True")

                    # 辞書形式と認識すると簡単にデータを取得できるが, 末尾に邪魔なのがあるので消しておく（「空白2つ + \n + ;」を消す）
                    dict_str = dict_str.split(";</script>")[0]
                    dict = eval(dict_str)
                    continuation = dict['contents']['twoColumnWatchNextResults']['conversationBar']['liveChatRenderer']['continuations'][0]['reloadContinuationData']['continuation']
                    next_url = 'https://www.youtube.com/live_chat_replay?continuation=' + continuation
                    print(next_url)

            while(1):
                #取得したURL
                count += 1
                print(str(count) + '回目:' + next_url)

                response = session.get(next_url, headers=headers)
                html = response.content.decode(response.encoding)
                html = str(html).replace('&lt;script &gt;', ' <script >')
                html = str(html).replace('&lt;/script&gt;', ' </script>')
                soup = BeautifulSoup(html, "lxml")

                # 次に飛ぶurlのデータがある部分をfind_allで探してsplitで整形
                for scrp in soup.find_all("script"):
                    if "window[\"ytInitialData\"]" in str(scrp):
                        dict_str = str(scrp).split("[\"ytInitialData\"] = ")[1]

                # javascript表記なので更に整形. falseとtrueの表記を直す
                dict_str = dict_str.replace("false", "False")
                dict_str = dict_str.replace("true", "True")

                # 辞書形式と認識すると簡単にデータを取得できるが, 末尾に邪魔なのがあるので消しておく（「空白2つ + \n + ;」を消す）
                dict_str = dict_str.split(";\n")[0]

                # 辞書形式に変換
                dics = eval(dict_str)

                # "https://www.youtube.com/live_chat_replay?continuation=" + continue_url が次のlive_chat_replayのurl
                continue_url = dics["continuationContents"]["liveChatContinuation"]["continuations"][0]["liveChatReplayContinuationData"]["continuation"]
                next_url = "https://www.youtube.com/live_chat_replay?continuation=" + continue_url
                # dics["continuationContents"]["liveChatContinuation"]["actions"]がコメントデータのリスト。先頭はノイズデータなので[1:]で保存
                for samp in dics["continuationContents"]["liveChatContinuation"]["actions"][1:]:
                    comment_data.append(str(samp)+"\n")

        # next_urlが入手できなくなったら終わり
        except Exception as e:
            print(e)
            logging.info(msg="検索対象のURLが存在しないためスクレイピングを終了します。", stack_info=True)

        return comment_data
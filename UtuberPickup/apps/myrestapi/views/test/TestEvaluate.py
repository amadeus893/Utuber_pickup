import logging
from apps.myrestapi.views.getYoutubeLiveComments import getYoutubeLiveComments as gylc
from apps.myrestapi.views.evaluateLiveChat import evaluateLiveChat as evl

video_id = 'ADsvz5W2C9E'

def createTestData():
    try:
        comment_data = gylc.getYoutubeLiveComments(video_id)
        # comment_data = ['aim', 'buy']
        with open('../../../../../data/csv/test.csv', 'w') as f:
            for comment in comment_data:
                f.write(comment)

    except Exception as e:
        e.with_traceback()
        logging.exception(e)

def evaluate():
    try:

        comment_data = []
        with open('../../../../../data/csv/test.csv') as f:
            comment_data = f.readlines()

        time_list, moderator_chat_list = evl.evaluateLiveChat(comment_data)
        print(time_list)

    except Exception as e:
        print(e)
        e.with_traceback()
        logging.exception(e)


# 実行
# createTestData()
evaluate()
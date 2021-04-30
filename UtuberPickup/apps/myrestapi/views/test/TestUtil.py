import pandas as pd
from apps.myrestapi.views.util import *


def TEST_setDocList():
    data = [{"time":"1900-01-01 00:30:00", "text": "私はりんごを食べます。"},
            {"time":"1900-01-01 00:30:10", "text": "私はバナナを食べます。"},
            {"time": "1900-01-01 00:30:20", "text": "私はぶどうを食べます。"},
            {"time": "1900-01-01 00:30:30", "text": "私はりんごを食べます。"},
            ]

    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time'])
    print(getDocList(df))


def TEST_getWdList():
    data = [{"time":"1900-01-01 00:30:00", "text": "私はりんごを食べます。"},
            {"time":"1900-01-01 00:30:10", "text": "私はバナナを食べます。"},
            {"time": "1900-01-01 00:30:20", "text": "私はぶどうを食べます。"},
            {"time": "1900-01-01 00:30:30", "text": "私はりんごを食べます。"},
            ]

    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time'])
    print(getWdList(df))

# TEST_setDocList()
# TEST_getWdList()
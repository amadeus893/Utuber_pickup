import pandas as pd
from apps.myrestapi.views.extractFeatureWords import *
from apps.myrestapi.views.util import *


def TEST_extractFeatureWords():
    # data = [{"time":"1900-01-01 00:30:00", "text": "私はりんごを食べます。"},
    #         {"time":"1900-01-01 00:30:10", "text": "私はバナナを食べます。"},
    #         {"time": "1900-01-01 00:30:20", "text": "私はぶどうを食べます。"},
    #         {"time": "1900-01-01 00:30:30", "text": "私はりんごを食べます。"},
    #         ]

    dfOrgn = pd.read_csv('../../../../../data/csv/dfTerm5.csv', usecols=['time', 'text'])
    docList = getDocList(dfOrgn)

    dfTerm = pd.read_csv('../../../../../data/csv/dfTerm5.csv', usecols=['time', 'text'])
    wdList = getWdList(dfTerm)

    print(extractFeatureWords(docList, wdList))

TEST_extractFeatureWords()
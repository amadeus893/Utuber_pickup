import re
from janome.analyzer import Analyzer
from janome.tokenfilter import POSKeepFilter


def getAnalyzer():
    # アナライザーのフィルター
    token_filters = [
        POSKeepFilter(['名詞'])
    ]
    # フィルターからアナライザーを生成
    return Analyzer(token_filters=token_filters)


# 文章リスト取得処理
def getDocList(dfOrgn):
    analyzer = getAnalyzer()
    docList = []

    # コメントから名詞のみ抜き出してリスト化する
    for colname, df in dfOrgn.iterrows():
        doc = []
        for tok in analyzer.analyze(str(df[1])):
            parts = tok.part_of_speech.split(',')
            if parts[1] == '固有名詞' or parts[1] == '一般':
                doc.append(tok.surface)
        docList.append(doc)

    return docList

# 単語リスト取得処理
def getWdList(dfTerm):

    analyzer = getAnalyzer()
    wdList = []
    stopWdList = ['笑', 'w', '草', 'lol', 'LOL', 'W', 'LMAO', 'ー']
    re_kanji = re.compile(r'^[\u4E00-\u9FD0]+$')

    # コメントから名詞のみ抜き出してリスト化する
    for colname, df in dfTerm.iterrows():
        for tok in analyzer.analyze(str(df[1])):
            # 一度出現した単語は除外
            if tok.surface not in wdList:
                parts = tok.part_of_speech.split(',')
                if parts[1] == '固有名詞' or parts[1] == '一般':
                    # ストップワード除外
                    if tok.surface not in stopWdList:
                        # 漢字の場合は1文字でも採用
                        if re_kanji.fullmatch(tok.surface):
                            wdList.append(tok.surface)
                        # 漢字じゃない場合は2文字以上で採用
                        elif not re_kanji.fullmatch(tok.surface) and len(tok.surface) > 1:
                            wdList.append(tok.surface)
    return wdList


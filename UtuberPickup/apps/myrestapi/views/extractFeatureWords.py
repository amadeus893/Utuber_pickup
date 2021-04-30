import math

# 抽出単語数
N = 5

# IDF計算処理
def calcIDF (docList, wd):
    # 単語を含む文章数を算出
    nqi = [wd for doc in docList if wd in doc].count(wd)
    return math.log((len(docList) - nqi + 0.5) / nqi + 0.5)

# 重要単語抽出処理
def extractFeatureWords(docList, wdList):
    # 計算に必要なパラメータなどを初期化
    k1 = 1.2  # param(k)
    b = 0.75  # param(b)
    D = 0  # 全文章の総単語数
    sumApperCnt = 0  # 合計出現回数
    wdDict = {}  # 単語辞書 = 単語 : {出現回数: X, 重みスコア: X}

    # 単語ごとの出現回数と合計出現回数を求める
    for wd in wdList:
        cnt = 0
        wdDict[wd] = {"fcnt": 0, "score": 0}
        # 全文章における単語の出現回数を保持
        for doc in docList:
            cnt = cnt + doc.count(wd)
        wdDict[wd]["fcnt"] = cnt
        # 全単語の出現回数の合計を保持
        sumApperCnt = sumApperCnt + cnt

    # 全文章の総単語数
    D = 0
    for doc in docList:
        D = D + len(doc)

    # 全文章の平均単語数
    avgdl = sumApperCnt / D

    # 単語の重み付け
    # Method by Okapi BM25
    for wd in wdList:
        # TF計算
        TF = wdDict[wd]["fcnt"] / sumApperCnt
        # IDF計算
        IDF = calcIDF(docList, wd)
        # 重み付け単語辞書に追加
        wdDict[wd]["score"] = IDF * (TF * (k1 + 1)) / (TF + (k1 * (1 - b + (b * (D / avgdl)))))

    # 重み順にソートして上記N個を返却
    words = sorted(wdDict.items(), key=lambda x: eval(str(x[1]))["score"], reverse=True)[:N]

    # タグのみ抽出して返却
    tags = []
    for wd in words:
        tags.append(wd[0])

    return tags

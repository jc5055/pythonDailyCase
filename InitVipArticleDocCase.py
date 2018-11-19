#!/usr/bin/python
#hzjiangcong5055
import requests
import  json
import csv
from collections import namedtuple
import  time

def readCsv2BookSourceUuidList(file):
    sourceUuidList = []
    with open(file, 'r') as f:
        f_csv= csv.reader(f)
        headings = next(f_csv)
        Row = namedtuple('Row', headings)
        for row in f_csv:
            r = Row(*row)
            print(r.sourceUuid)
            sourceUuidList.append(r.sourceUuid)
    return sourceUuidList


def writeCsv2BookUnitList(filePath, bookUnitList, headers):
    rows = []
    for temp in bookUnitList:
        row = {'sourceUuid': temp.sourceUuid, 'vipArticleUuid': temp.vipArticleUuid, 'vipArticleTitle': temp.vipArticleTitle}
        rows.append(row)

    with open(filePath, 'w') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()
        f_csv.writerows(rows)



class BookUnit:
    def __init__(self, sourceUuid, vipArticleUuid,vipArticleTitle):
        self.sourceUuid = sourceUuid
        self.vipArticleUuid = vipArticleUuid
        self.vipArticleTitle = vipArticleTitle


def getArticleUuidfromNet(bookSourceUuid, i):
    url = "https://xkcszh.kuxuanbook.com/book/catalog.json"
    palload = {"sourceUuid": bookSourceUuid,
               "pageNow": "1", "reverse": "false", "pageSize": "100"}
    headers = {
        "Cookie": "_lc_online=cc9e85-316d576cab1b4cddada13f22b0f4f936-7b3aa099-0; N_userAccess=true; XSRF-TOKEN=a7e37fb8-ead3-4774-bbcb-cb0bb2480eea",
        "XSRF-TOKEN": "a7e37fb8-ead3-4774-bbcb-cb0bb2480eea"}
    try:
        r = requests.get(url, headers=headers, params=palload)

    except requests.exceptions.ConnectTimeout:
        NETWORK_STATUS = False
        return  ['请求超时异常','请求超时异常']


    a = r.text
    rsJson = json.loads(r.text)
    code = rsJson.get('code')
    msg = rsJson.get('msg')
    if code == 0:
        categorys = rsJson.get('categorys')
        data = categorys.get('data')

        for temp in data:
            needPay = temp.get("needPay")
            if needPay == True:
                # sourceUuid = temp.get('sourceUuid')
                vipArticleUuid = temp.get('articleUuid')
                title = temp.get('title')
                return [vipArticleUuid,title]
        else:
            return  ['-2','no vip article']
    else:
        return [code, msg]

def main():
    filePathOringial = "bookOriginal.csv"
    timeTemp = time.strftime("%Y%m%d", time.localtime())
    filePathRs = 'bookOriginalRs' + timeTemp + '.csv'
    bookUnitList = []

    bookSourceUuid = readCsv2BookSourceUuidList(filePathOringial)

    i = 1
    for sourceUuidTemp in bookSourceUuid:
        print(i)
        i = i + 1
        try:
            vipArtileInfo = getArticleUuidfromNet(sourceUuidTemp, i)
            vipArticleSourceUuid = vipArtileInfo[0]
            vipArticleTitle = vipArtileInfo[1]
            bookUnitTemp = BookUnit(sourceUuidTemp, vipArticleSourceUuid, vipArticleTitle)
            bookUnitList.append(bookUnitTemp)

        except :
            print(sourceUuidTemp)
            bookUnitTemp = BookUnit(sourceUuidTemp, '-1', 'request error')
            bookUnitList.append(bookUnitTemp)


    headers = ['sourceUuid', 'vipArticleUuid', 'vipArticleTitle']
    writeCsv2BookUnitList(filePathRs, bookUnitList, headers)

    return


if __name__ == '__main__':
    main()
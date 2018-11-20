#!/usr/bin/python
#hzjiangcong5055
import requests
import  json
import csv
from collections import namedtuple
import time
import codecs
import  datetime

def readBookUnitFromCSV(filePath):
    bookUnitList = []
    with codecs.open(filePath, 'r', 'utf_8_sig') as f:
        f_csv = csv.reader(f)
        headings = next(f_csv)
        Row = namedtuple('Row', headings)
        for row in f_csv:
            r = Row(*row)
            sourceUuid = r.sourceUuid
            vipArticleUuid = r.vipArticleUuid
            vipArticleTitle = r.vipArticleTitle
            bookUnitTemp = BookUnit(sourceUuid, vipArticleUuid, vipArticleTitle)
            bookUnitList.append(bookUnitTemp)
    return bookUnitList



def writeBookUnitToCSV(filePath, bookUnitList):
    headers = ['sourceUuid', 'vipArticleUuid', 'vipArticleTitle']
    rows = []
    for temp in bookUnitList:
        rowTemp = {
            'sourceUuid':temp.sourceUuid,
            'vipArticleUuid':temp.vipArticleUuid,
            'vipArticleTitle':temp.vipArticleTitle,
        }
        rows.append(rowTemp)
    with codecs.open(filePath, 'w', 'utf_8_sig') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()
        f_csv.writerows(rows)


def writeBookUnitDifToCSV(filePath, bookUnitCompareList):
    headers = ['sourceUuid', 'vipArticleUuidYesterday', 'vipArticleTitleYesterday','vipArticleUuidToday', 'vipArticleTitleToday']
    rows = []
    for temp in bookUnitCompareList:
        rowTemp = {
            'sourceUuid':temp.sourceUuid,
            'vipArticleUuidYesterday':temp.vipArticleUuidYesterday,
            'vipArticleTitleYesterday':temp.vipArticleTitleYesterday,
            'vipArticleUuidToday':temp.vipArticleUuidToday,
            'vipArticleTitleToday':temp.vipArticleTitleToday
        }
        rows.append(rowTemp)
    with codecs.open(filePath, 'w', 'utf_8_sig') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()
        f_csv.writerows(rows)


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
        return  ['-3','time out']


    a = r.text
    try:
        rsJson = json.loads(r.text)
    except :
        return ['-1','response error']

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



class BookUnit:
    def __init__(self, sourceUuid, vipArticleUuid,vipArticleTitle):
        self.sourceUuid = sourceUuid
        self.vipArticleUuid = vipArticleUuid
        self.vipArticleTitle = vipArticleTitle

class BookUnitCompare:
    def __init__(self, sourceUuid, vipArticleUuidYesterday,vipArticleTitleYesterday, vipArticleUuidToday, vipArticleTitleToday):
        self.sourceUuid = sourceUuid
        self.vipArticleUuidYesterday = vipArticleUuidYesterday
        self.vipArticleTitleYesterday = vipArticleTitleYesterday
        self.vipArticleUuidToday = vipArticleUuidToday
        self.vipArticleTitleToday = vipArticleTitleToday

def strIsNegative(str):
    try:
        str = int(str)
        return isinstance(str, int)
    except ValueError:
        return False

def compareBookData(bookUnitList1, bookUnitList2):
    difBookUnitList = []

    i = 1

    for i in range(0, bookUnitList1.__len__()):
        vipArticleUuid1 = bookUnitList1[i].vipArticleUuid
        vipArticleUuid2 = bookUnitList2[i].vipArticleUuid

        if strIsNegative(vipArticleUuid1) or strIsNegative(vipArticleUuid2) or vipArticleUuid1 != vipArticleUuid2:
            difBookUnit = BookUnitCompare(bookUnitList1[i].sourceUuid, vipArticleUuid1, bookUnitList1[i].vipArticleTitle,
                                          vipArticleUuid2, bookUnitList2[i].vipArticleTitle)
            difBookUnitList.append(difBookUnit)


    # for bookUnit1, bookUnit2 in bookUnitList1, bookUnitList2:
    #     vipArticleUuid1 = bookUnit1.vipArticleUuid
    #     vipArticleUuid2 = bookUnit2.vipArticleUuid
    #
    #
    #     if strIsNegative(vipArticleUuid1) or strIsNegative(vipArticleUuid2) or vipArticleUuid1 != vipArticleUuid2 :
    #         difBookUnit = BookUnitCompare(bookUnit1.sourceUuid, vipArticleUuid1,bookUnit1.vipArticleTitle,
    #                                   vipArticleUuid2, bookUnit2.vipArticleTitle)
    #         difBookUnitList.append(difBookUnit)

    return  difBookUnitList

def main():
    today = datetime.date.today()
    todayStr = today.strftime('%Y%m%d')

    yesterday = today - datetime.timedelta(days=1)
    yesterdayStr = yesterday.strftime('%Y%m%d')

    filePath = 'bookData' + yesterdayStr + '.csv'
    dataTodayFilePath = "bookData" + todayStr + ".csv"
    bookVipDifFilePath = "bookVipDif.csv"

    bookUnitListYesterday = readBookUnitFromCSV(filePath)

    difBookUnitList = []
    bookUnitListToday = []
    i = 1

    for bookTemp in bookUnitListYesterday:
        sourceUuidTemp = bookTemp.sourceUuid
        print(i)
        i = i + 1
        try:
            vipArtileInfo = getArticleUuidfromNet(sourceUuidTemp, i)
            vipArticleSourceUuid = vipArtileInfo[0]
            vipArticleTitle = vipArtileInfo[1]
            bookUnitTemp = BookUnit(sourceUuidTemp, vipArticleSourceUuid, vipArticleTitle)
            bookUnitListToday.append(bookUnitTemp)

        except:
            print(sourceUuidTemp)
            bookUnitTemp = BookUnit(sourceUuidTemp, '-1', 'request error')
            bookUnitListToday.append(bookUnitTemp)

    writeBookUnitToCSV(dataTodayFilePath, bookUnitListToday)

    difBookUnitList = compareBookData(bookUnitListYesterday, bookUnitListToday)

    writeBookUnitDifToCSV(bookVipDifFilePath, difBookUnitList)

if __name__ == '__main__':
    main()
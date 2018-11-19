#!/usr/bin/python
#hzjiangcong5055
import requests
import  json
import csv
from collections import namedtuple
import time
import codecs

def readBookUnitFromCSV(filePath):
    bookUnitList = []
    with open(filePath, 'r') as f:
        f_csv = csv.reader(f)
        headings = next(f_csv)
        Row = namedtuple('Row', headings)
        for row in f_csv:
            r = Row(*row)
            sourceUuid = r.sourceUuid
            vipArticleUuidFromCSV = r.vipArticleUuid
            vipArticleTitleFromCSV = r.vipArticleTitle
            bookUnitTemp = BookUnit(sourceUuid, vipArticleUuidFromCSV, vipArticleTitleFromCSV)
            bookUnitList.append(bookUnitTemp)
    return bookUnitList


def writeBookUnitToCSV(filePath, bookUnitList):
    headers = ['sourceUuid', 'vipArticleUuidFromCSV', 'vipArticleTitleFromCSV','vipArticleUuidNet', 'vipArticleTitleNet']
    rows = []
    for temp in bookUnitList:
        rowTemp = {
            'sourceUuid':temp.sourceUuid,
            'vipArticleUuidFromCSV':temp.vipArticleUuidFromCSV,
            'vipArticleTitleFromCSV':temp.vipArticleTitleFromCSV,
            'vipArticleUuidNet':temp.vipArticleUuidNet,
            'vipArticleTitleNet':temp.vipArticleTitleNet
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


def filterAbnormalBookUnit(bookUnitList):
    return


class BookUnit:
    def __init__(self, sourceUuid, vipArticleUuidFromCSV,vipArticleTitleFromCSV):
        self.sourceUuid = sourceUuid
        self.vipArticleUuidFromCSV = vipArticleUuidFromCSV
        self.vipArticleTitleFromCSV = vipArticleTitleFromCSV
        self.vipArticleUuidNet = ""
        self.vipArticleTitleNet = ""

def strIsNegative(str):
    try:
        str = int(str)
        return isinstance(str, int)
    except ValueError:
        return False

def main():
    timeTemp = time.strftime("%Y%m%d", time.localtime())
    filePath = 'bookOriginalRs' + timeTemp + '.csv'

    bookVipDifFilePath = "bookVipDif" + timeTemp + ".csv"
    bookUnitList = readBookUnitFromCSV(filePath)

    difBookUnitList = []
    i = 1
    for bookTemp in bookUnitList:
        print(i)
        sourceUuid = bookTemp.sourceUuid
        articleVipUuid = bookTemp.vipArticleUuidFromCSV
        flag = strIsNegative(articleVipUuid)
        if flag:
            print(sourceUuid)
            difBookUnit = BookUnit(sourceUuid, bookTemp.vipArticleUuidFromCSV, bookTemp.vipArticleTitleFromCSV)
            difBookUnit.vipArticleUuidNet = bookTemp.vipArticleUuidFromCSV
            difBookUnit.vipArticleTitleNet = bookTemp.vipArticleTitleFromCSV
            difBookUnitList.append(difBookUnit)
        else:
            rs = getArticleUuidfromNet(sourceUuid, i)
            if rs[0] != bookTemp.vipArticleUuidFromCSV:
                difBookUnit = BookUnit(sourceUuid, bookTemp.vipArticleUuidFromCSV, bookTemp.vipArticleTitleFromCSV)
                difBookUnit.vipArticleUuidNet = rs[0]
                difBookUnit.vipArticleTitleNet = rs[1]
                difBookUnitList.append(difBookUnit)


        i = i + 1

    writeBookUnitToCSV(bookVipDifFilePath, difBookUnitList)


if __name__ == '__main__':
    main()
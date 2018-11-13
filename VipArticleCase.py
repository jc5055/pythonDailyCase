#!/usr/bin/python

import requests
import  json
import csv
from collections import namedtuple





def main():
    bookUnitsOriginal = readCSV('data.csv')
    bookUnitsResult = []

    for book in bookUnitsOriginal:
        vipArticle = getVipBookArticle(book.sourceUuid)
        book.vipArticleUuidfromNet = vipArticle
        if vipArticle != book.vipArticleUuidfromCSV:
            book.flag = False
            bookUnitsResult.append(book)
    print(bookUnitsResult[0].flag)
    writeCSV('dataRs.csv', bookUnitsResult)





class bookUnit:
    def __init__(self, sourceUuid, vipArticleUuid):
        self.sourceUuid = sourceUuid
        self.vipArticleUuidfromCSV = vipArticleUuid #vip 章节文档读取
        self.vipArticleUuidfromNet = "" #vip 章节网络获取
        self.flag = True #vip 章节是否相同的标识为，true相同，false不同


def writeCSV(filename, bookUnitsResult):
    headers = ['sourceUuid','vipArticleUuidfromCSV','vipArticleUuidfromNet']
    rows = []
    for temp in bookUnitsResult:
        rowTemp = {'sourceUuid':temp.sourceUuid,'vipArticleUuidfromCSV':temp.vipArticleUuidfromCSV, 'vipArticleUuidfromNet':temp.vipArticleUuidfromNet}
        rows.append(rowTemp)
    with open(filename, 'w') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()
        f_csv.writerows(rows)

def getVipBookArticle(souceUuid):
    url = "https://pre.kuxuanbook.com/book/catalog.json"
    palload = {"sourceUuid": "np_c3sEL8RBi3Gu_jgpLD9-yUiMcvj5MnAuPiyZRt9_ra06IS4EKQ",
               "pageNow": "1", "reverse": "false", "pageSize": "100"}
    headers = {
        "Cookie": "_u_vid_pre=1541993418345187; _lc_pre=245852-2e078af870154e08b9b7511057931c14-7b3aa099-0; N_userAccess=true; XSRF-TOKEN=e61da93b-4444-4d65-b303-df9d2d397c94; _u_vid_online=1538238438122191",
        "XSRF-TOKEN": "e61da93b-4444-4d65-b303-df9d2d397c94"}

    r = requests.get(url, headers=headers, params=palload)

    rsJson = json.loads(r.text)
    categorys = rsJson.get('categorys')
    data = categorys.get('data')

    for temp in data:
        needPay = temp.get("needPay")
        if needPay == True:
            sourceUuid = temp.get('sourceUuid')
            vipArticleUuid = temp.get('articleUuid')
            title = temp.get('title')
            return  vipArticleUuid


def readCSV(file):
    bookUnits = []
    with open(file, 'r') as f:
        f_csv = csv.reader(f)
        headings = next(f_csv)
        Row = namedtuple('Row', headings)
        for row in f_csv:
            r = Row(*row)
            print(r.sourceUuid)
            bookUnitTemp = bookUnit(r.sourceUuid, r.vipArticleSourceUuid)
            bookUnits.append(bookUnitTemp)
    return  bookUnits


if __name__ == '__main__':
    main()
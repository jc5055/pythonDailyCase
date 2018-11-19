import asyncio
import concurrent.futures
import requests
import json
import csv
from collections import namedtuple

def getVipBookArticle(bookUnitOriginal):
    url = "https://xkcszh.kuxuanbook.com/book/catalog.json"
    palload = {"sourceUuid": bookUnitOriginal.sourceUuid,
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
            # print()
            sourceUuid = temp.get('sourceUuid')
            vipArticleUuid = temp.get('articleUuid')
            title = temp.get('title')
            bookUnitRs = bookUnit(sourceUuid,vipArticleUuid)
            bookUnitRs.vipArticleUuidfromNet = vipArticleUuid
            bookUnitRs.vipArticleTitlefromCSV = title
            return bookUnitRs


class bookUnit:
    def __init__(self, sourceUuid, vipArticleUuid):
        self.sourceUuid = sourceUuid
        self.vipArticleUuidfromCSV = vipArticleUuid #vip 章节文档读取
        self.vipArticleUuidfromNet = "" #vip 章节网络获取
        self.vipArticleTitlefromCSV = ""
        self.flag = True #vip 章节是否相同的标识为，true相同，false不同


def readBookSourceUuidfromCSV(filename):
    bookUnits = []
    with open(filename, 'r') as f:
        f_csv = csv.reader(f)
        headings = next(f_csv)
        Row = namedtuple('Row', headings)
        for row in f_csv:
            r = Row(*row)
            bookUnitsTemp = bookUnit(r.sourceUuid, '11')
            # print(r.sourceUuid,r.name)
            bookUnits.append(bookUnitsTemp)
    return bookUnits






async def main():

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        bookUnitList = readBookSourceUuidfromCSV('bookOriginal.csv')
        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(
                executor,
                getVipBookArticle,
                bookUnitList[i]
            )
            for i in range(bookUnitList.__len__())
        ]

        for response in await asyncio.gather(*futures):
            print(response.vipArticleUuidfromNet + ':vipArticle:' + response.vipArticleTitlefromCSV)
            pass




# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
# 'bookOriginal.csv'
if __name__ == '__main__':
    # bookUnitList = readBookSourceUuidfromCSV('bookOriginal.csv')
    # a = bookUnitList.__len__()
    # print(a)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    # a = getVipBookArticle('ts_1a03b127ab254ba7bcfde0ef27049856_4')
    # print(a)

import asyncio
import concurrent.futures
import requests
import json

def getVipBookArticle(souceUuid1):
    url = "https://pre.kuxuanbook.com/book/catalog.json"
    palload = {"sourceUuid": souceUuid1,
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
            print(sourceUuid)
            vipArticleUuid = temp.get('articleUuid')
            title = temp.get('title')
            return  vipArticleUuid



async def main():

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        par = ['ts_81a508b00c174f17b1faa154ee75fb32_4','ts_86d50b99b5f6426ea2f3b653c06c07b8_4']
        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(
                executor,
                getVipBookArticle,
                par[i]
            )
            for i in range(2)
        ]
        for response in await asyncio.gather(*futures):
            pass


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
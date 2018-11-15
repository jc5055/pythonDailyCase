#!/usr/bin/python
import time,asyncio,aiohttp,requests


def urlRequest():
    url = "https://pre.kuxuanbook.com/book/catalog.json"
    palload = {"sourceUuid": "np_c3sEL8RBi3Gu_jgpLD9-yUiMcvj5MnAuPiyZRt9_ra06IS4EKQ",
               "pageNow": "1", "reverse": "false", "pageSize": "100"}
    headers = {
        "Cookie": "_u_vid_pre=1541993418345187; _lc_pre=245852-2e078af870154e08b9b7511057931c14-7b3aa099-0; N_userAccess=true; XSRF-TOKEN=e61da93b-4444-4d65-b303-df9d2d397c94; _u_vid_online=1538238438122191",
        "XSRF-TOKEN": "e61da93b-4444-4d65-b303-df9d2d397c94"}

    return requests.get(url, headers=headers, params=palload)

async def main():
    loop = asyncio.get_event_loop()
    for _  in range(10):
        temp = loop.run
        print()


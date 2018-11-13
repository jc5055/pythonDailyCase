import requests
import  json
import csv
from collections import namedtuple


with open('data.csv', 'r') as f:
    f_csv = csv.reader(f)
    headings = next(f_csv)
    Row = namedtuple('Row', headings)
    for row in f_csv:
        r = Row(*row)
        print(r.sourceUuid)
        sourceUuid = r.sourceUuid
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
                articleUuid = temp.get('articleUuid')
                title = temp.get('title')
                print(sourceUuid)
                print(title)
                print(articleUuid)
                break
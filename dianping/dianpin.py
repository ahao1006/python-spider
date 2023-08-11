"""
    任务目标:
    从大众点评,获取面包甜点的数据,进行数据的整合,并将数据存入excel表格
    数据: 店铺名称、营业时间、地址、人均、口味、环境、服务
"""

from parsel import Selector
from time import sleep
import requests
import csv

fieldnames = ['店铺名称', '营业时间', '地址', '人均', '口味', '环境', '服务']

f = open('sweetmeat.csv',  mode = 'a', encoding='utf8', newline='')
writer = csv.DictWriter(f, fieldnames=fieldnames)

# 获取列表
page = 1
while True:
    url = "https://www.dianping.com/xiamen/ch10/g117"
    if not page == 1:
        url += "p" + str(page)

    headers = {
        'Cookie': 'm_flash2=1; WEBDFPID=w818xz3yw9005wxy083962x086w559z9810v735098197958508z029x-2007080387125-1691720387125YGEWEUC75613c134b6a252faa6802015be905511269; _lxsdk_cuid=183ede611adc8-0415502654cd35-1a525635-1fa400-183ede611aec8; _lxsdk=183ede611adc8-0415502654cd35-1a525635-1fa400-183ede611aec8; _hc.v=cd888007-272e-aae6-3e39-2dd05bc5acdd.1691720387; cityid=15; msource=default; default_ab=citylist%3AA%3A1%7CshopList%3AA%3A5; OUTFOX_SEARCH_USER_ID_NCOO=1436778585.3574781; dper=191db3a0372ee831d66210701824a98fa824045633724680fb20d5f89792658003795356cce990434161779feabfb9f3ccb41f5cdb29c48bd6c2fbe359fcdf0a; ll=7fd06e815b796be3df069dec7836c3df; pvhistory="6L+U5ZuePjo8L3N1Z2dlc3QvZ2V0SnNvbkRhdGE/Y2FsbGJhY2s9anNvbnBfMTY5MTcyMTg4OTYzNl83ODYyNz46PDE2OTE3MjE4OTE4ODddX1s="; fspop=test; cy=15; cye=xiamen; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1691721911; s_ViewType=10; _lxsdk_s=189e2648a85-a67-a2-d4%7C%7C1522; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1691722447',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Host': 'www.dianping.com'
    }

    response = requests.get(url = url, headers = headers)

    if not response.status_code == 200:
        print("采集结束, 第" + i + "页")
        break

    selector = Selector(response.text)
    hrefs = selector.css('.pic a::attr(href)').getall()
    if not len(hrefs):
        print("采集结束, 第" + i + "页")
        break

    for href in hrefs:
        # 获取详情
        detail_response = requests.get(url = href, headers = headers)
        if not detail_response.status_code == 200:
            continue

        detail_select = Selector(detail_response.text)
        comment_score = detail_select.css('#comment_score .item::text').getall()

        bool = True if len(comment_score) == 3 else False

        # 创建字典
        dist = {
            '店铺名称': detail_select.css('.shop-name::text').get(),
            '营业时间': detail_select.css('.info-indent .item::text').get(),
            '地址': detail_select.css('#address::text').get(),
            '人均': detail_select.css('#avgPriceTitle::text').get(),
            '口味': comment_score[0] if bool else 0,
            '环境': comment_score[1] if bool else 0,
            '服务': comment_score[2] if bool else 0
        }

        writer.writerow(dist)
        sleep(20)
    
    sleep(60)

    page += 1

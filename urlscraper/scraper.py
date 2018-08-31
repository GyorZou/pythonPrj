import requests
from bs4 import BeautifulSoup
from urllib import parse, request
from news import News
from company import Company
import csv
import ssl
import time
from datetime import datetime
import re

news_url = "https://www.futunn.com/quote/stock-news?m=hk&code="
count_suc = 0
count_fail = 0


def scrap_html(url):
    # print("scraping url:", url)
    context = ssl._create_unverified_context()
    resp = request.urlopen(url, context=context)

    html = resp.read().decode(encoding="utf-8")
    return html


def scrap_news_html(num):
    num = "%s" % num
    num = num.zfill(5)
    url = news_url + num
    html = scrap_html(url)
    response_soup = BeautifulSoup(html, 'html.parser')
    list_node = response_soup.find('div', class_='ulList02')
    return list_node


def scrap_news_company(comp):
    num = comp.stock
    global count_fail, count_suc
    url = news_url + str(num).zfill(5)
    html = scrap_html(url)
    response_soup = BeautifulSoup(html, 'html.parser')
    list_node = response_soup.find('div', class_='ulList02')
    stamp_now = datetime.now().timestamp()

    if list_node:
        # print("get stock:", num)

        h1 = response_soup.find("h1", class_="tf")
        if h1:
            comp.name = h1.get("title")

        up = response_soup.find("div", class_="div002 up")
        if not up:
            up = response_soup.find("div", class_="div002 down")
        if up:
            spans = up.find_all("span")
            if spans:
                lens = len(spans)
                value =   spans[lens-1].text
                comp.up =value

        list = list_node.find_all("li")

        count_suc += 1
        count_hot = 0
        hot_news = []
        comp.ishot = len(list) > 3

        for li in list:
            if not li.find("a"):
                continue
            if not li.find("div", class_="bar01"):
                continue

            txt = li.find("a").text;
            link = li.find("a").get("href")
            date = li.find("div", class_="bar01").text

            date = date.split("：").pop()

            cdate = datetime.strptime(date, "%Y-%m-%d %H:%M")

            # print("== %s=== %s=====+++" % (txt, cdate))
            stamp_new = cdate.timestamp()

            if stamp_now - stamp_new < 24 * 60 * 60 * 2:
                n = News(txt, date, link)
                hot_news.append(n)

        # print("finished get stock: %s ;hot new:%d" % (num, len(hot_news)))
        return hot_news

    else:
        print("error happend", num)
        count_fail = count_fail + 1


def scrap_news(num):
    com = Company(num)
    return scrap_news_company(com)


def analysis_news(lis):
    # 消息数量
    #
    #
    #
    if not lis:
        return 0
    count = len(lis)
    result = 1
    must_words = ["修订稿", "上市", "借壳"]
    positive_words = ["收购", "提振", "盈利", "增"]
    negative_words = ["减持", "停牌", "负面", "下滑", "亏"]

    total = positive_words + negative_words
    reg = ""
    c = len(total)
    index = 0
    for w in total:
        reg += w
        index += 1
        if index != c:
            reg += "|"
    reg = r"\w*(%s\w*)" % reg
    reg = re.compile(reg)

    reg2 = ""
    c = len(must_words)
    index = 0
    for w in must_words:
        reg2 += w
        index += 1
        if index != c:
            reg2 += "|"
    reg2 = r"\w*(%s\w*)" % reg2
    reg2 = re.compile(reg2)

    for new in lis:
        # 判断是否包含must字词，每个50分
        title = new.title
        if reg.match(title):
            result += 10
        title = new.title

        if reg2.match(title):
            result += 50

        # 判断是否包含关键字词，每个10分

    return result * count


def save_result(num, result):
    pass


def compare(comp):
    return comp.rate


if __name__ == "__main__":
    time_start = time.time()
    header_dict = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15"}  # {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}

    ran = range(200)

    result_list = []
    for i in ran:
        num = ("%s" % (i)).zfill(5)
        news = scrap_news(num)
        if not news:
            continue
        result = analysis_news(news)

        comp = Company(num)
        comp.rate = result
        comp.news = news

        result_list.append(comp)

        print("finished anaylisysi %s,%s" % (num, result))

    result_list.sort(key=compare, reverse=True)

    time_end = time.time()

    print("finished suc:%s fail:%s by using time:%s" % (count_suc, count_fail, time_end - time_start))

    print("=" * 20)
    top10 = result_list[:10]
    for com in top10:
        print(com)
    print("=" * 20)

# writer = csv.writer(csvFile)
# for li in list:
#
#     print("=" * 60)
#     sku = li.get("data-sku")
#     if not sku:
#         print("--------cant get sku-------\n", li)
#         continue
#     row = []
#     key = "J_AD_" + sku
#     name = li.find("i", id=key).text
#     row.append(name)
#
#     print("===%s==name:%s" % (key, name))
#     row.append("123.99")
#     writer.writerow(row);
#
# csvFile.close()

# req = request.Request(url=url, headers=header_dict)
# resp = request.urlopen(req)
# resp = resp.read()
#
# print(resp)
# resp = requests.get(url)
#
#

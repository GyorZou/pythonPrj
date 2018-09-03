from stock_scraper import scrape_urls
from bs4 import BeautifulSoup
import stocks_lister
from  company import  Company
from datetime import  datetime
from news import  News
import timecounter
import stocks_lister
import  stock_compare
import stock_analysis

def anylisor(resp):
    timecounter.updateprogress()
    if  not resp:
        return
    response_soup = BeautifulSoup(resp, 'html.parser')
    list_node = response_soup.find('div', class_='ulList02')
    if list_node:
        stamp_now = datetime.now().timestamp()
        comp = Company(stock="")
        h1 = response_soup.find("h1", class_="tf")
        if h1:
            comp.name = h1.get("title")
            compnents = h1.text.split(".")
            if len(compnents) >0:
                stock_num = compnents[0]
                comp.stock = stock_num
        else:
            return None

        up = response_soup.find("div", class_="div002 up")
        if not up:
            up = response_soup.find("div", class_="div002 down")
        if up:
            spans = up.find_all("span")
            if spans:
                lens = len(spans)
                value = spans[lens - 1].text
                comp.up = value

        list = list_node.find_all("li")

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

            stamp_new = cdate.timestamp()

            if stamp_now - stamp_new < 24 * 60 * 60 * 2:
                n = News(txt, date, link)
                hot_news.append(n)
        comp.news = hot_news
        return comp



def printlist(lis):
    for obj in lis:
        print(obj)
if __name__ =="__main__":
    timecounter.begin()
    host = "http://www.futunn.com/quote/stock-news?m=hk&code="

    nums = stocks_lister.read_all("hotstocks.csv")
    urls_todo = [ host+ str(x).zfill(5) for  x in nums]
   # urls_todo = list(map(lambda x: host+ str(x).zfill(5), range(1, 10)))
    holder = []
    timecounter.total = len(urls_todo)
    scrape_urls(urls_todo,holder=holder,analyse_func=anylisor)

    #stocks_lister.write_2_csv("hotstocks.csv",holder)
    print("finished with count:",len(holder))



    for cp in holder:
        cp.rate = stock_analysis.analysis_news(cp.news)




    holder.sort(key=stock_compare.compare_rate,reverse=True)
    top = holder[:30]
    print("*"*30)
    printlist(top)

    holder.sort(key=stock_compare.compare_price, reverse=True)
    top2= holder[:30]
    print("*" * 30)
    printlist(top2)

    inter = set(top).intersection(set(top2))

    print("*" * 30)
    printlist(inter)





    # for comp in holder:
    #     print(comp)

    timecounter.end()
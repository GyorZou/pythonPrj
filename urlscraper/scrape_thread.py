import threading
import scraper
import stocks_lister
from company import Company
from news import News
import timecounter
class ScrapeThread(threading.Thread):


    def __init__(self,stock_range,callback=None):

        super().__init__()
        self.stock = stock_range
        self.callback = callback
        self.result_list = []

    def run(self):

        for num in self.stock:
            comp = Company(num)
            news = scraper.scrap_news_company(comp)
            comp.news = news
            comp.rate = scraper.analysis_news(news)
            self.result_list.append(comp)
            timecounter.updateprogress()
        #完成线程，回调
        if self.callback:

            self.callback(self.result_list)

class Company(object):

    def url(self):
        return "https://www.futunn.com/quote/stock-news?m=hk&code="+ str(self.stock).zfill(5)
    def __init__(self,stock):
        if type(stock) == Company:
            self.stock = stock.stock
        else:
            self.stock = stock
        self.rate = 0  # -5 ~ 5
        self.name = "unknow"
        self.news = []
        self.ishot = True
        self.up = "0"

    def __str__(self):
        return "company:%s url:%s rate:%d  up:%s"%(self.name,self.url(),self.rate,self.up)

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return self.stock == other.stock
    def __hash__(self):
        return hash(self.stock)
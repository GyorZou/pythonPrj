class News(object):
    def __init__(self,title,date,link):
        self.title = title
        self.date =date
        self.link = link

    def __str__(self):
        return "news:title = %s,href=%s,date = %s"%(self.title,self.link,self.date)
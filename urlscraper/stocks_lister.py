import csv
from scraper import scrap_news_html
import threading
import  timecounter
from  company import Company
file_name = "stocks.csv"
rs = {}

lock = threading.Lock()
def fetch_range(rang):
    global rs
    ls = []
    for i in rang:
        li = scrap_news_html(i)
        if li:  # 存在保存这个num
            ls.append(i)
    lock.acquire()
    rs[str(rang.start)] = ls
    lock.release()

def write_2_csv(filename,complist):
    with open(filename, 'w', newline='', encoding='gb18030') as csvfile:
        print("writing:",len(complist))
        writer = csv.writer(csvfile)
        for comp in complist:
            writer.writerow([str(comp.stock),comp.name])
        csvfile.close()

def refresh():
    with open(file_name, 'w', newline='', encoding='gb18030') as csvfile:
        # 开始抓取
        k = 10000
        threads = []
        timecounter.begin()
        for j in range(9):
            ran = range(j*k,(j+1)*k,1)
            t = threading.Thread(target=fetch_range,args=(ran,))
            t.setDaemon(True)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()



        keys = rs.keys()
        writer = csv.writer(csvfile)
        for key,values in rs.items():
            for value in values:
                writer.writerow([str(value)])
        csvfile.close()
        usetime = timecounter.end()
        print("all finished:%s s"%usetime)


def read_companys(filename=file_name):
    with open(filename, 'r',encoding='gb18030') as csvfile:
        reader = csv.reader(csvfile)
        list = []
        for row in reader:
            stock = row[0]
            name = row[1]
            comp = Company(stock)
            comp.name = name
            list.append(comp) #第一个元素
        return list

def read_all(filename=file_name):
    with open(filename, 'r',encoding='gb18030') as csvfile:
        reader = csv.reader(csvfile)
        list = []
        for row in reader:
            list.append(row[0]) #第一个元素

        return list




if __name__ == "__main__":
    #refresh()
    read_all()
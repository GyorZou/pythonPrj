import stocks_lister
import scraper
import scrape_thread
import threading
import timecounter


num_per_thread = 2000


results = []
lock = threading.Lock()

def scrape_thread_callback(list):#cmp list
    global results
    lock.acquire()
    results += list
    print("now length =",len(results))
    lock.release()


def scraper_socks(list):
    totalcount = len(list)
    num_thread = totalcount//num_per_thread
    num_thread = num_thread if num_thread >1 else 1
    true_num_per_thread = totalcount //num_thread
    left = totalcount%num_thread #余的个数，放到最后一个线程里去


    temp = 0
    start = 0
    end = 0

    threads = []
    while temp <num_thread :

        end +=true_num_per_thread

        if temp == 0 :
            end =true_num_per_thread + left


        childs= list[start:end]


        #启动线程开始抓
        t = scrape_thread.ScrapeThread(childs,scrape_thread_callback)

        threads.append(t)
        t.setDaemon(True)
        t.start()

        start = end
        temp += 1

    for t in threads:
        t.join()

    #完成了所有，开始暂时


    return  results


def price_compare(obj):
    return abs(float(obj.up.replace("%", "")))


#一个线程专跑已购

#一个线程专跑信息

if __name__ == "__main__":
    timecounter.begin()

    list = stocks_lister.read_companys("hotstocks.csv") #stocks_lister.read_all()
    list = list[:1000]
    timecounter.total = len(list)
    timecounter.updateprogress()

    rs =  scraper_socks(list)

    rs.sort(key =scraper.compare,reverse=True)

    filtered  = [obj for obj in rs if obj.ishot] #list(filter(lambda obj:obj.ishot,results))


    top20 = filtered[:30]  #results[:30]


    #涨跌幅排序

    #stocks_lister.write_2_csv("hotstocks.csv",filtered)

    for com in top20:
        print(com)


    filtered.sort(key=price_compare,reverse=True)
    top20_2 = filtered[:30]
    print("="*50)
    for com in top20_2:
        print(com)


    inter = set(top20_2).intersection(set(top20))
    print("=" * 50)
    for com in inter:
        print(com)

    timecounter.end()
import  time


total = 0
finished = 0

time_start =time_end = time.time()
def updateprogress():
    if total == 0:
        return
    global finished
    rate1 = int(finished*100 / total )
    finished +=1
    rate2 = int(finished*100 / total )
    if rate1 != rate2:
        print("progress updateing:%s%s" % (rate2, "%"))

def begin():
    global  time_start
    time_start = time.time()

def end():
    ti =  time.time() - time_start
    print("finished by using time",ti)
    return ti
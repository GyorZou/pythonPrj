def read():
   d = yield 22
   print("returning d")
   return d

def read2():
    d = yield from read()
    print("d == ",d)
    total = 0
    while total<20:
        d = yield  2
        total += d

    print("returing total",total)
    return total

e = read2()
e.send(None)

while True:
    try:
        result = e.send(1)
        print("ssss",result)
    except StopIteration:
        break



print("r=",result)

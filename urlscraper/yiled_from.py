def gen():

    while True:
        z2 = yield 2
        print("z==",z2)
    return  "i am done"


def gen2():
    g = gen()
    rsp = ""
    try:
        z = yield from g
        print("fz=",z)
        rsp += str(z)
    except StopIteration as e:
        pass

    return rsp


gg = gen2()

m = gg.send(None)
m = gg.send(2)
m = gg.send(3)
print(m)


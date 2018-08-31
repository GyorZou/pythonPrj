import socket,time
import asyncio
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE

selectors = DefaultSelector()
done = False

urls_todo = list(map(lambda x: r"/" + str(x), range(1, 10)))


class Future:
    def __init__(self):
        self.result = b""
        self.__callbacks = []

    def set_callback(self, fn):
        self.__callbacks.append(fn)

    def set_result(self, result):
        self.result = result
        for fn in self.__callbacks:
            fn(self)


class Task(Future):
    def __init__(self, coro):
        self.coro = coro
        f = Future()
        f.set_result(None)

        self.next_step(f)

    def next_step(self, future):
        try:
            new_future = self.coro.send(future.result)
        except StopIteration:
            return
        new_future.set_callback(self.next_step)


class WebFetcher:
    def __init__(self, url1):
        self.url = url1

    def fetch(self):
        sock = socket.socket()

        try:
            sock.setblocking(False)
            sock.connect(('example.com', 80))

        except BlockingIOError as e:
            print("blic err",e)
            pass

        f = Future()

        def on_connected():
            print("connected web xxx:", self.url)
            f.set_result(None)

        selectors.register(sock.fileno(), EVENT_WRITE, on_connected)
        r = yield f
        if not r:  # 这里r肯定为None
            pass
        selectors.unregister(sock.fileno())

        get = "GET {0} HTTP/1.0\r\n Host: example.com\r\n\r\n".format(self.url)
        sock.send(get.encode("utf-8"))

        while True:
            f = Future()

            def on_read():
                print("can read :", self.url)
                f.set_result(sock.recv(4096))

            selectors.register(sock.fileno(), EVENT_READ, on_read)
            r = yield f
            selectors.unregister(sock.fileno())
            if not r:
                break
            f.result += r

        # done remove url and
        urls_todo.remove(self.url)
        global done
        if len(urls_todo) == 0:
            done = True


def loop():
    while not done:
        events = selectors.select()
        for key, value in events:
            callback = key.data
            callback()


if __name__ == "__main__":
    t = time.time()
    for url in urls_todo:
        fetcher = WebFetcher(url)
        t = Task(fetcher.fetch())



    loop()
    print("use time:",time.time()-t)
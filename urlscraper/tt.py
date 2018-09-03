import  socket
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE


selector = DefaultSelector()
stopped = False
urls_todo = {'/', '/1', '/2', '/3', '/4'}


class Future:
    def __init__(self):
        self.result = None
        self.__callbacks = []

    def add_done_callback(self, fn):
        self.__callbacks.append(fn)

    def set_result(self, result):
        self.result = result
        for fn in self.__callbacks:
            fn(self)


class Crawler:
    def __init__(self, url):
        self.url = url
        self.response = b''

    @property
    def fetch(self):
        sock = socket.socket()
        sock.setblocking(False)
        try:
            sock.connect(('example.com', 80))
        except BlockingIOError:
            pass
        f = Future()

        def on_connected():
            f.set_result(None)

        selector.register(sock.fileno(), EVENT_WRITE, on_connected)
        yield f
        selector.unregister(sock.fileno())
        #https://www.futunn.com/quote/stock-news?m=hk&code=
        get = 'GET {0} HTTP/1.1\r\nHost: example.com\r\n\r\n'.format(self.url)
        get = 'GET /quote/stock-news?m=hk&code=00101 HTTP/1.0\r\nHost: futunn.com\r\n\r\n'
        sock.send(get.encode('ascii'))

        global stopped
        while True:
            f = Future()

            def on_readable():
                f.set_result(sock.recv(4096))

            selector.register(sock.fileno(), EVENT_READ, on_readable)
            chuck = yield f
            selector.unregister(sock.fileno())
            if chuck:
                self.response += chuck
            else:
                print("finished url:{0} with result:\n{1}".format(get, self.response.decode("utf-8")))
                urls_todo.remove(self.url)
                if not urls_todo:
                    stopped = True
                break



class Task:
    def __init__(self, coro):
        self.coro = coro
        f = Future()
        f.set_result(None)
        self.step(f)

    def step(self, future):
        try:
            next_future = self.coro.send(future.result)
        except StopIteration:
            return
        next_future.add_done_callback(self.step)


def loop():
    while not stopped:
        events = selector.select()
        for event_key, event_mask in events:
            callback = event_key.data
            callback()


if __name__ == '__main__':
    import time
    start = time.time()
    for url in urls_todo:
        c = Crawler(url)
        Task(c.fetch)
    loop()
    print("use time:", time.time() - start)
import socket
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE

selectors = DefaultSelector()
done = False

urls_todo = list(map(lambda x: str(x).zfill(5), range(1, 10)))
urls_todo = ["/","/","/"]
host="futunn.com"
host ="example.com"

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


class Task:
    def __init__(self, coro):
        self.coro = coro
        f = Future()
        f.set_result(None)

        self.next_step(f)

    def next_step(self, future):
        try:
            new_future = self.coro.send(future.result)
        except StopIteration:
            print("last time stopped")
            return
        new_future.set_callback(self.next_step)


class WebFetcher:
    def __init__(self, url1):
        self.url = url1
        self.response = b''

    def connect(self, address):
        _f = Future()
        _sock = socket.socket()
        _sock.setblocking(False)
        try:
            _sock.connect(address)
        except BlockingIOError as err:
            print("blocking err", err)
            pass

        def on_connected():
            _f.set_result(None)

        selectors.register(_sock.fileno(), EVENT_WRITE, on_connected)
        yield _f

        selectors.unregister(_sock.fileno())

        return _sock

    def read(self, sock):
        _f = Future()

        def on_readable():
            _f.set_result(sock.recv(4096))

        selectors.register(sock.fileno(), EVENT_READ, on_readable)
        chuck = yield _f
        selectors.unregister(sock.fileno())
        return chuck

    def read_all(self, sock):
        resp = []
        chunk = b''
        while True:
            chuck = yield from self.read(sock)
            if not chuck:
                break
            resp.append(chuck)
        return b''.join(resp)

    def fetch(self):
        sock = yield from self.connect((host, 80))

        url_todo = "/quote/stock-news?m=hk&code=" + self.url

        url_todo = self.url
        get = "GET {0} HTTP/1.1\r\n Host: {1}\r\n\r\n".format(url_todo,host)
        sock.send(get.encode("utf-8"))
        self.response = yield from self.read(sock)

        # done remove url and
        print("finished read {0} content:\n{1}".format(self.url, self.response.decode("utf-8")))
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
    for url in urls_todo:
        fetcher = WebFetcher(url)
        Task(fetcher.fetch())

    loop()

class Q:
    def __init__(self, size, lock):
        self.a = []
        self.lock = lock
        self.size = size
        self.length = 0
    def put(self, item):
        with self.lock:
            self.a.append(item)
            self.length += 1
    def get(self):
        with self.lock:
            a = self.a
            item = a[0]
            del a[0]
            self.length -= 1
            return item
    def empty(self):
        if self.length == 0:
            return True
        return False
    def full(self):
        if self.length == self.size:
            return True
        return False
    def __repr__(self):
        return "Q(%s)" % self.a
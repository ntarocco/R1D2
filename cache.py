class MemoryCache:

    def __init__(self):
        self.data = {}

    def __contains__(self, key):
        return key in self.data

    def get(self, key):
        return self.data[key] if key in self.data else None

    def set(self, key, value):
        self.data[key] = value

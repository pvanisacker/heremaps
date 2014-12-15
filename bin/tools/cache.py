import datetime

import os.path


try:
    import cPickle as pickle
except ImportError:
    import pickle


class FileCache(object):
    """
    A simple cache for storing all kinds of results.
    The cache can be persisted to disk and items expire after a certain time and only x cached entries are kept
    """

    def __init__(self, max_count=100000, expiry=31):
        self.max_count = max_count
        self.expiry = expiry
        self.objects = {}

    def read_cache_file(self, filename):
        if os.path.isfile(filename):
            self.read_cache_handler(open(filename, "rb"))

    def read_cache_handler(self, handler):
        self.objects = pickle.load(handler)

    def get(self, key):
        if key in self.objects:
            return self.objects[key]["data"]
        raise KeyError()

    def set(self, key, value):
        self.objects[key] = {"data": value, "created_time": self.get_today()}

    def write_cache_file(self, filename):
        self.write_cache_handler(open(filename, "wb"))

    def write_cache_handler(self, handler):
        self.clean_cache()
        pickle.dump(self.objects, handler)
        handler.close()

    def clean_old(self):
        # remove all the old items
        reduced_objects = {}
        time_expiry = (self.get_today() - datetime.timedelta(days=self.expiry))
        for k, v in self.objects.iteritems():
            if v["created_time"] > time_expiry:
                reduced_objects[k] = v
        self.objects = reduced_objects

    def clean_count(self):
        # make sure we only have the maximum amount of items
        count = 0
        reduced_objects = {}
        for k, v in self.objects.iteritems():
            if count < self.max_count:
                reduced_objects[k] = v
                count += 1
            else:
                break
        self.objects = reduced_objects

    def clean_cache(self):
        self.clean_old()
        self.clean_count()

    def get_today(self):
        return datetime.datetime.today().date()

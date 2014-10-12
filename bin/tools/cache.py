import os.path
import datetime
import logging
try:
    import cPickle as pickle
except ImportError:
    import pickle


class FileCache(object):
    """
    A simple file cache for storing reverse geocoding results.
    Items expire after a certain time and only x cached entries are kept
    """

    expiry = 31
    max_count = 100000
    cache_file = "cache"
    objects = {}

    def __init__(self, cache_file, max_count, expiry):
        self.cache_file = cache_file
        self.max_count = max_count
        self.expiry = expiry

    def read_cache(self):
        # Read cache file
        if os.path.isfile(self.cache_file):
            self.objects = pickle.load(open(self.cache_file, "rb"))


    def get(self, key):
        if key in self.objects:
            return self.objects[key]["data"]
        return None

    def set(self, key, value):
        self.objects[key] = {"data": value, "created_time": datetime.date.today()}

    def write_cache(self):
        # remove all the old items
        reduced_objects = {}
        time_expiry = (datetime.datetime.today() - datetime.timedelta(days=self.expiry)).date()
        for k, v in self.objects.iteritems():
            if v["created_time"] > time_expiry:
                reduced_objects[k] = v
        self.objects = reduced_objects

        # make sure we only have the maximum amount of items
        count = 0
        reduced_objects = {}
        for k,v in self.objects.iteritems():
            if count <= self.max_count:
                reduced_objects[k] = v
            else:
                break
        self.objects = reduced_objects

        # write the cache to file
        pickle.dump(self.objects, open(self.cache_file, "wb"))

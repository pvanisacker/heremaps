import datetime

import unittest
import mock
from tools.cache import FileCache


class CacheTest(unittest.TestCase):
    def test_cache_creation(self):
        cache = FileCache(1000, 1)
        self.assertEqual(cache.max_count, 1000, "Is max count the same")
        self.assertEqual(cache.expiry, 1, "Is expiry the same")
        self.assertEqual(len(cache.objects), 0)

    def test_set_key(self):
        cache = FileCache(1000, 1)
        cache.set("mykey", "myvalue")
        self.assertEquals(cache.objects["mykey"]["data"], "myvalue")

    def test_overwrite_key(self):
        cache = FileCache(1000, 1)
        cache.set("mykey", "myvalue")
        cache.set("mykey", "NewValue")
        self.assertEquals(cache.objects["mykey"]["data"], "NewValue")

    def test_empty_key(self):
        cache = FileCache(1000, 1)
        cache.set("mykey", "myvalue")
        cache.set("mykey", None)
        self.assertEquals(cache.objects["mykey"]["data"], None)

    def test_get_non_existent_key(self):
        cache = FileCache(1000, 1)
        with self.assertRaises(KeyError):
            cache.get("mykey")

    def test_get_existent_key(self):
        cache = FileCache(1000, 1)
        cache.set("mykey", "myvalue")
        self.assertEqual("myvalue", cache.get("mykey"))

    def test_clean_count_1(self):
        cache = FileCache(3, 1)
        cache.set("key1", "value")
        cache.set("key2", "value")
        cache.set("key3", "value")
        cache.set("key4", "value")
        self.assertEqual(4, len(cache.objects))
        cache.clean_count()
        self.assertEqual(3, len(cache.objects))

    def test_clean_count_2(self):
        cache = FileCache(10, 1)
        cache.set("key1", "value")
        cache.set("key2", "value")
        cache.set("key3", "value")
        cache.set("key4", "value")
        self.assertEqual(4, len(cache.objects))
        cache.clean_count()
        self.assertEqual(4, len(cache.objects))

    def test_clean_old_1(self):
        cache = FileCache(10, 2)
        cache.get_today = mock.Mock(return_value=datetime.datetime.today().date())
        cache.set("key1", "value")
        cache.get_today = mock.Mock(return_value=(datetime.datetime.today() - datetime.timedelta(days=1)).date())
        cache.set("key2", "value")
        cache.get_today = mock.Mock(return_value=(datetime.datetime.today() - datetime.timedelta(days=2)).date())
        cache.set("key3", "value")
        cache.get_today = mock.Mock(return_value=(datetime.datetime.today() - datetime.timedelta(days=3)).date())
        cache.set("key4", "value")
        self.assertEqual(4, len(cache.objects))
        cache.get_today = mock.Mock(return_value=datetime.datetime.today().date())
        cache.clean_old()
        self.assertEqual(2, len(cache.objects))

    def test_clean_old_2(self):
        cache = FileCache(10, 2)
        cache.set("key1", "value")
        cache.set("key2", "value")
        cache.set("key3", "value")
        cache.set("key4", "value")
        self.assertEqual(4, len(cache.objects))
        cache.clean_old()
        self.assertEqual(4, len(cache.objects))

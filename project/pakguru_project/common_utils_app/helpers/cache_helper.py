import redis
from django.conf import settings


class DummyRedisCacheFactory(object):
    def __init__(self, key_prefix):
        self.key_prefix = key_prefix
        print(f"{key_prefix} - Using Dummy Redis cache ..")

    def incr(self, key):
        pass

    def delete(self, key):
        pass

    def flushdb(self):
        pass

    def keys(self, *args, **kwargs):
        pass

    def scan_iter(self, *args, **kwargs):
        return []


class CacheHelper(object):

    def __init__(self, key_prefix):
        if settings.USING_DUMMY_CACHE:
            self.r = DummyRedisCacheFactory(key_prefix)
        else:
            # connect to redis
            self.r = redis.StrictRedis(host=settings.REDIS_HOST,
                                       port=settings.REDIS_PORT,
                                       db=settings.REDIS_DB)
            print(f"{key_prefix} - Using Redis cache ..")

        self.key_prefix = key_prefix

    def get_key(self, key):
        return f'{self.key_prefix}:' + key

    def get_timeout(self):
        return settings.CACHE_TIMEOUT

    def increment(self, key):
        return self.r.incr(self.get_key(key))

    def delete(self, key):
        return self.r.delete(self.get_key(key))

    def clear_all(self):
        self.r.flushdb()

    def get_all_keys(self):
        keys_filter = f'{self.key_prefix}:*'
        return self.r.keys(keys_filter)

    def get_all_keys_in_db(self):
        return self.r.keys('*')

    def clear(self):
        keys_filter = f'{self.key_prefix}:*'
        for key in self.r.scan_iter(keys_filter):
            self.r.delete(key)

    def print_all_keys(self):
        keys = self.get_all_keys()
        if not keys:
            print('redis cache is empty')
        else:
            for key in keys:
                print(key)

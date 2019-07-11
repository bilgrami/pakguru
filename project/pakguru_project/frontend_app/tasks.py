import os
from subprocess import Popen

from django.core import management

import pakguru_app as app
from common_utils_app.helpers import cache_helper as ch


class ProcessFeedsTask():

    def worker(self):
        app_path = os.path.dirname(app.__file__)
        cmd = os.path.join(app_path, 'shell_scripts', 'process_show_feeds.sh')
        print('cmd:\n', cmd)
        p = Popen([cmd])
        p.terminate()

    def process_feeds(self):
        print('calling process_feeds command')
        self.worker()
        return 'OK'


class CacheTask():

    def clear_cache(self):
        print('calling clear_cache command')
        c = ch.CacheHelper(key_prefix=None)
        all_keys = c.get_all_keys_in_db()
        before_clear_cache = len(c.get_all_keys_in_db())
        management.call_command("clear_cache")
        after_clear_cache = len(c.get_all_keys_in_db())

        before_cache_helper = len(c.get_all_keys_in_db())
        c.clear_all()
        after_cache_helper = len(c.get_all_keys_in_db())
        data = {
                'before_clear_cache': before_clear_cache,
                'after_clear_cache': after_clear_cache,
                'before_cache_helper': before_cache_helper,
                'after_cache_helper': after_cache_helper,
                'all_keys': str(all_keys),
        }
        return ('OK', data)

    def get_cache(self):
        print('calling get_cache command')
        c = ch.CacheHelper(key_prefix=None)
        all_keys = c.get_all_keys_in_db()
        key_count = len(all_keys)
        data = {
                'key_count': key_count,
                'all_keys': str(all_keys),
        }
        return ('OK', data)

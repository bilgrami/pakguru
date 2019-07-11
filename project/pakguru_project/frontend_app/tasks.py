from django.core import management
import threading


class ProcessFeedTask():

    def worker(self, args):
        param1 = args[0]
        param2 = int(args[1])
        param3 = int(args[2])
        management.call_command("harvest_show_feeds_UNT", param1, param2)
        management.call_command("harvest_show_feeds_DOL", param1, param2)
        management.call_command("harvest_show_feeds_VPK", param1, param2)
        management.call_command("load_harvested_show_feeds", param3)

    def process_feeds(self, param1, param2, param3):
        print('calling command with Arg ->', param1, param2, param3)
        args = (param1, param2, param3,)
        # self.worker(args)
        worker_thread = threading.Thread(target=self.worker, args=args)
        worker_thread.daemon = True
        worker_thread.start()
        return 'done'

from django.core import management


class ProcessFeedTask():

    def process_feeds(data):
        # TODO: make it run async
        print('calling command with Arg ->', data)
        management.call_command("harvest_show_feeds_UNT", "True", data)
        management.call_command("harvest_show_feeds_DOL", "True", data)
        management.call_command("harvest_show_feeds_VPK", "True", data)
        management.call_command("load_harvested_show_feeds", -1)
        return 'done'

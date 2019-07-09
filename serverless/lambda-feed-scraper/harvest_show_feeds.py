import harvest_show_feeds_DOL as DOL
import harvest_show_feeds_UNT as UNT
import harvest_show_feeds_VPK as VPK


class harvest_show_feeds:
    def __init__(self, params):
        self.feed_source = params['feed_source']
        self.params = params


def get_harvest_feed_handler(feed_source):
    if feed_source == 'DOL':
        h = DOL.harvest_show_feeds_UNT()
        return h.get_feed_posts
    elif feed_source == 'UNT':
        h = UNT.harvest_show_feeds_UNT()
        return h.get_feed_posts
    elif feed_source == 'VPK':
        h = VPK.harvest_show_feeds_UNT()
        return h.get_feed_posts
    else:
        raise ValueError(feed_source)

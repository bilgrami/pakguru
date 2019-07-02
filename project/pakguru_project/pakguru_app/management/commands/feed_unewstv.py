import json
import os

from django.core import signing
from django.core.management.base import BaseCommand, CommandError

import requests
from bs4 import BeautifulSoup
from pakguru_app.models import ShowSourceFeed


class Command(BaseCommand):
    def add_arguments(self, parser):
        help_text = 'Process a feed by Feed Id'
        parser.add_argument('feed_id', type=int, help=help_text)

    def handle(self, *args, **options):
        # get feed url by id 
        # find all the links
        # create posts for each link, make sure to not add dupes
        # update the job table with latest date
        # save links as json

        feed_id = options['feed_id']
        print(feed_id)
        feed_url = ShowSourceFeed.get(feed_id).playlist_link
        if not feed_url:
            raise CommandError(f'Feed Playlist for Feed Id {feed_id} not found')
        else:
            print(feed_url)


        # fixture_folder_path = '../../pakguru_app/fixtures'
        # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # root = os.path.join(BASE_DIR, fixture_folder_path)

        # if not os.path.exists(root):
        #     raise CommandError('Folder "%s" does not exist' % root)
        # else:
        #     print(f'Found folder: {root}')
        #     for filename in os.listdir(root):
        #         if filename.endswith(".json"):
        #             input_file_path = os.path.join(root, filename)
        #             output_file = os.path.join(root, 'enc', filename + '.enc')
        #             json_data = open(input_file_path, 'r').read()
        #             enc_json_data = signing.dumps(json_data)
        #             with open(output_file, "w") as enc_file:
        #                 enc_file.write(enc_json_data)

    def get_video_from_post(self, post_url, result_as_json=False):
        page = requests.get(post_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        f = soup.find('iframe')
        embed = f['src']
        link = embed.replace('embed','watch')
        if result_as_json:
            d = {
              'link': link,
              'embed': embed
            }
            result = {}
            result[post_url] = d
            return result
        else:
            return link

    def get_feed_posts(self, base_url, feed_url):
        page = requests.get(feed_url)

        soup = BeautifulSoup(page.content, 'html.parser')
        post_body = soup.find_all('div', class_='post_body')
        result = {}

        for body in post_body:
            heading = body.find('div', class_='heading')
            a = heading.find('a', href=True)
            link = a['href']
            label = a.get_text()

            la = body.find('div', class_='links_area')
            views = la.find_all('span', class_='partition')[0]
            views = views.find('span', class_='highlight').get_text()
            dt = la.find_all('span', class_='partition')[1]
            dt = dt.find('span', class_='highlight').get_text()
            post_url = base_url + link
            d = {
              'dt': dt,
              'link': post_url,
              'video_link': self.get_video_from_post(post_url),
              'label': label,
              'views': views
            }
            result[dt] = d

        # print(result)
        return result



# base_url = 'http://www.unewstv.com'
# feed_url = "http://www.unewstv.com/category/Zara+Hut+Kay+on+Dawn+News"
# result = get_feed_posts(base_url, feed_url)

# # post_url = 'http://www.unewstv.com/150327/zara-hut-kay-human-smuggling-via-marriage-fraud-9th-may-2019'
# # result = get_video_from_post(post_url, result_as_json = True)
# # json_data = json.dumps(result, indent=4)
# # print(json_data)

# for key, value in result.items():
#   date = key
#   post_url = value['link']
#   video_link = get_video_from_post(post_url)
#   print(date, post_url, video_link)


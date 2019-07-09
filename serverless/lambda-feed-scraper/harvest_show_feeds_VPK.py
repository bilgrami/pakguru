import datetime
from urllib.parse import urlparse

import datefinder
import requests
from bs4 import BeautifulSoup


class harvest_show_feeds_VPK:
    def _get_domain_from_link(self, link):
        # if link[:2] == '//':
        #     link = link[2:]
        if 'http' not in link:
            link = 'http:' + link

        return urlparse(link).netloc, link

    def _extract_links_from_iframe(self, content):
        links = []
        soup = BeautifulSoup(content, "html.parser")
        for f in soup.find_all('iframe'):
            links.append(f['src'])
        return links

    def _get_video_from_post(self, url):
        result = {}
        if url:
            content = str(requests.get(url).content)
            soup = BeautifulSoup(content, "html.parser")
            for f in soup.find_all('iframe'):
                original = f['src']
                host, link = self._get_domain_from_link(original)
                link = link.replace('embed', 'watch')

                d = {
                    'link': link,
                    'original': original
                }
                result[host] = d
        return result

    def _process_lising(self, listing, show_name, dict_episode_reference):
        a = listing.find('a', href=True)
        link = a['href']
        div_label_text = listing.find('div', class_='archive-list-text')
        label_text = div_label_text.find('h2').get_text()
        episode = -1
        dt = ''
        if "Episode" in label_text:
            if label_text and len(label_text.split(" Episode ")) == 2:
                episode_running_number = self._get_episode(label_text.split(" Episode ")[1])  # noqa: E501

        dt = self._get_date(label_text, show_name, dict_episode_reference, episode_running_number)  # noqa: E501
        dt = dt.isoformat()
        return (link, label_text, episode, dt)

    def _get_episode(self, str):
        nums = [int(s) for s in str.split() if s.isdigit()]
        return nums[0]

    def _get_date(self, label_text, show_name, dict_episode_reference, episode_running_number):  # noqa: E501
        ei = dict_episode_reference[episode_running_number]
        if ei:
            return ei['original_air_date']
        else:
            if "Episode" in label_text and len(label_text.split(" Episode ")) == 2:  # noqa: E501
                label_text = label_text.split(" Episode ")[1]

            matches = datefinder.find_dates(label_text)
            dt = next(iter(matches), False)
            if dt:
                dt = dt.date().isoformat()
                return dt + datetime.timedelta(days=episode_running_number)

    def _get_feed_posts(self, feed_url, show_name,
                        dict_episode_reference):

        page = requests.get(feed_url)

        soup = BeautifulSoup(page.content, 'html.parser')
        mid_container = soup.find('div', {"id": "archive-list-wrap"})
        post_listings = mid_container.find_all('li', class_='infinite-post')
        result = {}

        for listing in post_listings:
            link, label, episode, dt = self._process_lising(listing, show_name, dict_episode_reference)  # noqa: E501
            d = {
                'label': label,
                'dt': dt,
                'episode': episode,
                'link': link,
                'video_link': self._get_video_from_post(link),
            }
            if dt:
                result[str(dt)] = d

        return result

    def get_feed_posts(self, params):
        feed_url = params['feed_url']
        show_name = params['show_name']
        dict_episode_reference = params['episode_reference']
        return self._get_feed_posts(feed_url, show_name,
                                    dict_episode_reference)

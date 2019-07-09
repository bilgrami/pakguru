import datefinder
import requests
from bs4 import BeautifulSoup


class harvest_show_feeds_DOL:
    def _get_video_from_post(self, post_url):
        if post_url:
            page = requests.get(post_url)
            soup = BeautifulSoup(page.content, 'html.parser')
            f = soup.find('iframe')
            if f:
                embed = f['src']
                return embed.replace('embed', 'watch')
        return ""

    def _process_lising(self, listing):
        heading = listing.find('div', class_='list_cont_title')
        a = heading.find('a', href=True)
        link = a['href']
        label_text = a.get_text().replace(' in HD', '')
        label = label_text.replace(' in HD', '').replace(' IN hd', '')
        category = listing.find('p', class_='list_cont_title').get_text()
        # channel = listing.find('p', class_='list_detail').get_text()
        episode = dt = ''
        in_hd = 'False'
        if "Episode" in label:
            in_hd = 'True' if "-in-hd" in link else 'False'
            if label and len(label.split(" Episode ")) == 2:
                episode = label.split(" Episode ")[1]

            if label and len(label.split(" Episodee ")) == 2:
                episode = label.split(" Episodee ")[1]
        else:
            matches = datefinder.find_dates(label_text)
            dt = next(iter(matches))
            if dt:
                dt = dt.date().isoformat()

        return (link, label_text, category, episode, dt, in_hd)

    def _get_additional_feed_posts(self, feed_url, result, channel, show_name):
        pages = [10, 20, 40, 80, 160, 320, 640]
        for pg in pages:
            data = {'var_post': f'{channel}/{show_name}/{pg}'}

            page = requests.post(url=feed_url, data=data)
            soup = BeautifulSoup(page.content, 'html.parser')
            post_listings = soup.find_all('div', class_='list_contents')

            for listing in post_listings:
                link, label, category, episode, dt, in_hd = self._process_lising(listing)  # noqa: E501
                d = {
                    'label': label,
                    'dt': dt,
                    'channel': channel,
                    'show_name': show_name,
                    'episode': episode,
                    'category': category,
                    'link': link,
                    'video_link': self._get_video_from_post(link),
                    'in_hd': in_hd,
                    'additional': 'True',
                }

                result[str(dt)] = d

        return result

    def _get_feed_posts(self, feed_url, additional_feed_url,
                        channel, show_name_from_feed):

        page = requests.get(feed_url)

        soup = BeautifulSoup(page.content, 'html.parser')
        mid_container = soup.find('div', {"id": "middle-container"})
        post_listings = mid_container.find_all('div', class_='list_contents')
        result = {}

        for listing in post_listings:
            link, label, category, episode, dt, in_hd = self._process_lising(listing)  # noqa: E501
            d = {
                'label': label,
                'dt': dt,
                'channel': channel,
                'show_name': show_name_from_feed,
                'episode': episode,
                'category': category,
                'link': link,
                'video_link': self._get_video_from_post(link),
                'in_hd': in_hd,
                'additional': 'False',
            }

            result[str(dt)] = d

        # load more feed_posts
        latest_episode_key = next(iter(result))
        latest_episode = result[latest_episode_key]
        channel = latest_episode['channel']
        show_name = latest_episode['show_name']
        self._get_additional_feed_posts(additional_feed_url, result, channel, show_name)  # noqa: E501
        return result

    def get_feed_posts(self, params):
        feed_url = params['feed_url']
        additional_feed_url = params['additional_feed_url']
        channel = params['channel']
        show_name_from_feed = params['show_name_from_feed']
        return self._get_feed_posts(feed_url, additional_feed_url,
                                    channel, show_name_from_feed)

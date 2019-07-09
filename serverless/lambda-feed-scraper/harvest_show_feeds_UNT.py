from datetime import datetime
import requests
from bs4 import BeautifulSoup


class harvest_show_feeds_UNT:
    def _get_video_from_post(self, post_url,
                             result_as_json=False):
        if post_url is not None:
            page = requests.get(post_url)
            soup = BeautifulSoup(page.content, 'html.parser')
            f = soup.find('iframe')
            if f is not None:
                embed = f['src']
                link = embed.replace('embed', 'watch')
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
            else:
                return ""

    def _get_feed_posts(self, base_url, feed_url):

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
            dt_label = dt.find('span', class_='highlight').get_text()
            dt = datetime.strptime(dt_label, '%B %d, %Y')
            dt = dt.date().isoformat()

            post_url = base_url + link
            d = {
                'dt_label': dt_label,
                'link': post_url,
                'video_link': self._get_video_from_post(post_url),
                'label': label,
                'views': views
            }
            result[str(dt)] = d

        return result

    def get_feed_posts(self, params):
        base_url = params['base_url']
        feed_url = params['feed_url']
        return self._get_feed_posts(base_url, feed_url)

import json
from datetime import datetime

# import boto3
import requests
from bs4 import BeautifulSoup


# def save_file_to_s3(bucket, file_name, data):
#   s3 = boto3.resource('s3')
#   obj = s3.Object(bucket, file_name)
#   obj.put(Body=json.dumps(data))


def get_video_from_post(post_url,
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


def get_feed_posts(base_url, feed_url):
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
            'video_link': '',  # get_video_from_post(post_url),
            'label': label,
            'views': views
        }
        result[str(dt)] = d

    return result


def main(event, context):
    base_url = 'http://www.unewstv.com'
    feed_url = 'http://www.unewstv.com/category/Zara+Hut+Kay+on+Dawn+News'
    result = get_feed_posts(base_url, feed_url)
    body = json.dumps(result, indent=4)

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

# main(None,None)
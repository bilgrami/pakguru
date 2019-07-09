import json
import harvest_show_feeds
# import boto3
# def save_file_to_s3(bucket, file_name, data):
#   s3 = boto3.resource('s3')
#   obj = s3.Object(bucket, file_name)
#   obj.put(Body=json.dumps(data))


def main(event, context):

    feed_source = event['feed_source']
    harveset_handler = harvest_show_feeds.get_harvest_feed_handler(feed_source)
    result = harveset_handler(event)
    body = json.dumps(result)

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

# event = {
#   "feed_source": "UNT",
#   "base_url": "http://www.unewstv.com",
#   "feed_url": "http://www.unewstv.com/category/Aapas+Ki+Baat+With+Najam+Sethi"
# }
# result = main(event, None)
# print(result)

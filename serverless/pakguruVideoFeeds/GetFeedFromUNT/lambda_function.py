import boto3
import json
from GetFeedFromUNT.harvest_show_feeds_UNT import harvest_show_feeds_UNT
from datetime import datetime


def save_file_to_s3(bucket, file_name, data):
    """saves file to s3 bucket and make it available publicly
      # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Object.put
    
    """
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket, file_name)
    acl='public-read'
    obj.put(Body=data, ACL=acl)


BUCKET_NAME = 'devstorage.pak.guru'
COLLECTION_NAME = 'video_feeds'

def get_file_name_for_storage(collection_name, file_prefix):
    """computes file_name to be stored in a cloud bucket
    Returns 
    a string containing filename in the following format 
    {collection_name}/{folder}/{file_name_with_time}
    where
        folder: of format {year}/{today}
            year: 4 digit year YYYY
            today: Today's date in format YYYY-MM-DD
        file_name_with_time is in format {today}-{file_prefix}
            today: Today's date in format YYYY-MM-DD
    """    
    dt = datetime.today()
    year = dt.strftime('%Y')
    today = dt.strftime('%Y-%m-%d')

    folder = f'{year}/{today}'
    file_name_with_time = f'{today}-{file_prefix}'
    return f'{collection_name}/{folder}/{file_name_with_time}'
    
def parse_params(event):
    """reads and parse input params available in event dictionary
    Returns a tuple containing following params values 
        feed_source, base_url, feed_url, feed_name
    """
    if 'body' in event.keys():
      params_dict = json.loads(event['body'])
    else:
      params_dict = event
      
    feed_source = params_dict['feed_source']
    base_url = params_dict['base_url']
    feed_url = params_dict['feed_url']
    feed_name = params_dict['feed_name']
    
    return feed_source, base_url, feed_url, feed_name
  
def lambda_handler(event, context):
    feed_source, base_url, feed_url, feed_name = parse_params(event)
    
    h = harvest_show_feeds_UNT()
    result =  h.get_feed_posts(base_url, feed_url)

    body = json.dumps(result, indent=4, sort_keys=True)

    file_prefix = f'{feed_name}.json'
    file_name = get_file_name_for_storage(COLLECTION_NAME, file_prefix)
    save_file_to_s3(BUCKET_NAME, file_name, body)
    
    response = {
        "headers": {
        "x-custom-response-header": "my custom response header value"
        },
        "statusCode": 200,
        "body": result,
    }

    return response



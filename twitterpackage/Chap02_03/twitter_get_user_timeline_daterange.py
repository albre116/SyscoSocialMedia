# Chap02-03/twitter_get_user_timeline_daterange.py
import sys
import json
from tweepy import Cursor
from twitter_client import get_twitter_client
from argparse import ArgumentParser
from datetime import datetime
from datetime import timezone    

def get_parser():
    parser = ArgumentParser("Clustering of followers")
    parser.add_argument('--username')
    parser.add_argument('--startdate')
    return parser

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    print("Length of Arguments {}".format(args))
    
    user = args.username
    startdate = datetime.strptime(args.startdate, "%Y-%m-%d").date()
    client = get_twitter_client()
    fname = "user_timeline_{}.jsonl".format(user)
    with open(fname, 'w') as f:
        for page in Cursor(client.user_timeline, screen_name=user, count=200).pages(16):
            for status in page:
                created_at_time = datetime.strptime(status._json['created_at'], '%a %b %d %H:%M:%S %z %Y').replace(tzinfo=timezone.utc).astimezone(tz=None).date()
                if created_at_time >= startdate:
                    f.write(json.dumps(status._json)+"\n")


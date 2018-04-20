# Chap02-03/twitter_mutual_friend_followers.py
import os
import sys
import json
import time
import math
from tweepy import Cursor
import tweepy
from twitter_client import get_twitter_client
import sys
import json
from random import sample

MAX_FRIENDS = 25000

def usage():
    print("Usage:")
    print("python {} <username>".format(sys.argv[0]))
    
def paginate(items, n):
    """Generate n-sized chunks from items"""
    for i in range(0, len(items), n):
        yield items[i:i+n]

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)
    screen_name = sys.argv[1]
    followers_file = 'users/{}/followers.jsonl'.format(screen_name)
    friends_file = 'users/{}/friends.jsonl'.format(screen_name)
    with open(followers_file) as f1, open(friends_file) as f2:
        t0 = time.time()
        followers = []
        friends = []
        for line in f1:
            profile = json.loads(line)
            followers.append(profile['screen_name'])
        for line in f2:
            profile = json.loads(line)
            friends.append(profile['screen_name'])
        t1 = time.time()
        mutual_friends = [user for user in friends if user in followers]
        followers_not_following = [user for user in followers if user not in friends]
        friends_not_following = [user for user in friends if user not in followers]
        t2 = time.time()
        print("{} has {} mutual friends".format(screen_name, len(mutual_friends)))

    ###now we do the calls 
    client = get_twitter_client()
    i = 0
    for mutual in mutual_friends:
        i += 1
        print("Getting Followers for {} which is {} of {}".format(mutual, i, len(mutual_friends)))
        screen_name = mutual
        dirname = "users/{}".format(screen_name)
        max_pages = math.ceil(MAX_FRIENDS / 5000)
        try:
            os.makedirs(dirname, mode=0o755)
        except OSError:
            print("Directory {} already exists moving to next".format(dirname))
            continue
        except Exception as e:
            print("Error while creating directory {}".format(dirname))
            print(e)
            sys.exit(1)
        # get followers for a given user
        fname = "users/{}/followers.jsonl".format(screen_name)
        with open(fname, 'w') as f:
            status = client.rate_limit_status()
            nfollowers = status['resources']['followers']['/followers/ids']['remaining']
            while nfollowers <= 1:
                    print("Sleeping for 30 seconds to check rate limit which is at {}".format(nfollowers))
                    time.sleep(30)
                    status = client.rate_limit_status()
                    nfollowers = status['resources']['followers']['/followers/ids']['remaining']
                    print("Checked API and limit is at {}".format(nfollowers))
            try:
                for followers in Cursor(client.followers_ids, screen_name=screen_name).pages(max_pages):
                    for chunk in paginate(followers, 100):
                        users = client.lookup_users(user_ids=chunk)
                        for user in users:
                            f.write(json.dumps(user._json)+"\n")

                    status = client.rate_limit_status()
                    nfollowers = status['resources']['followers']['/followers/ids']['remaining']
                    while nfollowers <= 1:
                            print("Sleeping for 30 seconds to check rate limit which is at {}".format(nfollowers))
                            time.sleep(30)
                            status = client.rate_limit_status()
                            nfollowers = status['resources']['followers']['/followers/ids']['remaining']
                            print("Checked API and limit is at {}".format(nfollowers))
            except tweepy.TweepError:
                print("Failed to run the followers command on that user, Skipping...")

        # get friends for a given user
        fname = "users/{}/friends.jsonl".format(screen_name)
        with open(fname, 'w') as f:
            status = client.rate_limit_status()
            nfollowers = status['resources']['friends']['/friends/ids']['remaining']
            while nfollowers <= 1:
                    print("Sleeping for 30 seconds to check rate limit which is at {}".format(nfollowers))
                    time.sleep(30)
                    status = client.rate_limit_status()
                    nfollowers = status['resources']['friends']['/friends/ids']['remaining']
                    print("Checked API and limit is at {}".format(nfollowers))
            
            try:
                for friends in Cursor(client.friends_ids, screen_name=screen_name).pages(max_pages):
                    for chunk in paginate(friends, 100):
                        users = client.lookup_users(user_ids=chunk)
                        for user in users:
                            f.write(json.dumps(user._json)+"\n")
                    status = client.rate_limit_status()
                    nfollowers = status['resources']['friends']['/friends/ids']['remaining']
                    while nfollowers <= 1:
                            print("Sleeping for 30 seconds to check rate limit which is at {}".format(nfollowers))
                            time.sleep(30)
                            status = client.rate_limit_status()
                            nfollowers = status['resources']['friends']['/friends/ids']['remaining']
                            print("Checked API and limit is at {}".format(nfollowers))
            except tweepy.TweepError:
                print("Failed to run the friends command on that user, Skipping...")


        # get user's profile
        fname = "users/{}/user_profile.json".format(screen_name)
        with open(fname, 'w') as f:
            profile = client.get_user(screen_name=screen_name)
            f.write(json.dumps(profile._json, indent=4))
    
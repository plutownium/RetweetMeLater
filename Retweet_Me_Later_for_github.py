import tweepy
import os
from flask import Flask

# RetweetMeLater

# https://github.com/tweepy/tweepy/issues/1192 On building tweet urls
# https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object
# Ctrl + F "retweet_count" and "favorite_count"

# Goal: Retrieve all of a user's tweets for the past twelve months and filter by most popula
# Goal: sort by most retweeted, most liked, most replied to and give top 10 per year, per month, per week

consumer_key = "xxx"
consumer_secret = "xxx"

access_token = "331107386-xxx"
access_token_secret = "xxx"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet.text)


def get_all_tweets(screen_name):
    # https://gist.github.com/yanofsky/5436496
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    all_tweets = []	 # initialize a list to hold all the tweepy Tweets

    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

    all_tweets.extend(new_tweets) # Save most recent tweets

    oldest = all_tweets[-1].id

    while len(new_tweets) > 0:
        print("Getting tweets before %s)" % oldest)
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)
        all_tweets.extend(new_tweets)
        oldest = all_tweets[-1].id - 1

        print("...%s tweets downloaded so far" % len(all_tweets))

    # out_tweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in all_tweets]
    print([[tweet.id for tweet in all_tweets]])

# for tweet in tweepy.Cursor(api.search,q="#unitedAIRLINES",count=100,
#                            lang="en",
#                            since="2017-04-03").items():
#     print (tweet.created_at, tweet.text)


def get_url_of_tweet(tweet):
    print("URL of the tweet: https://twitter.com/{}/status/{})"
          .format(tweet.user.screen_name, tweet.id))
    return "https://twitter.com/{}/status/{})".format(tweet.user.screen_name, tweet.id)


main_account = "EdLatimore"
eddy = api.get_user(main_account)


a = 0
list_of_tweets = []
tweet_iter = tweepy.Cursor(api.user_timeline, id=main_account).items()  # A list of tweets ?

for tweet in tweet_iter:
    url = "https://twitter.com/{}/status/{})".format(tweet.user.screen_name, tweet.id)
    if tweet.text[0:2] == "RT":
        pass
    else:
        list_of_tweets.append([tweet.retweet_count, tweet.favorite_count, tweet.id, tweet.text, url, tweet.created_at])

    # a += 1
    # if a > 40:
    #     break

b = sorted(list_of_tweets, reverse=True)

number = 1
for i in b[0:40]:
    print("{}: {}; URL: {}; RTs: {}; DATE: {}".format(number, i[3], i[4], i[0], i[-1]))
    number += 1

print(len(list_of_tweets))

# Goal: Get an entire month of tweets.
# Goal: Display only tweets made by the account itself, not RTs of other accounts.

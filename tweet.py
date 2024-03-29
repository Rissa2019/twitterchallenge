import tweepy import datetime

#authenticate
consumer_key= 'QpofFWZncjIRUJUNSwNWcikHj'
consumer_secret= '7ewZRAXZJeRfD49FglYzuirerka2RcMErFSWKMtkUmotz5ucc5'
access_token='1161503197481054209-MfiuR0aEEdi47fsrKE9fF1x67YUx2x'
access_token_secret='3zUcEiffyr1ybtkmgjuVjbiMiQO2WaqzZlTwBLF3RZ2Os'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

max_tweets = 1000000
celebrities = ["@katyperry", "@justinbieber", "@BarackObama", "@rihanna", "@taylorswift13", "@ladygaga", "@TheEllenShow", "@cristiano", "@timberlake", "@ArianaGrande"]
# Since we're using the standard Twitter API, there is a rate limit of 180 requests per 15 mins and maximum 100 entries per request.
# Therefore, to make this realistic, we are restricting the time frame to be 1 hour: 23:00 08/14/2019 - 00:00 08/15/2019
start_time = datetime.datetime(2019, 8, 14, 23, 0)

def get_cele_tweeted_by_count(query):
    searched_tweets = []
    last_id = -1
    passed_date = False
    tweet_authors = {}
    while len(searched_tweets) < max_tweets:
        count = max_tweets - len(searched_tweets)
        try:
            new_tweets = api.search(q=query, until='2019-08-15', count=count, max_id=str(last_id - 1))
            if not new_tweets:
                break
            for tweet in new_tweets:
                if tweet.created_at >= start_time:
                    author = tweet.author.name
                    tweet_authors[author] = tweet_authors.get(author, 0) + 1
                    searched_tweets.append(tweet)
                else:
                    passed_date = True
                    break
            if passed_date:
               break
            last_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # depending on TweepError.code, one may want to retry or wait
            # to keep things simple, we will give up on an error
            print e
            break
    if tweet_authors:
        import operator
        most_tweet_author = max(tweet_authors.iteritems(), key=operator.itemgetter(1))[0]
        most_tweet_author = most_tweet_author.encode('utf8')
    else:
        most_tweet_author = None
    return len(searched_tweets), most_tweet_author

max_tweeted_c = ""
max_tweeted_num = 0
most_tweeted_author = ""
for c in celebrities:
    count, most_tweet_author = get_cele_tweeted_by_count(c)
    if count > max_tweeted_num:
         max_tweeted_num = count
         max_tweeted_c = c
         most_tweeted_author = most_tweet_author
    print "celebrity", c, "tweeted by", count, "times.", most_tweet_author, "tweeted the celetrity most."
print "The celebrity who has been the most tweeted about in the specified time frame is", max_tweeted_c
print most_tweeted_author, "tweeted the celebrity most."

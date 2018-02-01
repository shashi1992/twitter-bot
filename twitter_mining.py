from twitter import Api
import re
from textblob import TextBlob
import pandas as pd
import time
from sumy.parsers.plaintext import PlaintextParser
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import matplotlib.pyplot as plt
import numpy as np

consumer_key = 'KW8NkeYXXPC8cYfwBUwMKTBWs'
consumer_secret = 'j69TIjMuLku7izDJd4fiSiba9XZlZpFuPvUWqRrIX9EZcNZ4HU'
access_token = '958267208177561600-y7lHwWd1cljCgfyYfdeFBFvSDQy2PCO'
access_secret = 'UUABVxyKBaS0MizBhqsKDGX04j7srPw2osAqxIXMFxH4d'

hashtag_list = ['#bitcoin', '#ripple', '#bitcoincash', '#ethereum', '#litecoin']

api = Api(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_token, access_token_secret=access_secret)

def clean_tweet(tweet):
    #clean tweet text by removing links and special characters
    return ' '.join(re.sub(r"(htt\w*:\S*)|(RT @[A-Za-z0-9]+)|(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])", " ", tweet).split())

def get_tweets_by_subject(api, query_or_hashtag, count=20):
    tweets = []
    fetch_tweets = api.GetSearch(term=query_or_hashtag, count=count, lang='en')

    for tweet in fetch_tweets:
        parsed_tweet = {}
        parsed_tweet['query'] = query_or_hashtag
        tweet = tweet.AsDict()

        tweet_text = tweet['text']
        parsed_tweet['raw_tweet'] = tweet_text
        cleaned_tweet = clean_tweet(tweet_text)
        parsed_tweet['clean_tweet'] = cleaned_tweet
        blob = TextBlob(cleaned_tweet)

        parsed_tweet['polarity'] = blob.polarity

        if blob.polarity > 0:
            parsed_tweet['sentiment'] = 'Positive'
        elif blob.polarity < 0:
            parsed_tweet['sentiment'] = 'Negative'
        else:
            parsed_tweet['sentiment'] = 'Neutral'

        try:
            parsed_tweet['hash_tags'] = [v for v in tweet['hashtags'][0].values()]
        except:
            parsed_tweet['hash_tags'] = None

        tweets.append(parsed_tweet)
    return tweets

def get_tweets_by_user(api, twitter_handle, count=10):
    tweets = []
    fetch_tweets = api.GetUserTimeline(screen_name=twitter_handle, count=count)

    for tweet in fetch_tweets:
        parsed_tweet = {}
        parsed_tweet['query'] = twitter_handle
        tweet = tweet.AsDict()

        tweet_text = tweet['text']
        parsed_tweet['raw_tweet'] = tweet_text
        cleaned_tweet = clean_tweet(tweet_text)
        parsed_tweet['clean_tweet'] = cleaned_tweet
        blob = TextBlob(cleaned_tweet)

        parsed_tweet['polarity'] = blob.polarity

        if blob.polarity > 0:
            parsed_tweet['sentiment'] = 'Positive'
        elif blob.polarity < 0:
            parsed_tweet['sentiment'] = 'Negative'
        else:
            parsed_tweet['sentiment'] = 'Neutral'

        try:
            parsed_tweet['hash_tags'] = [v for v in tweet['hashtags'][0].values()]
        except:
            parsed_tweet['hash_tags'] = None

        tweets.append(parsed_tweet)
    return tweets

def create_tweet_df(list_of_tweets):
    return pd.DataFrame.from_records(data=list_of_tweets)


twitter_tweets = get_tweets_by_subject(api, "#ripple")

df = create_tweet_df(twitter_tweets)

df.groupby(['query', 'sentiment'])['sentiment'].count()

collect_tweets_df = pd.DataFrame()
for tag in hashtag_list:
    tweets_by_hashtag = get_tweets_by_subject(api, query_or_hashtag=tag, count=30)
    df = create_tweet_df(tweets_by_hashtag)
    collect_tweets_df = collect_tweets_df.append(df)
    # time.sleep(300)
collect_tweets_df = collect_tweets_df.reset_index()
print(collect_tweets_df)

number = len(collect_tweets_df['query'].unique())

abc = collect_tweets_df.groupby(['query', 'sentiment'])['sentiment'].count().unstack().fillna(0)
plot1 = abc[['Negative', 'Neutral', 'Positive']].plot(kind='bar', stacked=True, figsize=(12,9))

api.PostUpdate('Sentiment Analysis of tweets', media='Figure_1.jpeg')
# p1 = plt.bar(np.arange(number), abc['Negative'], color='r')
# p2 = plt.bar(np.arange(number), abc['Neutral'], color='b')
# p3 = plt.bar(np.arange(number), abc['Positive'], color='g')
# plt.xticks(np.arange(number), collect_tweets_df['query'].unique())
# plt.show()




collect_tweets_df.to_csv('twitter_crypto.csv', encoding='utf-8')






if __name__ == '__main__':
    collect_tweets_df = pd.DataFrame()
    for tag in hashtag_list:
        tweets_by_hashtag = get_tweets_by_subject(api, query_or_hashtag=tag, count=30)
        df = create_tweet_df(tweets_by_hashtag)
        collect_tweets_df = collect_tweets_df.append(df)

        # time.sleep(300)
    collect_tweets_df = collect_tweets_df.reset_index()
    print(collect_tweets_df)








# with open('tweets_dump.txt', 'a+') as f:
#     for i in twitter_tweets:
#         f.write(i['clean_tweet'].encode('ascii', 'ignore') + ". ")
#     f.close()

# filename = "tweets_dump.txt"
#
# parser = PlaintextParser.from_file(filename, Tokenizer("english"))
#
# parser2 = HtmlParser.from_url("https://www.coindesk.com/ripple-vets-raising-money-for-cryptocurrency-hedge-fund/", Tokenizer('english'))
#
# summarizer = LexRankSummarizer()
#
# summary = summarizer(parser2.document, 1) #Summarize the document with 5 sentences
#
# object_lists = []
#
# for sentence in summary:
#     print sentence
#     object_lists.append(str(sentence))
#
# print(object_lists)
#
# update1 = api.PostUpdate(' '.join(object_lists))








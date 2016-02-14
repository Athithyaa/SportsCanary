# coding=utf-8
from nltk.corpus import twitter_samples
import re

input_file = twitter_samples.abspath("tweets.20150430-223406.json")

"""
NLTK Guide
After importing text

text1.similar("WORD") returns words with similar meaning to what we are searching for.


"""


class TweetProcessor:
    def __init__(self):
        pass

    @staticmethod
    def standardize_tweet(tweet):
        # Convert to lowercase
        """
        This method seeks to standardize tweets, currently it removes RT
        from the beginning of the tweet, it replaces #'s with those words,
        it replaces @USERNAME with the code USER and it removes any extra
        whitespaces it finds.

        :param tweet: A single tweet, currently as a string, in the future
        we could change this so it takes in a tweet object, with user id and
        other params that we wish to analyze

        :return: returns a single standardized tweet
        """
        tweet = tweet.lower()

        # remove RT if it's there
        # TODO: - Some sort of counter for this would be great
        if tweet[:2] == "rt":
            tweet = tweet[3:]

        # Replace #{word} with word
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)

        # Replace @{user} with USER
        tweet = re.sub('@[^\s]+', 'USER', tweet)

        # Remove extra whitespaces
        tweet = re.sub(r'[\s]+', ' ', tweet)

        return tweet


# A tweet with RT @, #'s and extra blank spaces for testing purposes
twit = u'RT @atirathaich:      #PeytonManning’s squeaky-clean' \
       u'image was built on lies https://t.co/Dh23C5iSpj #DenverBroncos #CamNewton #NFL #SuperBowl …'

t = TweetProcessor()
print t.standardize_tweet(twit)
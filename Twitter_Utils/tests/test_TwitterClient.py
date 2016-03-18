import unittest
from Twitter_Utils.TwitterClient import TwitterClient


class TestTwitterClient(unittest.TestCase):
    def test___init__(self):
        twitter_client = TwitterClient()
        self.assertIsNot("", twitter_client.APP_KEY)
        self.assertIsNot("", twitter_client.APP_SECRET)
        self.assertIsNot("", twitter_client.OAUTH_TOKEN)
        self.assertIsNot("", twitter_client.OAUTH_TOKEN_SECRET)
        self.assertIsNotNone(twitter_client.auth)
        self.assertIsNotNone(twitter_client.api)

    def test_tweet(self):
        assert True

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
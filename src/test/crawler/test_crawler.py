import unittest

from main.crawler.crawler import MyCrawler


class TestCrawlerMethods(unittest.TestCase):

    def setUp(self):
        self.crawler = MyCrawler("www.google.com")

    def test_getUrl(self):
        self.assertEqual(self.crawler.getUrl(), "www.google.com")

if __name__ == '__main__':
    unittest.main()
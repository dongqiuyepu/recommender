import unittest2 as unittest

from src.main.crawler import MyCrawler


class TestCrawler(unittest.TestCase):
    def setUp(self):
        self.crawler = MyCrawler("www.google.com")

    def test_getUrl(self):
        self.assertEqual(self.crawler.getUrl(), "www.google.com")

if __name__ == '__main__':
    unittest.main()
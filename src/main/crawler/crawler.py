import logging


class MyCrawler:

    logging.basicConfig(level=logging.DEBUG)

    def __init__(self, url):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(10)
        self.logger.info("Creating new MyCrawler")
        self.url = url

    def get_url(self):
        self.logger.info("Getting url...")
        return self.url


if __name__ == '__main__':
    crawler = MyCrawler("asdfasdf")
    print(crawler.get_url())

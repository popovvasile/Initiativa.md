# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from dynamic_scraper.spiders.django_spider import DjangoSpider
from newsletter.models import ToScrapeWebsite, Law, ArticleItem


class ArticleSpider(DjangoSpider):

    name = 'particip'

    def __init__(self, *args, **kwargs):
        self._set_ref_object(ToScrapeWebsite, **kwargs)
        self.scraper = self.ref_object.scraper
        self.scrape_url = self.ref_object.url
        self.scheduler_runtime = self.ref_object.scraper_runtime
        self.scraped_obj_class = Law
        self.scraped_obj_item_class = ArticleItem
        super(ArticleSpider, self).__init__(self, *args, **kwargs)
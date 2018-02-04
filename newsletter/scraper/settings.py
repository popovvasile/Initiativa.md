from __future__ import unicode_literals
import os,sys
import django



# sys.path.append('<abs path to initiativa/>')
# os.environ['DJANGO_SETTINGS_MODULE'] = "src.settings"


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trydjango18.settings") #Changed in DDS v.0.3






BOT_NAME = 'newsletter'

SPIDER_MODULES = ['dynamic_scraper.spiders', 'newsletter.scraper',]
USER_AGENT = '%s/%s' % (BOT_NAME, '1.0')

#Scrapy 0.20+
ITEM_PIPELINES = {
    'dynamic_scraper.pipelines.ValidationPipeline': 400,
    'newsletter.scraper.pipelines.DjangoWriterPipeline': 800,
}


django.setup()
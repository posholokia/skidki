from django.core.management.base import BaseCommand
from scraper.scraper.spiders.sunlight import SunlightSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


# "py manage.py runspider" to save the items to the database

class Command(BaseCommand):
    """
    Вышеупомянутый класс представляет собой специальную команду Python,
    которая запускает пауков для очистки веб-страниц с использованием платформы Scrapy.
    """
    help = "Release the spiders"

    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())
        process.crawl(SunlightSpider)
        process.start()

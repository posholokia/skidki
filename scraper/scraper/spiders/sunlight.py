import re
from ..utils import DataUpdate
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class SunlightSpider(CrawlSpider):
    name = "sunlight"
    allowed_domains = ["sunlight.net"]
    start_urls = ["https://sunlight.net/catalog"]

    rules = (Rule(LinkExtractor(allow=("html",),
                                deny=("product-reviews",),
                                deny_domains=("spb.sunlight.net",
                                              "nnov.sunlight.net",
                                              "ekb.sunlight.net",
                                              "rnd.sunlight.net",
                                              "nsk.sunlight.net",
                                              "smr.sunlight.net",
                                              "krd.sunlight.net"), ), callback="parse_item", follow=True),)

    # Here we are filtering the url ↓
    def parse_item(self, response):
        # Checking if the number of digits in the URL is greater than or equal to 4 ↓.
        if len(re.findall('[0-9]', str(response.url))) >= 4:
            # Checking if the last four characters of the URL are equal to "html".
            # This is used to filter out URLs that do not end with ".html" and only process those that do.
            if str(response.url)[-4:] == "html":
                try:
                    title = response.css(
                        "h1.supreme-product-card__about-title::text"
                    ).get().strip()

                    current_price = response.css(
                        "div.supreme-product-card__price-discount-price::text"
                    ).get().strip().encode("ascii", "ignore").decode()

                    url = response.url

                    shop = response.css(
                        "div.footer-info-line__title span::text"
                    ).get().strip()

                    description = " ".join(response.css(
                        "li > p.supreme-product-card__description::text"
                    ).get().split())

                    old_price = response.css(
                        "div.supreme-product-card__price-old::text"
                    ).get().strip().encode("ascii", "ignore").decode()

                    image = response.css(
                        "img.supreme-product-card-slider-pagination__img::attr(src)"
                    ).get()

                    brand = response.css(
                        "a.supreme-product-card-description__item-text::text"
                    ).get().strip()

                    category = response.css(
                        "div.supreme-product-card__header-breadcrumbs span::text"
                    )[2].get().strip()
                except Exception as error:
                    print(f"AttributeError in {error} with {response.url}")
                else:
                    support = DataUpdate(title,
                                         current_price,
                                         url,
                                         shop,
                                         description,
                                         old_price,
                                         image,
                                         brand,
                                         category)
                    support.add_product()

            yield {"url": response.url}

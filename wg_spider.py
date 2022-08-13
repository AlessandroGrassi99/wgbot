import scrapy

class QuotesSpider(scrapy.Spider):
    name = "wg-gesucht"

    def start_requests(self):
        urls = [
            'https://www.wg-gesucht.de/en/wg-zimmer-und-1-zimmer-wohnungen-und-wohnungen-und-haeuser-in-Munchen.90.0+1+2+3.1.0.html?user_filter_id=7134295&ad_type=0&offer_filter=1&city_id=90&noDeact=1&dFr=1659045600&dTo=1664920800&rMax=800&sin=1&exc=2&img_only=1&ot=2114%2C2123%2C2124%2C2131%2C2132%2C2133&categories=0%2C1%2C2%2C3&rent_types=0',
            'https://www.wg-gesucht.de/en/wg-zimmer-und-1-zimmer-wohnungen-und-wohnungen-und-haeuser-in-Garching-b-Munchen.400.0+1+2+3.1.0.html?user_filter_id=7134280&ad_type=0&offer_filter=1&city_id=400&noDeact=1&dFr=1659045600&dTo=1664920800&rMax=800&sin=1&exc=2&img_only=1&categories=0%2C1%2C2%2C3&rent_types=0',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        entries = response.xpath('//div[contains(@id, "main_column")]//div[contains(@class, "wgg_card offer_list_item")]//h3[contains(@class, "truncate_title")]//a[contains(@href, "/en/")]/@href').getall()
        for i, entry in enumerate(entries):
            # print("{}: {}".format(i, entry))
            if not 'airbnb.pvxt.net' in entry:
                yield { "data-id": entry }


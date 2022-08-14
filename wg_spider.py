from typing import List
from bs4 import BeautifulSoup
from lxml import etree
import urllib3

XPATH_OFFER_URL = '//div[contains(@id, "main_column")]//div[contains(@class, "wgg_card offer_list_item")]//h3[contains(@class, "truncate_title")]//a[contains(@href, "/en/")]/@href'


class FilterSpider():
    def __init__(self, urls: List[str]):
        self.urls = urls
        self.http = urllib3.PoolManager()

    def get_pages_content(self) -> List[str]:
        pages = []

        for url in self.urls:
            res = self.http.request('GET', url)

            if res.status == 200:
                pages.append(res)
        return pages

    def get_offers(self) -> List[str]:
        pages = self.get_pages_content()

        urls = []
        for page in pages:
            soup = BeautifulSoup(page.data, "html.parser")
            dom = etree.HTML(str(soup))
            urls.extend(dom.xpath(XPATH_OFFER_URL))
        return list(set(urls))

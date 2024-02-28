from typing import Any

import scrapy
from scrapy import Request
from scrapy.http import Response

from ..services.streeteasy_rent_parser import StreeteasyRentParser
from ..services.details_parser import DetailsParser


class StreetEasyRentSpider(scrapy.Spider):
    name = "streeteasy_rent"
    start_urls = ['https://streeteasy.com/for-rent/nyc']
    rent_parser = StreeteasyRentParser()
    
    def parse(self, response: Response, **kwargs: Any) -> Any:
        rent_listings = response.css('.listingCard-globalLink::attr(href)').getall()

        for listing in rent_listings:
            yield Request(url=listing, callback=self.rent_parser.parse_rent)
    
        next_page = self.next_page(response) 
        if next_page is not None:  
            self.logger.debug(f"Flipping a page: {next_page.url}")
            yield next_page

    def next_page(self, response: Response) -> Request:
        next_button_href = response.css('li.next a::attr(href)').get()
        self.logger.info(f"A next button href: {next_button_href}")
        
        if next_button_href is None:
            return None
        next_page_url = response.urljoin(next_button_href)
        
        return Request(url=next_page_url, 
                       callback=self.parse)
        
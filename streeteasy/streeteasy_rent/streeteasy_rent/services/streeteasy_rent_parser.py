from ..services.details_parser import DetailsParser
from ..items import ApartmentDetails, StreeteasyRentItem
from scrapy.http import Response
import logging

class StreeteasyRentParser:
    details_parser = DetailsParser()
    
    def parse_rent(self, response: Response) -> StreeteasyRentItem:
        price = self.parse_price(response)
        title = self.parse_title(response)
        details = self.parse_details(response)
        amenities = self.parse_amenities(response)
        neighbourhood = self.parse_neighbourhood(response)
        days_on_market = self.parse_days_on_market(response)
        listing_link = response.url

        return StreeteasyRentItem(
            title=title,
            price=price,
            area=details.area,
            beds_number=details.beds_number,
            baths_number=details.baths_number,
            rooms_number=details.rooms_number,
            amenities=amenities,
            neighbourhood=neighbourhood,
            days_on_market=days_on_market,
            listing_link=listing_link
        )

    def parse_price(self, response: Response) -> str:
        price = response.css('.price::text').get()
        clean_price = price.replace('\n', '').strip()
        if clean_price == '':
            logging.error(f'Price is empty ({response.css(".price::text").get()}): {response.url}')
            logging.error(f"{response.css('.price').get()}")
            
            price_backup = response.xpath('normalize-space(//div[contains(@class, "price")]/text()[normalize-space()])').get()
            logging.debug(f"Price backup: {price_backup}")
            clean_price = price_backup
            

        return clean_price

    def parse_title(self, response: Response) -> str:
        title = response.css('.incognito::text').get()
        if title == '' or title is None:
            logging.error(f"Title is empty or None")

        return title

    def parse_details(self, response: Response) -> ApartmentDetails:
        items = response.css('.detail_cell::text').getall()
        parsed_items = self.details_parser.parse_details(items)

        return parsed_items

    def parse_amenities(self, response: Response):
        highlight_amenities = [item.replace('\n', '').strip() for item in response.css('.AmenitiesBlock-highlightsLabel div::text').getall()] 
        other_amenities = [item.replace('\n', '').strip() for item in response.css('.AmenitiesBlock-item::text').getall()]
        
        aggregated = highlight_amenities + other_amenities
        clean_aggregated = [item for item in aggregated if item != '']
        
        return clean_aggregated 
    
    def parse_days_on_market(self, response: Response):
        days_selector = response.xpath("//div[contains(.//h6, 'Days On Market')]/div[@class='Vitals-data']/text()")
        days = days_selector.get()
        if days is None:
            return None
        
        return days.replace('\n', '').strip()
    
    def parse_neighbourhood(self, response: Response):
        neighbourhood = response.css('.Breadcrumb-item span::text').getall()[1:]
        
        return neighbourhood
        
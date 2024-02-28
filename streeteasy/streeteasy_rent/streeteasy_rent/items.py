# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass
from typing import Optional


@dataclass
class StreeteasyRentItem:
    # define the fields for your item here like:
    # name = scrapy.Field()
    title: str
    price: str
    area: Optional[int]
    rooms_number: Optional[int]
    beds_number: Optional[int]
    baths_number: Optional[int]
    amenities: list[str]
    listing_link: str
    neighbourhood: list[str]
    days_on_market: str


@dataclass
class ApartmentDetails:
    area: Optional[int]
    rooms_number: Optional[int]
    beds_number: Optional[int]
    baths_number: Optional[int]
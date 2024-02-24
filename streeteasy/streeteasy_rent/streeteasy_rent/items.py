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
    area: int
    rooms_number: int
    beds_number: Optional[int]
    baths_number: Optional[int]
    amenities: list[str]
    listing_link: str
    neighbourhood: str

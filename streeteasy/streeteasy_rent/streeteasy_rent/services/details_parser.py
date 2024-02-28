from typing import Optional

from ..items import ApartmentDetails


class DetailsParser:
    def parse_details(self, items: list[str]) -> ApartmentDetails:
        area = self.find_area(items)
        rooms = self.find_rooms_number(items)
        beds = self.find_beds_number(items)
        baths = self.find_baths_number(items)

        details = ApartmentDetails(
            area=area,
            rooms_number=rooms,
            beds_number=beds,
            baths_number=baths
        )

        return details

    def find_area(self, items: list[str]) -> Optional[int]:
        return self.find_by_text(items, 'ft')

    def find_rooms_number(self, items: list[str]) -> Optional[int]:
        after_process = lambda x: x.replace('+', '')
        
        return self.find_by_text(items, 'room', after_process) 

    def find_beds_number(self, items: list[str]) -> Optional[int]:
        return self.find_by_text(items, 'bed') 


    def find_baths_number(self, items: list[str]) -> Optional[int]:
        return self.find_by_text(items, 'bath')
    
    def find_by_text(self, items: list[str], text: str, after_process: callable = None) -> int:
        items = list(filter(lambda item: text in item, items))
        if len(items) == 0:
            return None
        
        try:            
            result = items[0].split(' ')[0]
            if after_process is not None:
                result = after_process(result)
            
            return int(result)
        
        except:
            return None
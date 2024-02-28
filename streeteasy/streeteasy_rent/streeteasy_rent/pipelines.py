# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from .services.kafka_producer import StreeteasyRentProducer


class StreeteasyRentPipeline:
    producer = StreeteasyRentProducer()
    def process_item(self, item, spider):
        self.producer.send_rent(item)
        return item
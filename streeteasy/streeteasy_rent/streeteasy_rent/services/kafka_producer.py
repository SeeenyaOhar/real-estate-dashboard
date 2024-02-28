import io
import os
import avro
from kafka import KafkaProducer
from avro.io import DatumWriter
from avro.io import BinaryEncoder
import logging
from dataclasses import asdict

from ..items import StreeteasyRentItem

DEFAULT_PRODUCER_CONF = {
    'bootstrap_servers': os.environ.get('APP_KAFKA_BOOTSTRAP', 'localhost:9092')
}

class StreeteasyRentProducer:
    KAFKA_TOPIC = 'streeteasy_rent'
    
    def __init__(self, 
                 producer_conf=DEFAULT_PRODUCER_CONF, 
                 rent_schema='/mnt/e/code/real-estate-dashboard/streeteasy/streeteasy_rent/streeteasy_rent/services/streeteasy_rent.avsc'):
        self._producer = KafkaProducer(**producer_conf)
        self._schema = avro.schema.parse(open(rent_schema, "rb").read())
        self._writer = DatumWriter(self._schema) 
      
    def send_rent(self, rent: StreeteasyRentItem):
        bytes_writer = io.BytesIO()
        encoder = BinaryEncoder(bytes_writer)
        self._writer.write(asdict(rent), encoder)
        data_bytes = bytes_writer.getvalue()
        self._producer.send(topic=self.KAFKA_TOPIC, value=data_bytes)
        logging.info(f"kafka message, rent={rent.title}")
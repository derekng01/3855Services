import connexion
from connexion import NoContent
import json
import requests
from flask_cors import CORS, cross_origin

from datetime import datetime

import yaml
import logging
import logging.config
from pykafka import KafkaClient
from pykafka.common import OffsetType

# loading yaml config
with open('./app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

# loading logs config
with open('log_conf.yaml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')


def get_reader_book(index):
    hostname = "{}:{}".format(app_config["events"]["hostname"], app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[app_config["events"]["topic"]]

    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=100)

    logger.info("Retrieving books at index {}".format(index))

    count = 0
    for msg in consumer:
        msg_str = msg.value.decode("utf-8")
        msg = json.loads(msg_str)

        payload = msg["payload"]

        # Find the event at the index you want and
        # return code 200
        # i.e., return event, 200
        if msg["type"] == "add_reader_book":
            if count == index:
                return payload, 200

            count += 1

    logger.error("Could not find books at index {}".format(index))
    return {"message": "Not Found"}, 404

def get_reader_user(index):
    hostname = "{}:{}".format(app_config["events"]["hostname"], app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[app_config["events"]["topic"]]

    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=100)

    logger.info("Retrieving users at index {}".format(index))
    count = 0
    print(consumer)
    for msg in consumer:
        msg_str = msg.value.decode("utf-8")
        msg = json.loads(msg_str)

        payload = msg["payload"]

        # Find the event at the index you want and
        # return code 200
        # i.e., return event, 200
        if msg["type"] == "add_reader_user":
            if count == index:
                return payload, 200

            count += 1

    logger.error("Could not find readers at index {}".format(index))
    return {"message": "Not Found"}, 404

app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api('openapi.yaml', base_path='/', strict_validation=True, validate_responses=True)
app.add_api('lab7_api.yaml', base_path='/', strict_validation=True, validate_responses=True)

if __name__ == '__main__':
    app.run(port=8110)

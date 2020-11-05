import connexion
from connexion import NoContent
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from book_object import Book
from reader_object import Reader
from pykafka import KafkaClient
import json
from pykafka.common import OffsetType
from threading import Thread

import yaml
import logging.config

now = datetime.datetime.now()

with open('app_conf.yml','r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yaml','r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)


DB_ENGINE = create_engine('mysql+pymysql://{}:{}@{}:{}/{}'.format(
    app_config['datastore']['user'], app_config['datastore']['password'], app_config['datastore']['hostname'], app_config['datastore']['port'], app_config['datastore']['db']))
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

cloud_log ="Connected to: {} on port: {} " .format(
    app_config['datastore']['hostname'], app_config['datastore']['port'])

logger = logging.getLogger('basicLogger')
HOSTNAME = "{}:{}".format(app_config["events"]["hostname"], app_config["events"]["port"])
TOPIC = app_config["events"]["topic"]

def get_reader_book(timestamp):
    """get readers book"""
    session = DB_SESSION()

    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    results_list =[]
    books = session.query(Book).filter(Book.date_created >= timestamp_datetime)

    for book in books:
        results_list.append(book.to_dict())
    logger.info(cloud_log)
    logger.info('Query for Books added after {} returns {} results.'.format(timestamp,len(results_list)))
    return results_list, 200


def get_reader_user(timestamp):
    session = DB_SESSION()

    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    results_list = []
    readers = session.query(Reader).filter(Reader.date_created >= timestamp_datetime)

    for peoples in readers:
        results_list.append(peoples.to_dict())

    logger.info(cloud_log)
    logger.info('Query for Books added after {} returns {} results.'.format(timestamp, len(results_list)))
    return results_list, 200


def add_reader_book(body):
    """ add readers book"""
    session = DB_SESSION()
    bk = Book(body['title'],
              body['author'],
              body['publisher'],
              body['genre'],
              body['isbn_10'],
              body['isbn_13'],
              body['reader_rating'],
              body['reader_id']
              )

    session.add(bk)
    session.commit()
    session.close()

    logger.info(cloud_log)
    logger.info('Stored event add_reader_book request with a unique id of '+body['reader_id'])

    return NoContent, 201


def add_reader_user(body):
    session = DB_SESSION()

    rd = Reader(
                body['name'],
                body['reader_id'])

    session.add(rd)
    session.commit()
    logger.info(cloud_log)
    logger.info('Stored event add_reader_book request with a unique id of '+body['reader_id'])

    return NoContent, 201




def process_messages():
    """ Process event messages """
    client = KafkaClient(hosts=HOSTNAME)
    topic = client.topics[TOPIC]

    # Create a consume on a consumer group, that only reads new messages
    # (uncommitted messages) when the service re-starts (i.e., it doesn't
    # read all the old messages from the history in the message queue).
    consumer = topic.get_simple_consumer(consumer_group='event_group',
                                         reset_offset_on_start=False,
                                         auto_offset_reset=OffsetType.LATEST)
    # This is blocking - it will wait for a new message

    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info("Message: {}".format(msg))
        payload = msg["payload"]
        #if datetime.datetime.strptime(msg["datetime"],"%Y-%m-%dT%H:%M:%S") > now:
        print(payload)
        if msg["type"] == "add_reader_book":  # Change this to your event type
                # Store the event1 (i.e., the payload) to the DB
            add_reader_book(payload)
        elif msg["type"] == "add_reader_user":  # Change this to your event type
                # Store the event2 (i.e., the payload) to the DB
            add_reader_user(payload)
    # Commit the new message as being read
        consumer.commit_offsets()



app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("derekng_lab1.yaml", base_path='/', strict_validation=True, validate_responses=True)



if __name__=="__main__":
    t1=Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090, debug=True)

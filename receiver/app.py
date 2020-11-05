import connexion
from connexion import NoContent
import requests
import json
import yaml
import logging.config
import datetime
from pykafka import KafkaClient



with open('app_conf.yaml','r') as f:
    app_config = yaml.safe_load(f.read())

with open('log_conf.yaml','r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')
MAX_EVENTS = 10
EVENTS_LOG = "events.json"
BASE_URL = "http://localhost:8090/orders/"
HOSTNAME = "{}:{}".format(app_config["events"]["hostname"], app_config["events"]["port"])
TOPIC = app_config["events"]["topic"]


def add_reader_book(body):
    # logger.info('Received event add_reader_book request with a unique id of '+ body['reader_id'])
    # post_add_reader_book = requests.post(app_config['eventstore1']['url'], json=body)
    # logger.info('Returned event add_bug_report response '+body['reader_id']+' with status '+ str(post_add_reader_book))
    # return NoContent, post_add_reader_book.status_code
    #print(body)
    #return 201
    logger.info('Received event add_reader_book request with a unique id of '+ body['reader_id'])
    client=KafkaClient(hosts=HOSTNAME)
    topic = client.topics[TOPIC]
    producer = topic.get_sync_producer()
    msg = {"type": "add_reader_book",
           "datetime":
               datetime.datetime.now().strftime(
                   "%Y-%m-%dT%H:%M:%S"),
           "payload": body}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    logger.info("Processed event book_add request with a unique id of {}".format(body["reader_id"]))
    return NoContent, 201



def add_reader_user(body):

    # logger.info('Received event add_reader_book request with a unique id of '+ body['reader_id'])
    # post_add_reader_user = requests.post(app_config['eventstore2']['url'], json=body)
    # logger.info('Returned event add_bug_report response '+body['reader_id']+' with status '+ str(post_add_reader_user))
    # return NoContent, post_add_reader_user.status_code
    #print(body)
    #return 201

    logger.info('Received event add_reader_book request with a id of ' + body['reader_id'])
    client = KafkaClient(hosts=HOSTNAME)
    topic = client.topics[TOPIC]
    producer = topic.get_sync_producer()
    msg = {"type": "add_reader_user",
           "datetime":
               datetime.datetime.now().strftime(
                   "%Y-%m-%dT%H:%M:%S"),
           "payload": body}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    logger.info("Processed event add_reader_user request with a id of {}".format(body["reader_id"]))
    return NoContent, 201

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("derekng_lab1.yaml", base_path='/', strict_validation=True, validate_responses=True)


if __name__=="__main__":
        app.run(port=8080, debug=True)

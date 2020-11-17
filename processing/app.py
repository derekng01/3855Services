import connexion
import json
import requests
from apscheduler.schedulers.background import BackgroundScheduler

from datetime import datetime
from flask_cors import CORS, cross_origin

import yaml
import logging.config
import os

if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    app_conf_file = "/config/app_conf.yml"
    log_conf_file = "/config/log_conf.yaml"
else:
    print("In Dev Environment")
    app_conf_file = "app_conf.yml"
    log_conf_file = "log_conf.yaml"

with open (app_conf_file, 'r') as f:
    app_config=yaml.safe_load(f.read())

with open(log_conf_file,'r') as f:
    log_config=yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')
logger.info("App Conf File: %s" % app_conf_file)
logger.info("Log Conf File: %s" % log_conf_file)



def get_stats():
    """get readers book"""
    logger.info('GET request stats has been initiated')

    try:
        with open(app_config['datastore']['filename'], 'r') as f:
            data_stats_read = f.read()

            # object conversion
            data_stats = json.loads(data_stats_read)

            show_stats = {
                "genre_reader_pref": data_stats["genre_reader_pref"],
                "avg_books_reader": data_stats["avg_books_reader"],
                "num_readers": data_stats["num_readers"],
                "num_books": data_stats["num_books"]
            }

            logger.debug(
                'Get stats with genre_reader_pref: {}, max_books_read: {}, num_readers: {}, num_books: {}'.format(
                    show_stats['genre_reader_pref'],
                    show_stats['avg_books_reader'],
                    show_stats['num_readers'],
                    show_stats['num_books']
                ))

            logger.info('GET request stats has been completed')

            return show_stats, 200

    except FileNotFoundError:
        error_message = 'Statistics do not exist with status code 404'
        logger.error(error_message)

        return {"message": error_message}, 404



def populate_stats():
#     """Update stats on a regular basis"""
    logger.info('Regular processing for stats has started')

    current_time= datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

    try:
        with open(app_config['datastore']['filename'], 'r') as f:
            data_read = f.read()
            stats_info = json.loads(data_read)

    except FileNotFoundError:
        with open(app_config['datastore']['filename'], 'w') as f:
            json_template = {
                "genre_reader_pref": 0,

                "avg_books_reader": 0,

                "num_readers": 0,

                "num_books": 0,

                "last_updated": "2000-01-01T00:00:00Z"

            }
            f.write(json.dumps(json_template, indent=4))

        with open(app_config['datastore']['filename'], 'r') as f:
            data_read = f.read()

            stats_info = json.loads(data_read)

    timestamp = {"timestamp": stats_info['last_updated']}

    get_reader_book = requests.get('{}/readers/adding_book'.format(app_config['eventstore']['url']),params=timestamp)
    get_reader_user = requests.get('{}/readers/user'.format(app_config['eventstore']['url']),params=timestamp)



    #logs for all all gets through this api
    if (get_reader_book.status_code != 200):
        logger.error('Could not receive events GET list with status code {}'.format(
            get_reader_book.status_code))
    else:
        logger.info('{} events received from GET request with status code {}'.format(
            len(get_reader_book.json()), get_reader_book.status_code))

        stats_info["num_books"] = stats_info["num_books"] + len(
                get_reader_book.json())

        #Total number of books
        stats_info["num_books"] = stats_info["num_books"] + len(get_reader_book.json())
        #Top genre readers pref
        stats_info["genre_reader_pref"] = stats_info["genre_reader_pref"]  + int(len(get_reader_book.json())) / 2


        #avg books read
        stats_info["avg_books_reader"] = stats_info["avg_books_reader"] + (len(get_reader_book.json())) #logic incorrect but will do for now


    if (get_reader_user.status_code != 200):
        logger.error('Could not receive events GET list with status code {}'.format(
                get_reader_user.status_code))
    else:
        logger.info('{} events received from GET request with status code {}'.format(
                len(get_reader_user.json()),
                get_reader_user.status_code))

        #Total number of readers
        stats_info["num_readers"] = stats_info["num_readers"] + len(get_reader_user.json())


    with open(app_config['datastore']['filename'], 'w') as f:
        stats_info['last_updated'] = current_time
        f.write(json.dumps(stats_info, indent=4))

    logger.debug("Data store updated with num_books: {}, genre_reader_pref: {}, avg_books_reader: {}, num_readers: {}".format(
        stats_info["num_books"],
        stats_info["genre_reader_pref"],
        stats_info["avg_books_reader"],
        stats_info["num_readers"],
        stats_info["last_updated"]
        ))

    logger.info('Period processing for stats has ended')

def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats,
                  'interval',
                  seconds=app_config['scheduler']['period_sec'])
    sched.start()


app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("stats.yaml", base_path='/', strict_validation=True, validate_responses=True)



if __name__=="__main__":
    init_scheduler()

    app.run(port=8100, debug=True)

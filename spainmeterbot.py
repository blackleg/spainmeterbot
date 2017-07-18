import logging
import argparse


from twitter import Api
from reescraper import IberianPeninsula, BalearicIslands, CanaryIslands
from arrow import get
from dotenv import load_dotenv, find_dotenv
from os import environ

# Load environment variables
load_dotenv(find_dotenv())

logger = logging.getLogger('spainmeter')
logger.setLevel(logging.DEBUG)

# Create file handler which logs even debug messages
fh = logging.FileHandler('spainmeter.log')
fh.setLevel(logging.DEBUG)
# Create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# Create formatter and add it to the handlers
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(file_formatter)
# Add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


parser = argparse.ArgumentParser()
parser.add_argument("--demand", help="increase output verbosity", action="store_true")


def demand():
    logger.debug("Demand Tweet")
    logger.debug("- Getting Peninsula Data")
    peninsula = IberianPeninsula().get()
    if not peninsula:
        logger.error("!! No Peninsula response ¡¡")
        quit()

    date = get(peninsula.timestamp).to('Europe/Madrid')
    day = date.format('DD', 'es_ES')
    month = date.format('MMMM', 'es_ES')
    time = date.format('HH:mm', 'es_ES')

    peninsula_tweet = "Demanda electricidad España el {0} de {1} a las {2}, Península: {3} MW".format(day, month, time, peninsula.demand)

    logger.debug("- Getting Balearic Islands Data")
    balearic = BalearicIslands().get()
    if not balearic:
        logger.debug("!! No Balearic Islands response ¡¡")
        balearic_tweet = ''
    else:
        balearic_date = get(balearic.timestamp).to('Europe/Madrid')
        time = balearic_date.format('HH:mm', 'es_ES')
        balearic_tweet = ', Baleares ({0}): {1} MW'.format(time, balearic.demand)

    logger.debug("- Getting Canary Islands Data")
    canary = CanaryIslands().get()
    if not canary:
        logger.error("!! No Canary Islands response ¡¡")
        canary_tweet = ''
    else:
        canary_date = get(canary.timestamp).to('Europe/Madrid')
        time = canary_date.format('HH:mm', 'es_ES')
        canary_tweet = ', Canarias ({0}): {1} MW'.format(time, canary.demand)

    tweet = peninsula_tweet + balearic_tweet + canary_tweet
    logger.debug("- Generated Tweet: " + tweet)

    enabled = environ.get("ENABLED", 'False')
    if enabled != 'True':
        logger.error("!! Send tweet disabled ¡¡")
    else:
        api = Api(consumer_key=environ.get("CONSUMER_KEY"),
                consumer_secret=environ.get("CONSUMER_SECRET"),
                access_token_key=environ.get("ACCESS_KEY"),
                access_token_secret=environ.get("ACCESS_SECRET"))
        api.PostUpdate(tweet)
        logger.debug("- Tweet Sended")


args = parser.parse_args()
if args.demand:
    demand()





import logging
from twitter import Api
from reescraper import IberianPeninsula, BalearicIslands, CanaryIslands
from arrow import get
from dotenv import load_dotenv, find_dotenv
from os import environ

load_dotenv(find_dotenv())

logger = logging.getLogger('spainmeter')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('spainmeter.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

logger.debug("=> Getting Peninsula Data")
peninsula = IberianPeninsula().get()
if not peninsula:
    logger.error("- !! No Peninsula response ¡¡")
    quit()

date = get(peninsula.timestamp).to('Europe/Madrid')
day = date.format('DD', 'es_ES')
month = date.format('MMMM', 'es_ES')
time = date.format('HH:mm', 'es_ES')

peninsula_tweet = "Demanda electricidad España el {0} de {1} a las {2}, Península: {3} MW".format(day, month, time, peninsula.demand)

logger.debug("=> Getting Balearic Islands Data")
balearic = BalearicIslands().get()
if not balearic:
    logger.debug("- !! No Balearic Islands response ¡¡")
    balearic_tweet = ''
else:
    balearic_date = get(balearic.timestamp).to('Europe/Madrid')
    time = balearic_date.format('HH:mm', 'es_ES')
    balearic_tweet = ', Baleares ({0}): {1} MW'.format(time, balearic.demand)

logger.debug("=> Getting Canary Islands Data")
canary = CanaryIslands().get()
if not canary:
    logger.error("- !! No Canary Islands response ¡¡")
    canary_tweet = ''
else:
    canary_date = get(canary.timestamp).to('Europe/Madrid')
    time = canary_date.format('HH:mm', 'es_ES')
    canary_tweet = ', Canarias ({0}): {1} MW'.format(time, canary.demand)


tweet = peninsula_tweet + balearic_tweet + canary_tweet
logger.debug("=> Generated Tweet: " + tweet)

enabled = environ.get("ENABLED", 'False')
if enabled != 'True':
    logger.error("- !! Send tweet disabled ¡¡")
else:
    logger.debug("=> Sending tweet")
    api = Api(consumer_key=environ.get("CONSUMER_KEY"),
              consumer_secret=environ.get("CONSUMER_SECRET"),
              access_token_key=environ.get("ACCESS_KEY"),
              access_token_secret=environ.get("ACCESS_SECRET"))
    api.PostUpdate(tweet)





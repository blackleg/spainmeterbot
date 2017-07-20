import logging

from twitter import Api
from reescraper import IberianPeninsula, BalearicIslands, CanaryIslands
from arrow import get
from dotenv import load_dotenv, find_dotenv
from os import environ

# Load environment variables
load_dotenv(find_dotenv())

logger = logging.getLogger('spainmeter_demand')
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

logger.debug("Production Tweet")
peninsula = IberianPeninsula().get()
if not peninsula:
    logger.error("!! No Peninsula response ¡¡")
    quit()

datetime = get(peninsula.timestamp).to('Europe/Madrid')
date = datetime.format('DD-MM-YY', 'es_ES')
time = datetime.format('HH:mm', 'es_ES')

nuclear = round((peninsula.nuclear/peninsula.production())*100, 2)
fosil = round(((peninsula.gas + peninsula.combined + peninsula.carbon) /peninsula.production())*100, 2)
renewable = round(((peninsula.wind + peninsula.hydraulic + peninsula.solar) /peninsula.production())*100, 2)
other = round((peninsula.other/peninsula.production())*100, 2)


tweet = "Generación #electricidad #España (Península), {0} {1}, #Nuclear: {2}%, #Fósiles: {3}%, #Renovables: {4}%, Otras: {5}%".format(date, time, nuclear, fosil, renewable, other)

logger.debug("- Generated Tweet: " + tweet + " Size: " + str(len(tweet)))

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
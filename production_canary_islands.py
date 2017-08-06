import logging

from twitter import Api
from reescraper import CanaryIslands
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
canaryislands = CanaryIslands().get()
if not canaryislands:
    logger.error("!! No Canary Islands response ¡¡")
    quit()

datetime = get(canaryislands.timestamp).to('Europe/Madrid')
date = datetime.format('DD-MM-YY', 'es_ES')
time = datetime.format('HH:mm', 'es_ES')

print(canaryislands)

fosil = round(((canaryislands.gas + canaryislands.combined + canaryislands.carbon + canaryislands.fuel) / canaryislands.production()) * 100, 2)
renewable = round(((canaryislands.wind + canaryislands.hydraulic + canaryislands.solar) / canaryislands.production()) * 100, 2)
other = round((canaryislands.unknown() / canaryislands.production()) * 100, 2)


tweet = "Generación #electricidad #Canarias, {0} {1}, #Fósiles: {2}%, #Renovables: {3}%, Otras: {4}%".format(date, time, fosil, renewable, other)

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

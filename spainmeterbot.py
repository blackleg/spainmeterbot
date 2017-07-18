#import twitter
#import reescraper
#import arrow
from dotenv import load_dotenv, find_dotenv
#from os import environ
load_dotenv(find_dotenv())

#print(environ.get("ENABLED"))

#response = reescraper.IberianPeninsula().get()
#print(response)

#date = arrow.get(response.timestamp).to('Europe/Madrid')
#day = date.format('DD', 'es_ES')
#month = date.format('MMMM', 'es_ES')
#time = date.format('HH:mm', 'es_ES')


#tweet = "Demanda península el {0} de {1} a las {2}: {3} MW".format(day, month, time, response.demand)

#api = twitter.Api(consumer_key='', consumer_secret='', access_token_key='', access_token_secret='')

#status = api.PostUpdate(tweet)
#print(status.text)




import tweepy
import time
import json
import requests
import string
from account_keys import *

# Twitter API Config
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
FILE_NAME = 'last_seen_id.txt'

# Currency Exchange Config
USD = ["usd", "dollar", "dollars", "dólar", "dolar", "dólares", "dolares"]
EUR = ["eur", "euro", "euros"]
GBP = ["gbp", "libra", "libras", "esterlina", "esterlinas", "pound", "sterling"]
JPY = ["jpy", "jpn", "yen", "yens", "yene", "yenes", "ien", "iens", "iene", "ienes"]
ARS = ["ars", "peso", "pesos", "argentina", "argentino", "argentinos", "convertible"]
REQUEST_URL = "https://economia.awesomeapi.com.br/json/"

# Pokémon Config
pokedex = open('pokedex.json', encoding="utf8")
pokemon_list = json.load(pokedex)

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweets():
    print('retrieving and replying to tweets...')
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        current_currency = ""
        tweet_text = mention.full_text.lower().split()
        for tweet_word in tweet_text:
            table_punctuation = str.maketrans(dict.fromkeys(string.punctuation))
            word = tweet_word.translate(table_punctuation)      
            print(word)
            if word in USD:
                current_currency = "USD"
                break
            if word in EUR:
                current_currency = "EUR"
                break
            if word in GBP:
                current_currency = "GBP"
                break
            if word in JPY:
                current_currency = "JPY"
                break
            if word in ARS:
                current_currency = "ARS"
                break
        if current_currency != "":
            currency_info = request_value(current_currency)
            currency_value = "{:.2f}".format(float(currency_info['ask']))
            pokemon_number = currency_value.replace('.','')
            pokemon_name = pokemon_list[int(pokemon_number)-1]['name']['english']
            pokemon_image_path = 'pokemon_images/{}.png'.format(pokemon_number)
            post_message = "@{0} A cotação atual de 1 {1} é: R${2}!\n\nPokémon #{3} - {4}".format(mention.user.screen_name, currency_info['name'], currency_value.replace('.',','), pokemon_number, pokemon_name)
            api.update_with_media(
                filename = pokemon_image_path,
                status = post_message,
                in_reply_to_status_id = mention.id
            )

def request_value(currency):
    request = requests.get("{0}{1}".format(REQUEST_URL, currency))
    exchange_json = json.loads(request.content)
    return exchange_json[0]

while True:
    reply_to_tweets()
    time.sleep(15)
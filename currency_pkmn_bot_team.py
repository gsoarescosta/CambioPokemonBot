# -*- coding: utf-8 -*-
import tweepy
import time
import json
import requests
import string
import random
from itertools import islice

# For Running Bot
from account_keys import *

# Twitter API Config
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# Currency Exchange Config
ALL_CURRENCY = ["USD", "CAD", "AUD", "EUR", "GBP", "ARS", "JPY", "CHF", "CNY", "ILS"]
REQUEST_URL = "https://economia.awesomeapi.com.br/json/"
# USD (Dólar Comercial)
# CAD (Dólar Canadense)
# AUD (Dólar Australiano)
# EUR (Euro)
# GBP (Libra Esterlina)
# ARS (Peso Argentino)
# JPY (Iene Japonês)
# CHF (Franco Suíço)
# CNY (Yuan Chinês)
# ILS (Novo Shekel Israelense)

# Pokémon Config
pokedex = open('pokedex.json', encoding="utf8")
pokemon_list = json.load(pokedex)

def update_team():
    post_message = "O time atual do @cambiopokemon é:\n\n"
    pokemon_images_list = []
    random.shuffle(ALL_CURRENCY)
    for currency in islice(ALL_CURRENCY, 4):
        currency_info = request_value(currency)
        value = float(currency_info['ask'])
        if value >= 1:            
            currency_value = "{:.2f}".format(value)
            pokemon_number = currency_value.replace('.','')
        else:
            currency_value = "{:.3f}".format(value)
            pokemon_number = currency_value[1:].replace('.','')
        pokemon_name = pokemon_list[int(pokemon_number)-1]['name']['english']
        pokemon_images_list.append('pokemon_images/{}.png'.format(pokemon_number))
        post_message = post_message + "#{2} - {3} ({0}: R${1})\n".format(currency_info['name'], currency_value.replace('.',','), pokemon_number, pokemon_name)
        print("{1} - {0}".format(currency_info['code'],pokemon_name))
    media_ids = []
    for pokemon_image in pokemon_images_list:
        res = api.media_upload(pokemon_image)
        media_ids.append(res.media_id)
    api.update_status(status = post_message, media_ids = media_ids)
    print("- Tweet Enviado -")

def request_value(currency):
    request = requests.get("{0}{1}".format(REQUEST_URL, currency))
    exchange_json = json.loads(request.content.decode('utf-8'))
    return exchange_json[0]
    
while True:
    try:
        update_team()
    except:
        print("- Oops! Exception -")
    time.sleep(3600)
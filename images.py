import io
import os
import sys

import requests
import time
from bs4 import BeautifulSoup
import PIL.Image as Image

PNG_EXTENSION = '.png'
JPG_EXTENSION = '.jpg'
LARGE = '/large'
MEDIUM = '/medium'
SMALL = '/small'


def create_directories(path):
    if not os.path.exists(path + SMALL):
        os.makedirs(path + SMALL)
    if not os.path.exists(path + MEDIUM):
        os.makedirs(path + MEDIUM)
    if not os.path.exists(path + LARGE):
        os.makedirs(path + LARGE)


def scraping():
    path = sys.argv[1:][0]
    create_directories(path)
    pokemon_list = get_path()[:151]
    list_size = len(pokemon_list)
    for pokemon in pokemon_list:
        list_size -= 1
        get_pokemon_small_images(pokemon, path)
        get_pokemon_medium_images(pokemon, path)
        get_pokemon_large_images(pokemon, path)
        time.sleep(1)


def get_path():
    page = requests.get("https://pokemondb.net/pokedex/national")
    soup = BeautifulSoup(page.content, 'html.parser')
    names_tags = soup.find_all(class_='ent-name')
    names_path = [name.get('href') for name in names_tags]
    names = [name.replace('/pokedex/', '') for name in names_path]
    return names


def get_pokemon_small_images(pokemon, path):
    page = requests.get('https://img.pokemondb.net/sprites/bank/normal/' + pokemon + PNG_EXTENSION)
    if page.status_code == 200:
        image = Image.open(io.BytesIO(bytearray(page.content)))
        image.save(path + SMALL + '/' + pokemon + PNG_EXTENSION)
        print('Saving small image for: ' + pokemon)
    else:
        print('===>> error saving small image for: ' + pokemon)


def get_pokemon_medium_images(pokemon, path):
    page = requests.get('https://img.pokemondb.net/artwork/' + pokemon + JPG_EXTENSION)
    if page.status_code == 200:
        image = Image.open(io.BytesIO(bytearray(page.content)))
        image.save(path + MEDIUM + '/' + pokemon + JPG_EXTENSION)
        print('Saving medium image for: ' + pokemon)
    else:
        print('===>> error saving medium image for: ' + pokemon)


def get_pokemon_large_images(pokemon, path):
    page = requests.get('https://img.pokemondb.net/artwork/large/' + pokemon + JPG_EXTENSION)
    if page.status_code == 200:
        image = Image.open(io.BytesIO(bytearray(page.content)))
        image.save(path + LARGE + '/' + pokemon + JPG_EXTENSION)
        print('Saving large image for: ' + pokemon)
    else:
        print('===>> error saving large image for: ' + pokemon)


if __name__ == '__main__':
    scraping()

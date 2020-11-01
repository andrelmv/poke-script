import requests
import time
from bs4 import BeautifulSoup


def scraping():
    file = open("pokemon.json", "w")
    pokemon_path_list = get_path()[:151]
    list_size = len(pokemon_path_list)
    build_start(file)
    for pokemon_path in pokemon_path_list:
        list_size -= 1
        pokemon_page = get_pokemon(pokemon_path)
        pokemon_table = get_pokemon_table(pokemon_page)
        pokemon_name = get_pokemon_name(pokemon_page)
        build_object(pokemon_table, pokemon_name, list_size, file)
        time.sleep(10)

    build_end(file)
    file.close()
    f = open("pokemon.json", "r")
    print(f.read())


def build_object(pokemon_table, pokemon_name, list_size, file):
    build_object_start(file)
    build_name(pokemon_name, file)
    build_type(pokemon_table, file)
    build_ability(pokemon_table, file)
    build_height(pokemon_table, file)
    build_weight(pokemon_table, file)
    build_object_end(list_size, file)


def build_start(file):
    file.write("[")


def build_end(file):
    file.write("\n]")


def build_object_start(file):
    file.write("\n    {\n")


def build_object_end(list_size, file):
    end = "    }"
    if list_size > 0:
        end = end + ","
    file.write(end)


def build_name(pokemon_name, file):
    file.write("        \"name\": " + "\"" + pokemon_name + "\",\n")


def build_type(pokemon_table, file):
    result = "        \"type\": [\n"
    pokemon_types = pokemon_table[1].find('td').find_all('a')
    list_size = len(pokemon_types)
    i = 0
    for pokemon_type in pokemon_types:
        result = result + "            \"" + pokemon_type.get_text().upper() + "\""
        if (list_size - 1) > i:
            result = result + ",\n"
        i += 1
    result = result + "\n        ],\n"
    file.write(result)


def build_ability(pokemon_table, file):
    result = "        \"ability\": [\n"
    pokemon_abilities = pokemon_table[5].find('td').find_all('a')
    list_size = len(pokemon_abilities)
    i = 0
    for pokemon_ability in pokemon_abilities:
        result = result + "            \"" + pokemon_ability.get_text() + "\""
        if (list_size - 1) > i:
            result = result + ",\n"
        i += 1
    result = result + "\n        ],\n"
    file.write(result)


def build_height(pokemon_table, file):
    pokemon_height = "        \"height\": "
    pokemon_height = pokemon_height + pokemon_table[3].find('td').get_text().split()[0] + ",\n"
    file.write(pokemon_height)


def build_weight(pokemon_table, file):
    pokemon_weight = "        \"weight\": "
    pokemon_weight = pokemon_weight + pokemon_table[4].find('td').get_text().split()[0] + "\n"
    file.write(pokemon_weight)


def get_path():
    page = requests.get("https://pokemondb.net/pokedex/national")
    soup = BeautifulSoup(page.content, 'html.parser')
    names_tags = soup.find_all(class_='ent-name')
    names = [name.get('href') for name in names_tags]
    return names


def get_pokemon(pokemon):
    page = requests.get("https://pokemondb.net/" + pokemon)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def get_pokemon_table(pokemon_page):
    table = pokemon_page.find(class_='vitals-table')
    return table.find_all('tr')


def get_pokemon_name(pokemon_page):
    return pokemon_page.find('h1').get_text()


if __name__ == '__main__':
    scraping()

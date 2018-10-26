import requests
from bs4 import BeautifulSoup
from pprint import pprint
import json

class Hero:
  def __init__(self, hero_data):
    self.name = hero_data['name']
    self.epithet = hero_data['epithet']
    self.weapon_type = hero_data['weapon_type']
    self.movement_type = hero_data['movement_type']
    self.stats1 = hero_data['stats1']
    self.release_date = hero_data['release_date']

  def getBST(self):
    print('will do later lol')

  def get_info(self):
    print('Name:', self.name)
    print('Epithet:', self.epithet)
    print('Weapon Type:', self.weapon_type)
    print('Movement Type:', self.movement_type)
    print('Lv 1 Stats:')
    pprint(self.stats1)
    print('Release Date:', self.release_date)

url = 'https://feheroes.gamepedia.com/Hero_list'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
table_rows = soup.find('table').findAll('tr')

list = []
for row in table_rows:
    route = row.find('a', href=True)
    list.append(f'https://feheroes.gamepedia.com{route["href"]}')

number_of_heroes = len(list)
print('Heroes Found:', number_of_heroes)
for link in list:
    print(link)


def get_hero_info(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    result = soup.find("table", {"id": "boxshadow"}).findAll('span')

    name = result[0].text
    epithet = result[1].text
    weapon_type = result[6].text
    movement_type = result[8].text
    release_date = soup.find("table", {"id": "boxshadow"}).find('time').text
    print(
        '\nName:', name, ',', epithet,
        '\nWeapon Type:', weapon_type,
        '\nMovement Type:', movement_type,
        '\nRelease Date:', release_date,
        '\n'
    )
    return {'name': name, 'epitheth': epithet, 'weapon_type': weapon_type, 'movement_type': movement_type, 'release_date': release_date}


def get_hero_stats(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    result = soup.findAll("table", {"class": "wikitable default"})

    def get_stats(level):
        if level == 0:
            print('Level 1 stats:')
        if level == 1:
            print('Level 40 stats:')

        table_rows = result[level].findAll('tr')
        stats = {}
        for row in range(1, len(table_rows)):
            rarity = table_rows[row].findAll('td')

            hero_rarity = rarity[0].text
            hero_hp = rarity[1].text
            hero_atk = rarity[2].text
            hero_spd = rarity[3].text
            hero_def = rarity[4].text
            hero_res = rarity[5].text

            print(
                'Rarity', hero_rarity, '⭐' * int(hero_rarity),
                '\nHp', hero_hp,
                '\nAtk', hero_atk,
                '\nSpd', hero_spd,
                '\nDef', hero_def,
                '\nRes', hero_res,
                '\n'
            )

            stats['Rarity'] = hero_rarity
            stats['HP'] = hero_hp
            stats['Atk'] = hero_atk
            stats['Spd'] = hero_spd
            stats['Def'] = hero_def
            stats['Res'] = hero_res

        return stats

    response = {
        'level_one': get_stats(0),
        'level_fourty': get_stats(1)
    }
    return response


from pymongo import MongoClient
import os
dbuser = os.environ['DBUSER']
dbpassword = os.environ['DBPASSWORD']
client = MongoClient(f'mongodb://{dbuser}:{dbpassword}@ds117431.mlab.com:17431/feh')
db = client.feh
heroes = db.heroes

for hero in range(0, number_of_heroes):
    hero_info = get_hero_info(list[hero])
    hero_stats = get_hero_stats(list[hero])

    hero_data = {}
    hero_data['name'] = hero_info['name']
    hero_data['epithet'] = hero_info['epithet']
    hero_data['weapon_type'] = hero_info['weapon_type']
    hero_data['movement_type'] = hero_info['movement_type']
    hero_data['release_date'] = hero_info['release_date']
    hero_data['stats1'] = hero_stats['level_one']
    hero_data['stats40'] = hero_stats['level_fourty']

    created_hero = Hero(hero_data)
    created_hero.get_info()
    print('🦉🦉🦉')

    result = heroes.insert_one(created_hero.get_json())
    print('One post: {0}'.format(result.inserted_id))

'''
reference
https://clay-atlas.com/blog/2020/11/25/python-cn-sloved-urllib-error-urlerror/
https://itsmycode.com/python-urllib-error-httperror-http-error-403-forbidden/
https://zwindr.blogspot.com/2017/12/python-pyquery.html
https://codertw.com/%E7%A8%8B%E5%BC%8F%E8%AA%9E%E8%A8%80/360045/ 
'''
import shutil
from pyquery import PyQuery
import ssl
from urllib.request import Request, urlopen
import re
import requests
from os import path

ssl._create_default_https_context = ssl._create_unverified_context

link = 'https://pokemondb.net/pokedex/all' # pokedex

req = Request(link, headers={'User-Agent':'Mozilla/5.0'})
webpage = urlopen(req).read()
dom = PyQuery(webpage)
links = dom.find('tr')
# print(links)

pokemons_idx = []
pokemons_name = []
for idx, k in enumerate(links.items()):
    id = k.find('.infocard-cell-data').text()
    if not (id in pokemons_idx):
        pokemons_idx.append(id)
        name = k.find('.ent-name').text()
        pokemons_name.append(name)

pokemons_data = {}
# print(len(pokemons_idx))
# print(len(pokemons_name))
for i in range(len(pokemons_name)):
    pokemons_data[pokemons_idx[i]] = pokemons_name[i]
pokemons_data = {k:v for k, v in pokemons_data.items() if v}
# print(pokemons_data)


doc = PyQuery(url=link)
pokemons_ = doc.find('tr').children()
pokemons_index = pokemons_.find('.infocard-cell-data').text().split(' ')
pokemons_name = pokemons_.find('.ent-name').text().split(' ')

# print(pokemons_index, pokemons_name)

pokedex = dict(zip(pokemons_index, pokemons_name))
# print(pokedex)

# Pokedex Link
pokemons_link = 'https://pokemondb.net/pokedex/all'
# Get all info from link (html)
doc = PyQuery(url=pokemons_link)
# Get pokemons img src url
pokemons_urls = doc.find('td').find('span').children()
pokemons_img = dict()
# print(pokemons_urls)
empty_img = 'https://img.pokemondb.net/s.png' # Filter the empty img
for item in pokemons_urls:
    item = PyQuery(item)
    if not re.match(item.attr('data-src'), empty_img):
        url = item.attr('data-src')
        poke_name = str(url).split('/')[-1][:-4]
        pokemons_img[poke_name] = url
# print(pokemons_img)

# Save the img to db
folder = './PyQuery/pokemons/'
for img_url in pokemons_img.values():
    img_name = folder + str(img_url).split('/')[-1]
    if path.exists(img_name):
        print('Continuing ...')
        continue
    img_data = requests.get(url=img_url, stream=True)
    if img_data.status_code == 200:
        # Set decode_content be True, otherwise the downloaded image file's size will be zero
        img_data.raw.decode_content = True
        with open(img_name, 'wb') as f:
            shutil.copyfileobj(img_data.raw, f)
        print('Image sucessfully Downloaded: ',img_name)
    else:
        print('Image Couldn\'t be retreived')

# Regular Expression match testing
str1 = 'hello'
str2 = '   HellO  '
print(re.match(str1.lower(), str2.lower())) # Return None
print(re.match(str1.lower().strip(), str2.lower().strip())) # Return <0, 5>
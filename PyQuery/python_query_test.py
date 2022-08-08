'''
reference
https://clay-atlas.com/blog/2020/11/25/python-cn-sloved-urllib-error-urlerror/
https://itsmycode.com/python-urllib-error-httperror-http-error-403-forbidden/
https://zwindr.blogspot.com/2017/12/python-pyquery.html
https://codertw.com/%E7%A8%8B%E5%BC%8F%E8%AA%9E%E8%A8%80/360045/ 
'''
from pyquery import PyQuery
import ssl
from urllib.request import Request, urlopen

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
print(pokedex)
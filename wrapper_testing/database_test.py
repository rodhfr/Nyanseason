from nyaapy.nyaasi.nyaa import Nyaa
import anitopy
import db
from pprint import pprint
import sqlite3


# Settings
anitopy_options = {'allowed_delimiters': ' '}
keyword_user_input = "Dandadan"
torrent_group = "[SubsPlease]"

# Search for torrents
nyaasearch = Nyaa.search(keyword=keyword_user_input + torrent_group, category="1", filter="2")
n_torrent = 0


anime_dictionary = []
# Process and store each torrent's info in the database
for torrent in nyaasearch:
    if torrent_group.lower() in torrent.name.lower() and "(1080p)" in torrent.name.lower():
        #print(f"From Nyaa, Title: {torrent.name}")
        
        # Parse torrent name using anitopy
        parsed_info = anitopy.parse(torrent.name, options=anitopy_options)
        db.new_entry_database(parsed_info['anime_title'], parsed_info['episode_number'])
        anime_dictionary.append(parsed_info)
        n_torrent += 1


# Consultando e imprimindo animes
animes = db.consultar_animes()  # Chama a função para obter todos os animes
for anime in animes:  # Itera sobre a lista de animes
    print(anime)  # Imprime cada anime

#pprint(anime_dictionary)
# Check if no torrents were found
if n_torrent == 0:
    print("There is no torrent found")
else:
    print(f"Found {n_torrent} torrents")

# Closing database
sqlite3.connect('animes.db').close()

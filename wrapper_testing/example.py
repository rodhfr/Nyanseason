from nyaapy.nyaasi.nyaa import Nyaa
import json
import anitopy
import sqlite3

conn = sqlite3.connect('example.db')
cursor = conn.cursor()


# Settings
anitopy_options = {'allowed_delimiters': ' '}

keyword_user_input = "Dandadan"
torrent_group = "[Subsplease]"

arc = Nyaa.search(keyword=keyword_user_input+torrent_group, category="1", filter="2")
n_torrent = 0

anime_dictionary = []
for torrent in arc:
    if (torrent_group.lower() and "(1080p)" in torrent.name.lower()):
        print(f"Title: {torrent.name}")
        
        anitopy_options = {'allowed_delimiters': ' '}
        anime_dictionary.append(anitopy.parse(torrent.name, options=anitopy_options))
        n_torrent += 1

print()
print("now priting the json:")

with open ("database.json", "w", encoding="utf-8") as f:
    json.dump(anime_dictionary, f, indent = 4, ensure_ascii=False)

json_object = json.dumps(anime_dictionary, indent=4)
print(json_object)

if n_torrent == 0:
    print("There is no torrent found")
else: print(f"Found {n_torrent} torrents")


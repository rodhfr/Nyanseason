from nyaapy.nyaasi.nyaa import Nyaa
import anitopy
import db


# Library Settings
anitopy_options = {'allowed_delimiters': ' '}
keyword_user_input = "piece"
torrent_group = "[SubsPlease]"
anime_resolution = "(1080p)"

# Search for torrents
nyaasearch = Nyaa.search(keyword=keyword_user_input + torrent_group + anime_resolution, category="1", filter="2")
n_torrents = 0

for torrent in nyaasearch:
    # This loop searches throught the nyaa refreshed torrent name lists
    if torrent_group.lower() in torrent.name.lower():
        # Writing anime title and episode number to variables
        parsed_info = anitopy.parse(torrent.name, options=anitopy_options)
        episode_number = parsed_info.get('episode_number')
        anime_title = parsed_info.get('anime_title')
        # Check if the parsing succeded else print error
        if anime_title is not None and episode_number is not None:
            db.new_db_entry(parsed_info['anime_title'], episode_number)
            n_torrents += 1
        else:
            print(f"ERROR: Missing information for torrent: {torrent.name} - anime_title: {anime_title}, episode_number: {episode_number}")  # Error handling

print(f"SUCESS: Refreshed {n_torrents} torrents in Nyaa")





# Close Database
db.close_connection()

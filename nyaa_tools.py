from nyaapy.nyaasi.nyaa import Nyaa
import anitopy
import db
import logging


DEBUG_MODE = True
# Configure logging based on the debug mode
if DEBUG_MODE:
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
else:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Added 20:41 day 5 of november 2024
# status: Working great.
# description: Query directly from nyaa the torrent filenames using nyaapy bs4 wrapper.
def nyaasearch(usr_qry_anime_search, usr_qry_release_group = "[SubsPlease]", usr_qry_resolution = "1080p", category = "1", filter = "2"):
    composed_query = usr_qry_anime_search + " " + usr_qry_release_group + " " + usr_qry_resolution # Using composed_query its the simple string sum from the user search + user release group + user provided resolution
    try:
        return Nyaa.search(keyword=composed_query, category=category, filter=filter)
    except Exception as e:
        logging.error(f"Error searching nyaa: {e}")
        return []
    
# Added 20:44 day 5 of november 2024
# status: Working great.
# description: This function parses the torrent release name and returns anime title and episode number
def anitopy_parse(torrent_filename, anitopy_options = {'allowed_delimiters': ' '}):
    parsed_data = anitopy.parse(torrent_filename.name, anitopy_options)
    return parsed_data.get('episode_number'), parsed_data.get('anime_title')

# Added 20:41 day 5 of november 2024
# status: Working great.
# description: Composed function refreshes the database populating with new releases from nyaa. 
def refresh_nyaa(usr_qry_anime_search, usr_qry_release_group, usr_qry_resolution = "1080p", category = "1", filter = "2"):
    refreshed_count = 0
    added_to_db = 0
    present_in_db = 0

    # Querying new episodes from nyaa
    try:
        nyaadata = nyaasearch(usr_qry_anime_search, usr_qry_release_group, usr_qry_resolution, category, filter)
        for torrent_filename in nyaadata:
            anime_title, episode_number = anitopy_parse(torrent_filename)
            if anime_title is not None and episode_number is not None:
                # this db.new_db_entry fn returns 1 if added title
                new_added_to_db, new_present_in_db = db.new_db_entry(anime_title, episode_number)
                added_to_db += new_added_to_db
                present_in_db += new_present_in_db
                # following print just for DEBUG MODE
                logging.info(f"SUCESS: Anime title send to database: {added_to_db}")
                refreshed_count += 1
            else:
                logging.info(f"Missing information for torrent: '{torrent_filename.name}' - anime title: '{anime_title}', episode number: '{episode_number}'")

        if added_to_db == 0:
            logging.info("No new episodes added to the database.")
            return 0, 0, 0
    except Exception as e:
        logging.error(f"Error refreshing Nyaa data: {e}")
        return 0, 0, 0 # Return 0, 0 in case of error

    return added_to_db, refreshed_count, present_in_db


def get_nyaa_updates(usr_qry_anime_search, usr_qry_release_group, usr_qry_resolution = "1080p", category = "1", filter = "2", alt_release_grp = "EMBER"):

    # Helper function to log success/failure based on the results
    def log_update_status(added_to_db, refreshed_count, present_in_db):
        if added_to_db > 0:
            logging.info(f"SUCCESS: Refreshed {refreshed_count} torrents in Nyaa")
            logging.info(f"Added {added_to_db} new anime episodes to the database.")
        else:
            if present_in_db > 0:
                logging.info("Anime is already present on the database")
            else:
                logging.error("Failed to add new anime episodes to the database.")

    # Try refreshing Nyaa with the primary release group
    added_to_db, refreshed_count, present_in_db = refresh_nyaa(usr_qry_anime_search, usr_qry_release_group, usr_qry_resolution, category, filter)
    log_update_status(added_to_db, refreshed_count, present_in_db)

    if added_to_db < 1:
        logging.info(f"Trying secondary release group provider: '{alt_release_grp}'")
        # If no results, try refreshing with the secondary release group
        added_to_db, refreshed_count, present_in_db = refresh_nyaa(usr_qry_anime_search = usr_qry_anime_search, usr_qry_release_group = alt_release_grp, usr_qry_resolution = usr_qry_resolution, category = category, filter = filter)
        # Call the helper function to log the result
        log_update_status(added_to_db, refreshed_count, present_in_db)
   

def main():

    anime_escolhido = "asiofasdn"
    grupo_torrent_escolhido = "[SubsPlease]"
    grupo_release_alternativo = "[EMBER]"

    # Refresh titles in database
    get_nyaa_updates(anime_escolhido, grupo_torrent_escolhido, alt_release_grp=grupo_release_alternativo)

    # Delete anime function
    #db.delete_anime(anime_escolhido)

    # Close Database
    db.close_connection()

if __name__ == "__main__":
    main()

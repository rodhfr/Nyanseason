from nyaapy.nyaasi.nyaa import Nyaa
import anitopy
import db
import logging
from yaspin import yaspin
from fuzzywuzzy import process, fuzz

DEBUG_MODE = True
# Configure logging based on the debug mode
logging.basicConfig(level=logging.DEBUG if DEBUG_MODE else logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_best_match(user_input, title_list, threshold=80):
    """Return the best match from title_list based on fuzzy matching, only if the score is above the threshold."""
    best_match = process.extractOne(user_input, title_list, scorer=fuzz.ratio)
    return best_match[0] if best_match and best_match[1] >= threshold else None

def nyaasearch(usr_qry_anime_search, usr_qry_release_group="[SubsPlease]", usr_qry_resolution="1080p", category="1", filter="2"):
    """Search torrents using Nyaa."""
    composed_query = f"{usr_qry_anime_search} {usr_qry_release_group} {usr_qry_resolution}"
    try:
        return Nyaa.search(keyword=composed_query, category=category, filter=filter)
    except Exception as e:
        logging.error(f"Error searching Nyaa: {e}")
        return []

def anitopy_parse(torrent_filename, anitopy_options={'allowed_delimiters': ' '}):
    """Parse torrent filename and return anime title and episode number."""
    parsed_data = anitopy.parse(torrent_filename.name, anitopy_options)
    return parsed_data.get('anime_title'), parsed_data.get('episode_number')

def refresh_nyaa(usr_qry_anime_search, usr_qry_release_group, usr_qry_resolution="1080p", category="1", filter="2"):
    """Refresh the database with new episodes from Nyaa."""
    added_to_db = refreshed_count = present_in_db = 0
    try:
        nyaadata = nyaasearch(usr_qry_anime_search, usr_qry_release_group, usr_qry_resolution, category, filter)
        for torrent_filename in nyaadata:
            anime_title, episode_number = anitopy_parse(torrent_filename)
            if anime_title and episode_number:
                # Get the best match from the search query
                matched_title = get_best_match(usr_qry_anime_search, [anime_title])
                if matched_title:
                    # Only save if we have a valid match
                    new_added, new_present = db.new_db_entry(nome=matched_title, informacoes=episode_number)
                    added_to_db += new_added
                    present_in_db += new_present
                    logging.info(f"SUCCESS: Anime '{matched_title}' added to database.")
                    refreshed_count += 1
                else:
                    logging.info(f"No valid match for anime '{anime_title}' with search query.")
            else:
                logging.info(f"Missing info for torrent: '{torrent_filename.name}'.")
        return added_to_db, refreshed_count, present_in_db
    except Exception as e:
        logging.error(f"Error refreshing Nyaa data: {e}")
        return 0, 0, 0

def log_update_status(added_to_db, refreshed_count, present_in_db):
    """Log the update status based on the results."""
    if added_to_db > 0:
        logging.info(f"Refreshed {refreshed_count} torrents from Nyaa. Added {added_to_db} new episodes.")
    elif present_in_db > 0:
        logging.info("Anime is already present in the database.")
    else:
        logging.error("Failed to add new anime episodes.")

@yaspin(text="Fetching anime list...")
def get_nyaa_updates(usr_qry_anime_search, usr_qry_release_group, usr_qry_resolution="1080p", category="1", filter="2", alt_release_grp="EMBER"):
    """Fetch updates from Nyaa, including secondary release group if necessary."""
    added_to_db, refreshed_count, present_in_db = refresh_nyaa(usr_qry_anime_search, usr_qry_release_group, usr_qry_resolution, category, filter)
    log_update_status(added_to_db, refreshed_count, present_in_db)

    if added_to_db < 1:
        logging.info(f"Trying secondary release group: '{alt_release_grp}'")
        added_to_db, refreshed_count, present_in_db = refresh_nyaa(usr_qry_anime_search, alt_release_grp, usr_qry_resolution, category, filter)
        log_update_status(added_to_db, refreshed_count, present_in_db)

def main():
    anime_escolhido = "ranma"
    grupo_torrent_escolhido = "SubsPlease"
    grupo_release_alternativo = "EMBER"

    get_nyaa_updates(usr_qry_anime_search=anime_escolhido, usr_qry_release_group=grupo_torrent_escolhido, usr_qry_resolution=grupo_release_alternativo)

    all_data = db.qry_db_everything()
    print(all_data)

    db.close_connection()

if __name__ == "__main__":
    main()

import sqlite3

# Added unknown day 4 of november 2024
# status: working great.
# description: Connect to a database, or created if not exist.
conn = sqlite3.connect('animes.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS animes (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    informacoes TEXT
)
''')

# Added unknown day 4 of november 2024
# status: working great.
# description: create new entry in the database only if there is not the same one already.
#              Tries to avoid duplication.
def new_db_entry(informacoes, nome):
    present_in_database = 0
    cursor.execute('''
    SELECT * FROM animes WHERE nome = ? AND informacoes = ?
    ''', (nome, informacoes))
    
    if cursor.fetchone() is None:  # Se não encontrar resultados
        cursor.execute('''
        INSERT INTO animes (nome, informacoes) VALUES (?, ?)
        ''', (nome, informacoes))
        conn.commit()
        print(f"INFO: Successfully added anime '{nome}' episode '{informacoes}' to the database.")
    else:
        print(f"INFO: The episode '{informacoes}' of '{nome}' is already present on the database.")
        present_in_database = 1 
    return 1, present_in_database
# Added unknown day 4 of november 2024
# status: working great.
# description: query all anime names from database. Returns all items in a list of tuples.
def qry_db_everything():
    cursor.execute('SELECT * FROM animes')
    return cursor.fetchall() 

# Added unknown day 4 of november 2024
# status: working great. But need to address case sensisivity problem.
# description: search an anime info by name string. 
#              Case sensitive currently
def qry_db_by_name(nome):
    cursor.execute("SELECT nome, informacoes FROM animes WHERE nome LIKE ?", (f"%{nome}%",))
    return cursor.fetchall()

# Added unknown day 4 of november 2024
# status: working great.
# description: query all anime names from database
def qry_db_all_names():
    cursor.execute('SELECT nome FROM animes')
    return [row[0] for row in cursor.fetchall()]

# Added unknown day 4 of november 2024
# status: working great.
# description: closes the database connection.
def close_connection():
    conn.close

### --- NEW AND BROKEN FOLLOWING --- ###
# Added unknown day 4 of november 2024
# status: don't know if it is working probably not
# description: searches for animes by quering the string name
def get_latest_episode(nome):
    cursor.execute('SELECT informacoes FROM animes WHERE nome = ?', (nome,))
    episodes = cursor.fetchall()
    
    latest_episode_number = -1  # Initialize as -1 for comparison
    
    for informacoes in episodes:
        episode_number = int(informacoes[0])  # Convert to integer
        if episode_number > latest_episode_number:
            latest_episode_number = episode_number  # Update the latest episode number

    return latest_episode_number if latest_episode_number != -1 else None  # Return the latest episode number or None

# Added 20:21 day 5 of november 2024
# status: very little tested but working
# description: This function excludes anime from name. 
#              Case insensitive string anime name and also all related 
def delete_anime(nome):
    cursor.execute('''
    DELETE FROM animes WHERE nome LIKE ? COLLATE NOCASE 
    ''', (f"%{nome}%",))  # Search for the base anime name (case-insensitive) and delete all matching entries 
                          # Allowing partial matching (e.g., 'One Piece')
    conn.commit()
    if cursor.rowcount > 0:
        print(f"INFO: Anime '{nome}' and all related entries successfully deleted.")
    else:
        print(f"INFO: No anime found with the name '{nome}' to delete.")

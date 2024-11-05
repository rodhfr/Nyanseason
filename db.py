import sqlite3

# Conectar ao banco de dados (ou criar um se não existir)
conn = sqlite3.connect('animes.db')

# Criar um cursor
cursor = conn.cursor()

# Criar a tabela
cursor.execute('''
CREATE TABLE IF NOT EXISTS animes (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    informacoes TEXT
)
''')

def new_db_entry(nome, informacoes):
    # Função para adicionar um episódio de anime à base de dados
    # Verificando se a entrada já existe
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


def qry_db_everything():
    # Funcao que retorna todos os items da database em um dicionario
    cursor.execute('SELECT * FROM animes')
    return cursor.fetchall() # retorna em lista de tuplas

def qry_db_by_name(nome):
    # Search an anime by name (part of name)
    cursor.execute("SELECT nome, informacoes FROM animes WHERE nome LIKE ?", (f"%{nome}%",))
    return cursor.fetchall()

def qry_db_all_names():
    # Consulta todos os nomes dos animes na db
    cursor.execute('SELECT nome FROM animes')
    return [row[0] for row in cursor.fetchall()]

def get_latest_episode(nome):
    cursor.execute('SELECT informacoes FROM animes WHERE nome = ?', (nome,))
    episodes = cursor.fetchall()
    
    latest_episode_number = -1  # Initialize as -1 for comparison
    
    for informacoes in episodes:
        episode_number = int(informacoes[0])  # Convert to integer
        if episode_number > latest_episode_number:
            latest_episode_number = episode_number  # Update the latest episode number

    return latest_episode_number if latest_episode_number != -1 else None  # Return the latest episode number or None


def close_connection():
    conn.close



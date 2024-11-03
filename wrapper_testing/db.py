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

# Função para adicionar um anime
def new_entry_database(nome, informacoes):
    cursor.execute('''
    INSERT INTO animes (nome, informacoes) VALUES (?, ?)
    ''', (nome, informacoes))
    conn.commit()

def consultar_animes():
    cursor.execute('SELECT * FROM animes')
    return cursor.fetchall()
    

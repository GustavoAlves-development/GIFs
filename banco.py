import sqlite3

conexao = sqlite3.connect('API-GIFs.db')
cursor = conexao.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS GifsAPI(ID INTEGER PRIMARY KEY, Descricao TEXT, Gif TEXT)')
conexao.commit()


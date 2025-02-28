from flask import Flask, render_template, redirect, request, g
import requests
import sqlite3

def ligar_banco():
    banco = g._database = sqlite3.connect('API-GIfs.db')
    return banco
app = Flask(__name__)

@app.route('/')
def home():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('SELECT * FROM GifsAPI')
    dados = cursor.fetchall()

    return render_template('index.html', Titulo ="API Gifs", dados = dados)

@app.route('/cadastro')
def cadastro():
    # Gerar Imagem
    api_key = 'HauljIjwoi5o16fIBodhPGOmnbh7ZCwi'
    url = 'https://api.giphy.com/v1/gifs/random'
    parametros = {
        'api_key': api_key,
        'tag': 'funny',
        'rating': 'g'
    }
    solicitacao = requests.get(url, params=parametros)
    imagem = solicitacao.json()['data']['images']['original']['url']

    return render_template('cadastro.html', Titulo ="API Imagens - Cadastro", imagem=imagem)

@app.route('/galeria')
def galeria():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute('SELECT * FROM GifsAPI')
    dados = cursor.fetchall()

    return render_template('galeria.html', Titulo ="API Imagens - Galeria", dados=dados)

@app.route('/criar', methods =['POST'])
def criar():

    descricao = request.form['descricao']
    url = request.form['url']

    banco = ligar_banco()
    cursor = banco.cursor()

    cursor.execute('INSERT INTO GifsAPI(Descricao,Gif)'
                   'VALUES (?,?)', (descricao,url))
    banco.commit()

    return redirect("/cadastro")

@app.route('/unique/<id>', methods=['GET'])
def unique(id):
    banco = ligar_banco()
    cursor = banco.cursor()

    cursor.execute('SELECT * FROM GifsAPI WHERE ID = ?;', (id,))
    dados = cursor.fetchone()

    return render_template("ticket-details.html", dados=dados)

@app.route('/excluir/<id>', methods=['GET'])
def excluir(id):
    banco = ligar_banco()
    cursor = banco.cursor()

    cursor.execute('DELETE FROM GifsAPI WHERE ID = ?;', (id,))
    banco.commit()

    return redirect("/galeria")



if __name__ == '__main__':
    app.run()

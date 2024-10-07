from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Função para buscar o ID do ator
def get_actor_id(actor_name):
    api_key = os.getenv('TMDB_API_KEY')
    url = f"https://api.themoviedb.org/3/search/person?api_key={api_key}&query={actor_name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            return data['results'][0]['id']
    return None

# Função para buscar os filmes de um ator
def get_actor_movies(actor_id):
    api_key = os.getenv('TMDB_API_KEY')
    url = f"https://api.themoviedb.org/3/person/{actor_id}/movie_credits?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return {movie['id']: movie['title'] for movie in response.json().get('cast', [])}
    return {}

# Rota para a página principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota para buscar filmes em comum
@app.route('/filmes_comuns', methods=['POST'])
def filmes_comuns():
    ator1 = request.form['ator1']
    ator2 = request.form['ator2']
    
    if not ator1 or not ator2:
        return render_template('index.html', error="Você precisa fornecer dois atores.")
    
    ator1_id = get_actor_id(ator1)
    ator2_id = get_actor_id(ator2)
    
    if not ator1_id or not ator2_id:
        return render_template('index.html', error="Não foi possível encontrar um ou ambos os atores.")
    
    ator1_filmes = get_actor_movies(ator1_id)
    ator2_filmes = get_actor_movies(ator2_id)
    
    filmes_comuns = set(ator1_filmes.keys()) & set(ator2_filmes.keys())
    
    resultado = [ator1_filmes[filme_id] for filme_id in filmes_comuns]
    
    return render_template('index.html', filmes=resultado)

# Rota para buscar sugestões de atores
@app.route('/buscar_atores', methods=['GET'])
def buscar_atores():
    nome_ator = request.args.get('query')
    api_key = os.getenv('TMDB_API_KEY')
    
    # Chama a API da TMDB
    url = f"https://api.themoviedb.org/3/search/person?api_key={api_key}&query={nome_ator}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'results': []}), 404

if __name__ == "__main__":
    app.run(debug=True)

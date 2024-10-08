from flask import Flask, render_template, request, jsonify
import requests
import os
from collections import deque

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

# Função para encontrar a rota entre dois atores
def find_actor_route(actor1_id, actor2_id):
    queue = deque([(actor1_id, [])])  # (ID do ator, caminho até agora)
    visited = set()  # Para rastrear atores visitados

    while queue:
        current_actor_id, path = queue.popleft()
        if current_actor_id in visited:
            continue
        
        visited.add(current_actor_id)
        current_movies = get_actor_movies(current_actor_id)

        for movie_id, movie_title in current_movies.items():
            # Adiciona o filme ao caminho
            new_path = path + [(current_actor_id, movie_title)]
            
            # Buscando o elenco do filme
            movie_credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={os.getenv('TMDB_API_KEY')}"
            response = requests.get(movie_credits_url)
            if response.status_code == 200:
                cast = response.json().get('cast', [])
                for actor in cast:
                    if actor['id'] == actor2_id:
                        # Se encontramos o ator2, retornamos o caminho
                        return new_path + [(actor2_id, f"{get_actor_name(actor2_id)} encontrado(a)")]
                    if actor['id'] not in visited:
                        queue.append((actor['id'], new_path))

    return None  # Se não encontrar uma rota

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
    
    if filmes_comuns:
        resultado = [ator1_filmes[filme_id] for filme_id in filmes_comuns]
    else:
        # Se não houver filmes em comum, busque a rota entre os dois atores
        route = find_actor_route(ator1_id, ator2_id)
        if route:
            caminho = " -> ".join([f"{get_actor_name(actor_id)} em '{movie}'" for actor_id, movie in route])
            return render_template('index.html', error=f"Rota encontrada: {caminho}")
        else:
            return render_template('index.html', error="Não foi encontrado nenhum filme em comum nem ator em comum.")
    
    return render_template('index.html', filmes=resultado)

def get_actor_name(actor_id):
    api_key = os.getenv('TMDB_API_KEY')
    url = f"https://api.themoviedb.org/3/person/{actor_id}?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('name', 'Unknown Actor')
    return 'Unknown Actor'

@app.route('/buscar_atores')
def buscar_atores():
    query = request.args.get('query', '')
    api_key = os.getenv('TMDB_API_KEY')
    url = f"https://api.themoviedb.org/3/search/person?api_key={api_key}&query={query}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return jsonify(data)  # Retorna a resposta como JSON
    return jsonify({'results': []})  # Retorna uma lista vazia em caso de erro

if __name__ == "__main__":
    app.run()

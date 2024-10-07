import requests
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtenha a API Key do arquivo .env
api_key = os.getenv('TMDB_API_KEY')
movie_id = 550  # Exemplo com o filme Clube da Luta
url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}&language=pt-BR'

response = requests.get(url)
if response.status_code == 200:
    credits = response.json()
    
    # Lista os primeiros 10 atores do elenco
    for actor in credits['cast'][:10]:  # Lista os 10 primeiros atores
        print(f"Ator: {actor['name']} como {actor['character']}")
else:
    print("Erro ao buscar o elenco do filme.")


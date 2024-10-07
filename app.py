import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('TMDB_API_KEY')

def get_person_id(actor_name):
    url = f"https://api.themoviedb.org/3/search/person?api_key={api_key}&query={actor_name}&language=pt-BR"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            return data['results'][0]['id']
        else:
            print(f"Ator {actor_name} não encontrado.")
            return None
    else:
        print(f"Erro ao buscar o ator {actor_name}.")
        return None

def get_actor_movies(person_id):
    url = f"https://api.themoviedb.org/3/person/{person_id}/movie_credits?api_key={api_key}&language=pt-BR"
    response = requests.get(url)
    if response.status_code == 200:
        credits = response.json()
        movies = {movie['title'] for movie in credits['cast']}
        return movies
    else:
        print(f"Erro ao buscar os filmes do ator com ID {person_id}.")
        return set()

def find_common_movies(actor1, actor2):
    person_id1 = get_person_id(actor1)
    person_id2 = get_person_id(actor2)
    
    if person_id1 and person_id2:
        movies_actor1 = get_actor_movies(person_id1)
        movies_actor2 = get_actor_movies(person_id2)

        common_movies = movies_actor1.intersection(movies_actor2)

        if common_movies:
            print(f"Filmes em comum entre {actor1} e {actor2}:")
            for movie in common_movies:
                print(f"- {movie}")
        else:
            print(f"{actor1} e {actor2} não têm filmes em comum.")
    else:
        print("Não foi possível encontrar os IDs dos atores.")

actor1 = input("Digite o nome do primeiro ator: ")
actor2 = input("Digite o nome do segundo ator: ")

find_common_movies(actor1, actor2)

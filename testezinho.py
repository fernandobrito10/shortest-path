import requests
import os

# Função para buscar filmes de um ator por ID
def get_actor_movies(actor_id):
    url = f"https://api.themoviedb.org/3/person/{actor_id}/movie_credits?api_key=c0bffeb6fee7bb5ad14f542448f48300"
    response = requests.get(url)

    if response.status_code == 200:
        movies = response.json().get('cast', [])
        # Filtra e ordena os filmes por popularidade
        sorted_movies = sorted(movies, key=lambda movie: movie.get('popularity', 0), reverse=True)
        return sorted_movies
    else:
        print(f"Erro ao buscar filmes: {response.status_code}")
        return []

def print_movies(movies):
    if movies:
        print(f"{'Título':<50} {'Popularidade':<10}")
        print("-" * 60)
        for movie in movies:
            print(f"{movie['title']:<50} {movie['popularity']:<10}")
    else:
        print("Nenhum filme encontrado.")

if __name__ == "__main__":
    actor_id = 52583  # ID do ator
    movies = get_actor_movies(actor_id)
    print_movies(movies)

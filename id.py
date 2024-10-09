import requests

def get_actor_id(actor_name):
    api_key = 'c0bffeb6fee7bb5ad14f542448f48300'  # Teste diretamente com sua chave
    url = f"https://api.themoviedb.org/3/search/person?api_key={api_key}&query={actor_name}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            actor_id = data['results'][0]['id']
            actor_name = data['results'][0]['name']
            return actor_id, actor_name
        else:
            return None, None
    else:
        return None, None

# Exemplo de uso:
while True:
    actor_name = input('Digite o nome do ator: ')
    actor_id, actor_name = get_actor_id(actor_name)
    if actor_id:
        print(f"O ID do ator {actor_name} é {actor_id}.")
    else:
        print("Ator não encontrado.")

    CORINGA_ACTORS = [
    6193,   # DiCaprio
    10055,  # Fernanda Montenegro
    52583,     # Wagner Moura
    3223,     # Downey Jr.
    3895 # Michael Caine
] 
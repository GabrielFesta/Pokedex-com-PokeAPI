import requests
import tkinter as tk
from PIL import Image, ImageTk
import io

# Função para obter habilidades do Pokémon
def obter_habilidades(poke):
    habilidades = [ability['ability']['name'] for ability in poke['abilities']] 
    return habilidades

# Função para obter elemento do Pokémon
def obter_elemento(poke):
    tipo = [type['type']['name'] for type in poke['types']]
    return tipo

# Função para obter o HP do Pokémon
def obter_hp(poke):
    hp = poke['stats'][0]['base_stat']
    return hp

# Função para obter os melhores ataques do Pokémon
def obter_melhores_ataques(poke):
    melhores_ataques = []
    for move in poke['moves']:
        move_data = requests.get(move['move']['url']).json()
        power = move_data['power'] if move_data.get('power') else 0
        description = move_data['effect_entries'][0]['short_effect'] if move_data['effect_entries'] else "Sem descrição"
        melhores_ataques.append((move['move']['name'], power, description))
    melhores_ataques.sort(key=lambda x: x[1], reverse=True)
    return melhores_ataques[:5]  # Retorna os 5 melhores ataques

# Função para obter a imagem do Pokémon
def obter_imagem(poke):
    sprite_url = poke['sprites']['front_default']
    response = requests.get(sprite_url)
    image_data = response.content
    image = Image.open(io.BytesIO(image_data))
    return image

# Função para exibir informações do Pokémon na interface gráfica
def exibir_info_pokemon():
    pokemon = entry_pokemon.get()
    api = f"https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}"
    response = requests.get(api)
    
    if response.status_code == 200:
        poke = response.json()
        habilidades = obter_habilidades(poke)
        tipos = obter_elemento(poke)
        hp = obter_hp(poke)
        melhores_ataques = obter_melhores_ataques(poke)
        imagem = obter_imagem(poke)
        
        label_habilidades.config(text="Habilidades: " + ", ".join(habilidades))
        label_tipo.config(text="Tipo: " + ", ".join(tipos))
        label_hp.config(text="HP: " + str(hp))  # Convertendo para string antes da concatenação
        
        # Exibir ataques com descrição
        descricao_ataques = "\n".join([f"{ataque[0]}: {ataque[2]}" for ataque in melhores_ataques])
        label_ataques.config(text="Melhores Ataques:\n" + descricao_ataques)
        
        photo = ImageTk.PhotoImage(imagem)
        label_imagem.config(image=photo)
        label_imagem.image = photo
        
    else:
        label_habilidades.config(text="Pokemon não encontrado")
        label_tipo.config(text="")
        label_hp.config(text="")
        label_ataques.config(text="")
        label_imagem.config(image="")

# Interface gráfica
root = tk.Tk()
root.title("Pokedex")

# Entrada para o nome do Pokémon
label_entry = tk.Label(root, text="Digite o nome do Pokémon: ")
label_entry.pack()
entry_pokemon = tk.Entry(root)  # Atribuindo ao widget Entry
entry_pokemon.pack()

# Botão para buscar informações do Pokémon
button_buscar = tk.Button(root, text="Buscar", command=exibir_info_pokemon)
button_buscar.pack()

# Labels para exibir informações do Pokémon
label_habilidades = tk.Label(root, text="")
label_habilidades.pack()
label_tipo = tk.Label(root, text="")
label_tipo.pack()
label_hp = tk.Label(root, text="")
label_hp.pack()
label_ataques = tk.Label(root, text="")
label_ataques.pack()

# Label para exibir a imagem do Pokémon
label_imagem = tk.Label(root)
label_imagem.pack()

root.mainloop()


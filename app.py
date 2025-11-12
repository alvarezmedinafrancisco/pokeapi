from flask import Flask , render_template , request , redirect , url_for , flash
import requests 
app = Flask(__name__)
app.secret_key = 'contrasena_super_secreta'
pokeapi_url = 'https://pokeapi.co/api/v2/pokemon/'

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/buscar', methods=['POST'])
def buscar_pokemon():
    nombre_pokemon = request.form.get('nombre_pokemon', '').strip().lower()
    if not nombre_pokemon:
        flash('Por favor, ingresa el nombre de un Pokémon.', 'error')
        return redirect(url_for('index.html'))

    try:
        resp = requests.get(f'{pokeapi_url}{nombre_pokemon}')
        if resp.status_code == 200:
            datos_pokemon = resp.json()
            pokemon_info = {
                'nombre': datos_pokemon['name'].capitalize(),
                "id": datos_pokemon['id'],
                "height": datos_pokemon['height'] / 10,
                "weight": datos_pokemon['weight'] / 10,
                'imagen': datos_pokemon['sprites']['front_default'],
                "estadisticas": {stat['stat']['name']: stat['base_stat'] for stat in datos_pokemon['stats']},
                'tipos': [tipo['type']['name'].capitalize() for tipo in datos_pokemon['types']],
                'habilidades': [habilidad['ability']['name'].capitalize() for habilidad in datos_pokemon['abilities']]
            }
            return render_template('poke.html', pokemon=pokemon_info)
        else:
            flash(f'Pokémon {nombre_pokemon}no encontrado. Por favor, verifica el nombre e intenta de nuevo.', 'error')
            return redirect(url_for('inicio'))
    except requests.RequestException:
        flash('Error al conectar con la PokeAPI. Por favor, intenta más tarde.', 'error')
        return redirect(url_for('inicio'))
            
if __name__ == '__main__':
    app.run(debug=True)
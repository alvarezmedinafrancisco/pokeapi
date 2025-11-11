from flask import Flask , render_template , request , redirect , url_for , flash
import requests
app = Flask(__name__)
app.secret_key = 'contraseñaipermegasecreta'
pokeapi_url = 'https://pokeapi.co/api/v2/pokemon/'

app.run(debug=True)

@app.route('/')
def inicio():
    requests.get(pokeapi_url)
    return render_template('index.html')

@app.route('/buscar', methods=['POST'])
def buscar_pokemon():
    nombre_pokemon = request.form['nombre_pokemon'].lower()
    response = requests.get(f'{pokeapi_url}{nombre_pokemon}')
    if response.status_code == 200:
        datos_pokemon = response.json()
        nombre = datos_pokemon['name'].capitalize()
        imagen = datos_pokemon['sprites']['front_default']
        tipos = [tipo['type']['name'].capitalize() for tipo in datos_pokemon['types']]
        habilidades = [habilidad['ability']['name'].capitalize() for habilidad in datos_pokemon['abilities']]
        estadisticas = {stat['stat']['name'].capitalize(): stat['base_stat'] for stat in datos_pokemon['stats']}
        
        return render_template('pokemon.html', nombre=nombre, imagen=imagen, tipos=tipos, habilidades=habilidades, estadisticas=estadisticas)
    if not nombre_pokemon:
        flash('Por favor, ingresa el nombre de un Pokémon.', 'error')
        return redirect(url_for('index'))
    
    
    return redirect(url_for('mostrar_pokemon'))
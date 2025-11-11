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
    
    if not nombre_pokemon:
        flash('Por favor, ingresa el nombre de un Pokémon.', 'error')
        return redirect(url_for('index'))
    
    
    return redirect(url_for('mostrar_pokemon'))
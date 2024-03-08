from flask import Flask, request, jsonify, render_template
import pandas as pd
from joblib import load
import os

os.chdir(**A COMPLETER**)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Vérifie si le fichier est présent dans la requête
    if 'file' not in request.files:
        return "Aucun fichier fourni", 400
    
    file = request.files['file']
    model_file = request.files['model']
    
    # Si l'utilisateur ne sélectionne pas de fichier, le navigateur
    # soumet un fichier vide sans nom de fichier.
    if file.filename == '' or model_file.filename == '':
        return "Modèle ou fichier CSV non sélectionné", 400
    
    if file and model_file:
        # Charge le modèle .pkl sélectionné par l'utilisateur
        model = load(model_file)

        # Lit le fichier CSV dans un DataFrame pandas
        df = pd.read_csv(file)
        
        # Prédictions
        prediction = model.predict(df)
    
        data = prediction.tolist()
        predictions = [("Individu {}".format(i+1), pred) for i, pred in enumerate(data)]
        return render_template('resultat.html', predictions=predictions)

if __name__ == '__main__':
    app.run(debug=True)

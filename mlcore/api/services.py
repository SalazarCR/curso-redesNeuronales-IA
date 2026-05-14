import json
import numpy as np
from tensorflow.keras.models import model_from_json
import os


class TitanicPredictor:
    """Servicio para hacer predicciones del Titanic"""
    
    def __init__(self):
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Carga el modelo guardado desde disco"""
        try:
            model_dir = os.path.join(os.path.dirname(__file__), '..', 'model')
            json_path = os.path.join(model_dir, 'mimodelo.json')
            weights_path = os.path.join(model_dir, 'mimodelo.weights.h5')
            
            # Cargar la estructura del modelo
            with open(json_path, 'r') as json_file:
                loaded_model_json = json_file.read()
            
            self.model = model_from_json(loaded_model_json)
            
            # Cargar los pesos
            self.model.load_weights(weights_path)
            
            # Compilar el modelo
            self.model.compile(
                loss='binary_crossentropy',
                optimizer='adam',
                metrics=['accuracy']
            )
            
            return True
        except Exception as e:
            print(f"Error cargando el modelo: {e}")
            return False
    
    def preprocess_data(self, data):
        """Preprocesa los datos del formulario para la predicción"""
        try:
            # Extraer valores numéricos
            parch = float(data.get('parch', 0))
            age = float(data.get('age', 30))
            n_siblings_spouses = float(data.get('n_siblings_spouses', 0))
            fare = float(data.get('fare', 0))
            
            # El modelo espera: [fare, parch, age, n_siblings_spouses]
            features = np.array([[fare, parch, age, n_siblings_spouses]])
            
            return features, True, None
        except Exception as e:
            return None, False, f"Error en preprocesamiento: {str(e)}"
    
    def predict(self, data):
        """Realiza una predicción basada en los datos del formulario"""
        if self.model is None:
            return {
                'success': False,
                'prediction': None,
                'probability': None,
                'error': 'Modelo no cargado'
            }
        
        try:
            # Preprocesar los datos
            features, success, error = self.preprocess_data(data)
            
            if not success:
                return {
                    'success': False,
                    'prediction': None,
                    'probability': None,
                    'error': error
                }
            
            # Hacer la predicción
            raw_prediction = self.model.predict(features, verbose=0)
            probability = float(raw_prediction[0][0])
            prediction = int(round(probability))
            
            return {
                'success': True,
                'prediction': prediction,
                'probability': probability,
                'prediction_text': 'Sobrevivió' if prediction == 1 else 'No sobrevivió',
                'probability_percentage': f"{probability * 100:.2f}%"
            }
        except Exception as e:
            return {
                'success': False,
                'prediction': None,
                'probability': None,
                'error': f"Error en predicción: {str(e)}"
            }


# Instancia global del predictor
predictor = TitanicPredictor()

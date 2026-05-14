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
        """
        Preprocesa los datos del formulario para la predicción.
        
        El modelo espera 5 features en este orden:
        [Fare, Pclass, Gender, Age, SibSp]
        
        Mapeo de entrada:
        - fare → Fare (numérico)
        - passenger_class → Pclass (First=1, Second=2, Third=3)
        - sex → Gender (male=0, female=1)
        - age → Age (numérico)
        - n_siblings_spouses → SibSp (numérico)
        """
        try:
            # Convertir clase de pasaje a número
            class_map = {'First': 1, 'Second': 2, 'Third': 3}
            pclass = float(class_map.get(data.get('passenger_class', 'Third'), 3))
            
            # Convertir género a numérico
            gender_map = {'male': 0, 'female': 1}
            gender = float(gender_map.get(data.get('sex', 'male'), 0))
            
            # Extraer valores numéricos
            fare = float(data.get('fare', 0))
            age = float(data.get('age', 30))
            sibsp = float(data.get('n_siblings_spouses', 0))
            
            # El modelo espera: [Fare, Pclass, Gender, Age, SibSp]
            features = np.array([[fare, pclass, gender, age, sibsp]])
            
            return features, True, None
        except Exception as e:
            return None, False, f"Error en preprocesamiento: {str(e)}"
    
    def predict(self, data):
        """
        Realiza una predicción basada en los datos del formulario.
        
        Returns:
            dict con resultado y probabilidad
        """
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

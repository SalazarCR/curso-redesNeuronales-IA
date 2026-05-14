import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import confusion_matrix
import os

class NeuralNetworkService:
    """
    Servicio encargado de la lógica de la Red Neuronal Backpropagation.
    Esta clase maneja el preprocesamiento, construcción del modelo,
    entrenamiento y generación de métricas.
    """
    
    def __init__(self):
        self.model = None
        self.history = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        
    def preprocess_dataset(self, df):
        """
        Preprocesa el dataset automáticamente:
        1. Identifica la columna objetivo (asumimos la primera o última si no se especifica).
        2. Maneja valores nulos (media para numéricos, moda para categóricos).
        3. Codifica variables categóricas.
        4. Escala variables numéricas.
        """
        # Clonar para no afectar el original
        data = df.copy()
        
        # 1. Identificar Target (Y) y Features (X)
        # Por simplicidad académica, asumimos que 'survived' es el target si existe, 
        # o la primera columna del dataset.
        target_col = 'survived' if 'survived' in data.columns else data.columns[0]
        Y = data[target_col].values
        X = data.drop(columns=[target_col])
        
        # 2. Manejo de valores nulos
        for col in X.columns:
            if X[col].dtype == 'object':
                X[col] = X[col].fillna(X[col].mode()[0])
                # Codificación de etiquetas (Label Encoding)
                le = LabelEncoder()
                X[col] = le.fit_transform(X[col].astype(str))
                self.label_encoders[col] = le
            else:
                X[col] = X[col].fillna(X[col].mean())
        
        # 3. Escalamiento de características
        X_scaled = self.scaler.fit_transform(X)
        
        return X_scaled, Y, X.columns.tolist()

    def build_model(self, input_dim):
        """
        Construye una red neuronal secuencial Backpropagation.
        """
        model = keras.Sequential([
            # Capa de entrada y primera capa oculta (32 neuronas)
            layers.Dense(32, input_dim=input_dim, activation='relu'),
            # Segunda capa oculta (32 neuronas)
            layers.Dense(32, activation='relu'),
            # Capa de salida (1 neurona para clasificación binaria con Sigmoid)
            layers.Dense(1, activation='sigmoid')
        ])
        
        # Compilación del modelo usando el optimizador Adam (Backpropagation automático)
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        return model

    def train(self, X, Y, epochs=100):
        """
        Entrena el modelo y guarda el historial.
        """
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
        
        # Entrenamiento
        self.history = self.model.fit(
            X_train, Y_train,
            epochs=epochs,
            batch_size=32,
            validation_data=(X_test, Y_test),
            verbose=0 # No mostrar logs en consola para no saturar Django
        )
        
        # Generar predicciones para la matriz de confusión
        Y_pred = self.model.predict(X_test)
        Y_pred_binary = (Y_pred > 0.5).astype(int)
        
        # Métricas finales
        cm = confusion_matrix(Y_test, Y_pred_binary)
        
        return {
            'accuracy': self.history.history['accuracy'][-1],
            'val_accuracy': self.history.history['val_accuracy'][-1],
            'loss_history': self.history.history['loss'],
            'acc_history': self.history.history['accuracy'],
            'confusion_matrix': cm.tolist(),
            'epochs_count': len(self.history.history['loss'])
        }

# Instancia global para ser usada en las views
nn_service = NeuralNetworkService()

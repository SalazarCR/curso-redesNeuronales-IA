from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .forms import UploadFileForm
from .neural_network import nn_service
import pandas as pd
import os
import json

def dashboard(request):
    """
    Vista principal: Dashboard académico.
    """
    return render(request, 'app/dashboard.html')

def train_model_view(request):
    """
    Vista para manejar la carga de archivos y el entrenamiento.
    """
    results = None
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # 1. Guardar el archivo temporalmente
            file = request.FILES['file']
            fs = FileSystemStorage(location='uploads/')
            filename = fs.save(file.name, file)
            filepath = fs.path(filename)
            
            epochs = form.cleaned_data['epochs']
            
            try:
                # 2. Leer archivo con Pandas
                if filename.endswith('.csv'):
                    df = pd.read_csv(filepath)
                else:
                    df = pd.read_excel(filepath)
                
                # 3. Preprocesar y entrenar
                X, Y, columns = nn_service.preprocess_dataset(df)
                nn_service.build_model(input_dim=X.shape[1])
                results = nn_service.train(X, Y, epochs=epochs)
                
                # Agregar información del dataset para el dashboard
                results['dataset_info'] = {
                    'rows': df.shape[0],
                    'cols': df.shape[1],
                    'features': columns
                }
                
                # Convertir a JSON para que Chart.js lo entienda
                results['json_results'] = json.dumps(results)
                
            except Exception as e:
                results = {'error': str(e)}
            finally:
                # Limpiar archivo temporal
                if os.path.exists(filepath):
                    os.remove(filepath)
            
            return render(request, 'app/results.html', {'results': results})
    else:
        form = UploadFileForm()
    
    return render(request, 'app/train.html', {'form': form})

def explanation(request):
    """
    Vista con la explicación teórica para el profesor.
    """
    return render(request, 'app/explanation.html')

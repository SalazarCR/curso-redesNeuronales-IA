from django.shortcuts import render
from .forms import TitanicPredictionForm
from .services import predictor

def home(request):
    """Vista para el formulario de predicción del Titanic"""
    result = None
    error = None

    if request.method == "POST":
        form = TitanicPredictionForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            
            # Hacer la predicción
            result = predictor.predict(data)

    else:
        form = TitanicPredictionForm()

    return render(request, "form.html", {
        "form": form,
        "result": result,
        "error": error
    })
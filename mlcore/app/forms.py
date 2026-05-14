from django import forms

class UploadFileForm(forms.Form):
    """
    Formulario simple para subir archivos CSV o Excel.
    """
    file = forms.FileField(
        label='Selecciona un dataset (CSV o XLSX)',
        help_text='Máximo 5MB'
    )
    epochs = forms.IntegerField(
        label='Número de Iteraciones (Epochs)',
        initial=100,
        min_value=1,
        max_value=1000
    )

from django import forms

class TitanicPredictionForm(forms.Form):
    """Formulario para predicción del Titanic"""
    
    GENDER_CHOICES = [
        ('male', 'Masculino'),
        ('female', 'Femenino'),
    ]
    
    CLASS_CHOICES = [
        ('First', 'Primera clase'),
        ('Second', 'Segunda clase'),
        ('Third', 'Tercera clase'),
    ]
    
    DECK_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('F', 'F'),
        ('G', 'G'),
        ('unknown', 'Desconocido'),
    ]
    
    EMBARK_CHOICES = [
        ('Southampton', 'Southampton'),
        ('Cherbourg', 'Cherbourg'),
        ('Queenstown', 'Queenstown'),
    ]
    
    ALONE_CHOICES = [
        ('y', 'Sí'),
        ('n', 'No'),
    ]
    
    sex = forms.ChoiceField(
        choices=GENDER_CHOICES,
        label='Género',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    age = forms.FloatField(
        label='Edad',
        min_value=0,
        max_value=120,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )
    
    n_siblings_spouses = forms.IntegerField(
        label='Hermanos/Esposos a bordo',
        min_value=0,
        max_value=10,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    parch = forms.IntegerField(
        label='Padres/Hijos a bordo',
        min_value=0,
        max_value=10,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    fare = forms.FloatField(
        label='Tarifa de pasaje (£)',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    
    passenger_class = forms.ChoiceField(
        choices=CLASS_CHOICES,
        label='Clase de pasaje',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    deck = forms.ChoiceField(
        choices=DECK_CHOICES,
        label='Cubierta',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    embark_town = forms.ChoiceField(
        choices=EMBARK_CHOICES,
        label='Puerto de embarque',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    alone = forms.ChoiceField(
        choices=ALONE_CHOICES,
        label='¿Viaja solo?',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
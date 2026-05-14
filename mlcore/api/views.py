from django.shortcuts import render
from .forms import DataForm
# Create your views here.
def home(request):
    result = None

    if request.method == "POST":
        form = DataForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            # aquí luego conectas tu ML
            result = data  # temporal

    else:
        form = DataForm()

    return render(request, "form.html", {
        "form": form,
        "result": result
    })
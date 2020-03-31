from django.views.generic import ListView
from example.models import CeleryTask

class MainView(ListView):
    model = CeleryTask
    template_name = 'main.html'
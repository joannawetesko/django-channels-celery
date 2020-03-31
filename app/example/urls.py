from django.conf.urls import url
from example.views import MainView

urlpatterns = [
    url('', MainView.as_view(), name='main'),
]
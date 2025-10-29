from django.urls import path
from .views import presentar_preguntas

urlpatterns = [
    path('', presentar_preguntas, name='presentar_preguntas'),
]

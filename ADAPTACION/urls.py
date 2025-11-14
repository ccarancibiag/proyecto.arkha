from django.urls import path
from .views import presentar_preguntas
from .views import presentar_preguntas, reiniciar

urlpatterns = [
    path('', presentar_preguntas, name='presentar_preguntas'),
    path('reiniciar/', reiniciar, name='reiniciar'),
]

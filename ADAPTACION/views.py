from django.shortcuts import render
from .models import Question
from random import randint

# Create your views here.
#Vamos a definir 4 niveles de dificultad, facil-medio-dificil-experto
#iniciaremos con el nivel dificil, pues si acierta sabremos que tendra un buen nivel
#sino acertara, bajaremos a medio y luego a facil.
nivel = 'facil'
correctas = 0
incorrectas = 0

def obtener_pregunta(nivel):
    preguntas= list(Question.objects.filter(dificultad=nivel))
    if len(preguntas) == 0:
        return None
    return preguntas[randint(0, len(preguntas)-1)]


#aqui si respondemos bien sumamos 1 a correctas, si no a incorrectas, si acertamos 
#3 seguidas subimos de nivel, si fallamos 3 seguidas bajamos de nivel, porahora dejemoslo asi digo
def cambiar_nivel(nivel, correctas, incorrectas):
    if correctas >= 3:
        if nivel == 'facil':
            nivel = 'medio'
        elif nivel == 'medio':
            nivel = 'dificil'
        elif nivel == 'dificil':
            nivel = 'experto'
        correctas = 0
    if incorrectas > 2:
        if nivel == 'experto':
            nivel = 'dificil'
        elif nivel == 'dificil':
            nivel = 'medio'
        elif nivel == 'medio':
            nivel = 'facil'
        incorrectas = 0
    return nivel, correctas, incorrectas



    
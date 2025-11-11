from django.shortcuts import render
from .models import Question
from random import randint
from django.shortcuts import render, redirect
from django.contrib import messages




# Create your views here.
#Vamos a definir 4 niveles de dificultad, facil-medio-dificil-experto
#iniciaremos con el nivel dificil, pues si acierta sabremos que tendra un buen nivel
#sino acertara, bajaremos a medio y luego a facil.
nivel = 'Facil'
correctas = 0
incorrectas = 0

def obtener_pregunta(nivel):
    preguntas= list(Question.objects.filter(dificultad=nivel))
    if len(preguntas) == 0:
        return None
    return preguntas[randint(0, len(preguntas)-1)]

###def evaluar_respuesta(pregunta, respuesta_usuario):
  #  if pregunta.respuesta_correcta == respuesta_usuario:
    #    correctas += 1
    #    incorrectas = 0
    #    resultado = True
   # else:
       # incorrectas += 1
      #  correctas = 0
     #   resultado = False
  #  nivel, correctas, incorrectas = cambiar_nivel(nivel, correctas, incorrectas)
  #  return resultado
#####

#aqui si respondemos bien sumamos 1 a correctas, si no a incorrectas, si acertamos 
#3 seguidas subimos de nivel, si fallamos 3 seguidas bajamos de nivel, porahora dejemoslo asi digo
def cambiar_nivel(nivel, correctas, incorrectas):
    if correctas >= 3:
        if nivel == 'Facil':
            nivel = 'Medio'
        elif nivel == 'Medio':
            nivel = 'Dificil'
        elif nivel == 'Dificil':
            nivel = 'Experto'
        correctas = 0
    if incorrectas > 2:
        if nivel == 'Experto':
            nivel = 'Dificil'
        elif nivel == 'Dificil':
            nivel = 'Medio'
        elif nivel == 'Medio':
            nivel = 'Facil'
        incorrectas = 0
    return nivel, correctas, incorrectas

##por terminar##
def presentar_preguntas(request): 
    nivel= request.session.get('nivel', 'Experto')
    correctas= request.session.get('correctas', 0)
    incorrectas= request.session.get('incorrectas', 0)  
    if request.method == 'POST':
        respuesta_usuario= request.POST.get('respuesta')
        pregunta_id= request.POST.get('pregunta_id')
        pregunta_respondida = Question.objects.filter(id=pregunta_id).first()
        if pregunta_respondida:
            if pregunta_respondida.respuesta_correcta == respuesta_usuario:
                correctas += 1
                incorrectas = 0
            else:
                alternativa_correcta= "alternativa_" + pregunta_respondida.respuesta_correcta
                recorreccion= getattr(pregunta_respondida, alternativa_correcta)
                messages.error(request, 'Respuesta incorrecta. La respuesta correcta era: ' + recorreccion)

                incorrectas += 1
                correctas = 0
                messages.error(request, 'Respuesta incorrecta. La respuesta correcta era: ' + pregunta_respondida.respuesta_correcta)
        nivel, correctas, incorrectas = cambiar_nivel(nivel, correctas, incorrectas)
        request.session['nivel'] = nivel
        request.session['correctas'] = correctas
        request.session['incorrectas'] = incorrectas
        return redirect("presentar_preguntas")
    else: 
        
        pregunta = obtener_pregunta(nivel)
        context = {
            'pregunta': pregunta,
            'nivel': nivel,
            'correctas': correctas,
            'incorrectas': incorrectas,
        }
        
        return render(request, 'cuestionario/pregunta.html', context)


    
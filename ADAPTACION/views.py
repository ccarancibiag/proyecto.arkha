from django.shortcuts import render
from .models import Question
from random import randint
from django.shortcuts import render, redirect
from django.contrib import messages




# Create your views here.
#Vamos a definir 4 niveles de dificultad, facil-medio-dificil-experto
#iniciaremos con el nivel dificil, pues si acierta sabremos que tendra un buen nivel
#sino acertara, bajaremos a medio y luego a facil.
nivel = 'experto'
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
    nivel = request.session.get('nivel', 'Experto')
    correctas = request.session.get('correctas', 0)
    incorrectas = request.session.get('incorrectas', 0)  

    stats_tipos = request.session.get('stats_tipos', {
        'trigonometria': {'total': 0, 'correctas': 0},
        'álgebra':       {'total': 0, 'correctas': 0},
        'estadística':   {'total': 0, 'correctas': 0},
    })
    
    mostrar_pez = request.session.pop('mostrar_pez', False)
    gif_transicion = request.session.pop('gif_transicion', 'cuestionario/gifs/pez.gif')

    if request.method == 'POST':
        respuesta_usuario = request.POST.get('respuesta')
        pregunta_id = request.POST.get('pregunta_id')
        pregunta_respondida = Question.objects.filter(id=pregunta_id).first()
        nivel_anterior = nivel

        if pregunta_respondida:
            tipo = pregunta_respondida.tipo     
            if pregunta_respondida.respuesta_correcta == respuesta_usuario:
                correctas += 1
                incorrectas = 0
                messages.success(request, '¡Respuesta correcta!')
                stats_tipos[tipo]['total'] += 1
                stats_tipos[tipo]['correctas'] += 1
            else:
                alternativa_correcta = "alternativa_" + pregunta_respondida.respuesta_correcta
                recorreccion = getattr(pregunta_respondida, alternativa_correcta)
                messages.error(request, 'Respuesta incorrecta. La respuesta correcta era: ' + recorreccion)
                stats_tipos[tipo]['total'] += 1
                
                incorrectas += 1
                correctas = 0

       
        nivel, correctas, incorrectas = cambiar_nivel(nivel, correctas, incorrectas)

        if nivel != nivel_anterior:
            request.session['mostrar_pez'] = True
            transicion = {nivel_anterior, nivel}
            ruta_gif = 'cuestionario/gifs/pez.gif'

            if transicion == {'Facil', 'Medio'}:
                ruta_gif = 'cuestionario/gifs/pez_carga.gif'
            elif transicion == {'Medio', 'Dificil'}:
                ruta_gif = 'cuestionario/gifs/2_medusas.gif'
            elif transicion == {'Dificil', 'Experto'}:
                ruta_gif = 'cuestionario/gifs/pulpo_baila.gif'
            
            request.session['gif_transicion'] = ruta_gif
   
        request.session['nivel'] = nivel
        request.session['correctas'] = correctas
        request.session['incorrectas'] = incorrectas
        request.session['stats_tipos'] = stats_tipos
        return redirect("presentar_preguntas")
    
    else: 
        for tipo, datos in stats_tipos.items():
            total = datos.get('total', 0)
            correctas_tipo = datos.get('correctas', 0)
            if total == 0:
                porcentaje = 0
            else:
                porcentaje = (correctas_tipo / total) * 100
            stats_tipos[tipo] = {
                'total': total,
                'correctas': correctas_tipo,
                'porcentaje': porcentaje,
            }
        
        pregunta = obtener_pregunta(nivel)
        context = {
            'pregunta': pregunta,
            'nivel': nivel,
            'correctas': correctas,
            'incorrectas': incorrectas,
            'stats_tipos': stats_tipos,
            'mostrar_pez': mostrar_pez,
            'gif_transicion': gif_transicion,
        }
        
        return render(request, 'cuestionario/pregunta.html', context)

def reiniciar(request):
    request.session['nivel'] = 'Experto'  
    request.session['correctas'] = 0
    request.session['incorrectas'] = 0
    request.session['stats_tipos'] = {
        'trigonometria': {'total': 0, 'correctas': 0},
        'álgebra':       {'total': 0, 'correctas': 0},
        'estadística':   {'total': 0, 'correctas': 0},
    }
    return redirect("presentar_preguntas")
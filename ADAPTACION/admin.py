from django.contrib import admin
from .models import Question


# Register your models here.
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'pregunta', 'dificultad', 'respuesta_correcta', 'tipo')
    list_filter = ('dificultad',)
    search_fields = ('pregunta', 'alternativa_A', 'alternativa_B', 'alternativa_C', 'alternativa_D', 'tipo')

#Con esto hacemos que en el panel de administracion podamos ver las preguntas
#y filtrarlas por dificultad y buscar por texto en la pregunta o alternativas 
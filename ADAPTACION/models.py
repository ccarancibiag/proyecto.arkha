from django.db import models

# Create your models here.
#CREO LA CLASE DE LA BASE DE DATOS(Tipo tabla)
#que el formato sera: "id | pregunta | respuesta_correcta|alternativa A| ALTERNATIVA B| ALTERNATIVA C| ALTERNATIVA D | dificultad"
"alternativas : A|B|C|D"
#CharField indica que es texto, max_length es la longitud maxima del texto
#lo de aca abajo Hace que no haya problemas al guardar en la base de datos
UNICASRESPUESTAS=[
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
]

DIFICULTADES=[
    ('Facil', 'Facil'),
    ('Medio', 'Medio'),
    ('Dificil', 'Dificil'),
    ('Experto', 'Experto'),
] 

tipos = [
    ('trigonometria', 'trigonometria'), 
    ('álgebra', 'álgebra'), 
    ('estadística', 'estadística')]

class Question(models.Model):
    pregunta = models.TextField() #sin limite de caracteres
    respuesta_correcta = models.CharField(max_length=1, choices=UNICASRESPUESTAS)
    alternativa_A = models.CharField(max_length=255)
    alternativa_B = models.CharField(max_length=255)
    alternativa_C = models.CharField(max_length=255)
    alternativa_D = models.CharField(max_length=255)
    dificultad = models.CharField(max_length=50, choices=DIFICULTADES, db_index=True)
    tipo = models.CharField(max_length=100, choices=tipos, default='álgebra', db_index=True)
#db_index=True hace que se pueda buscar mas rapido en la base de datos por ese campo
#Como vamos anadir cosas manualmentea la base de datos desde admin no hace falta __str__
def __str__(self):
    return "[" + self.dificultad + "] " + self.pregunta[:50]








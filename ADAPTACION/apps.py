from django.apps import AppConfig

class AdaptacionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ADAPTACION'
    #default_auto_field sirve para que al crear nuevas tablas en la base de datos
    #y le puse el nombre de ADAPTACION, IMPORTANTE QUE NO SE PUEDE ESCRIBIR CON MINUSCULAS
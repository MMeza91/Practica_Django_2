# Trabajando con Django
Pequeño manual de primeros pasos para trabajar con Django.

## crear entorno virtual:
`python -m venv entorno_virtual`

(-m indica que el comando que se ocupara con Python, trabaja de forma global)

PD: Se recomienda ingresar la carpeta creada "entorno_virtual" dentro de `.gitignore`
PD2: en `.gitignore` escribir tambien "*__pycache__" para que sin importar dentro de que carpeta se encuentre, ningun pycache se guarde en el repositorio 

## activar entorno virtual
[Para Unix] `source entorno_virtual/bin/actívate`

[Para Windows] `. .\entorno_virtual\scripts\activate`

## Requerimientos del proyecto
*crear archivo "requirements.txt", dentro de esto puedo ingresar todos los programas que necesito durante el desarrollo del programa. Como por ejemplo:
*	django
*	pillow

`pip install -r requirements.txt`

## Creación del Proyecto
`django-admin startproject proyecto_Django .`

Esta es la estructura donde se hechará a andar nuestras aplicaciones

### Modulos del proyecto
* `__init__.py`
* `asgi.py`: Encargado de recibir las peticiones de los usuarios. (Servidor web embebido dentro del framework)  
* `settings.py`: Configuraciones del proyecto y de la base de datos que se utiliza.
    * `ALLOWED_HOST = ['*']` (Se entrega las direcciones ip de los servidores con los que se interactuará, incluyendo nuestro local)
    * `INSTALLED_APPS = ["....",]` (Se conectan las aplicaciones que se van creando para que el proyecto en si, sepa de la existencia de las otras aplicaciones, por default vienen las aplicaciones base del framework)
* `urls.py`: las rutas de las paginas para que el controlador sepa a donde debe redirigir.
* `wsgi.py`: Encargado de redireccionar las peticiones de los usuarios. (Servidor web embebido dentro del framework)

## Migración de modelos a tablas de la base de datos

Para realizar las migraciones se utilizan 2 comandos:
* `python manage.py makemigrations` (prepara la migración sin crear las tablas, es decir, verifica si hay modelos que deban ser migradosde todo el proyecto y aplicaciones)
    + Se puede escribir para cada solo realizar la migración en una aplicación y quedaria: `python manage.py makemigrations nombre_aplicacion`

+ `python manage.py migrate` (aplico los modelos de django como tablas en la base de datos)

## Crear la cuenta de administrador
`python manage.py createsuperuser`

## Hacer correr el Servicio/server
`python manage.py runserver` (hecho andar el servidor)

Ahora que el servidor está corriendo, puedo entrar a la pagina/admin (back-office) con el usuario creado como super usuario y su contraseña, para crear grupos y usuarios
 
## Crear carpeta contenedora de templates
Se crea carpeta para ir guardando los html que se creen, se recomienda en caso de tener varias aplicaciones, ir guardando en sub_carpetas para mantenerlas ordenadas.

Dentro del archivo `settings.py` de la carpeta del proyecto, en la sección `TEMPLATES`, agregar dentro de los parentesis cuadrados de `"DIRS"` la dirección de la carpeta de templates quedando `[BASE_DIR / "templates"]`


## Crear una aplicación
`python manage.py startapp nombre_aplicacion`

### Crear archivo `urls.py` dentro de la aplicación.

Se crea el archivo y se copia en su interior la misma información que está en el archivo `urls.py` del proyecto, como la importación de `path` y la forma de escribir las urls
path("ruta", función,  )

### Modulos de una aplicación
* Carpeta `migrations`: Los modelos creados desde la aplicación se depositan en esta carpeta, es un versionador de los modelos en la db
* `__init__.py`: le dice a python que es un modulo
* `admin.py`: Espacio donde se registran los modelos para que aparezcan en la pagina/admin (back-office)
* `apps.py`: Lugar para configurar la aplicacion y su relación con la base de datos
* `models.py`: Lugar donde se crean los modelos de las tablas a utilizar
* `test.py`: Se crean los testeos de nuestras funciones, entre otros
* `views.py`: El controlador de las vistas
* `urls.py`: archivo creado para manejar de forma interna las páginas asociadas exclusivamente a la aplicación.

## Realizar link entre aplicación y proyecto

En el archivo `settings.py` de la carpeta `Proyecto`, en la configuración de `INSTALLED_APPS` se agrega `"nombre_aplicacion",` (la coma final debe estar)

Esto se realiza para que el proyecto sepa la existencia de la aplicación.

## Crear modelos de la aplicación (Primera Parte)

Dentro del archivo `models.py` perteneciente a la aplicación, se crean clases para poder trabajar con el ORM y la base de datos, Cada clase es una tabla y dentro de la clase se escriben las columnas de la tabla con las caracteristicas de los datos y sus restricciones. Ejemplo:

    class Nombre_tabla(models.Model):
        nombre_columna_1 = models.CharField("nombre_columna_1", max_length=40)
        nombre_columna_2 = models.CharField("nombre_columna_2", max_length=40)

        def __str__(self):
            return f"{self.nombre_columna_1}"

Una vez que se construye el modelo se escriben los comandos de migración visto anteriormente, este proceso se debe realizar cada vez que se crea una nueva tabla o que se modifica una tabla.

## agregar modelos a carpeta de administración

Primero importamos el modelo 

    from .models import Nombre_tabla

y agregamos la tabla como una clase

    @admin.register(nombre_tabla)
    class Nombre_tabla_Admin(admin.ModelAdmin):
        pass

Esto permite poder agregar y eliminar filas en la base de datos en el backoffice (pagina www.sdfsdf.cl/admin)

## Crear funciones de visualización en el controlador

Dentro del archivo `views.py` dentro de la carpeta de la aplicación, importamos el modelo que estamos utilizando de ser necesario y creamos la función para la vista, quedando:

    import .models import Nombre_tabla
    def nombre_funcion_relacionada_a_la_pagina_web(request):
        nombre_variable = Nombre_tabla.objets.all()
         # esta es una query hecha para trabajar con el ORM de Django
        return render(request, 'pagina_web.html', { 'accion' : nombre_variable})

donde `request` es la petición del usuario

donde `render` es la función que "renderiza/dibuja" la pagina web con la información entregada en el request por parte del usuario.

donde {} es el diccionario que tiene el contexto de la petición

## Generar el nexo entre el controlador y las vistas

En el archivo creado de `urls.py` dentro de la aplicación, hacemos el nexo entre la función del controlador y la ruta que tendrá en la pagina web. quedando
    
    path("ruta_que_se_agrega_al_link", nombre_funcion_relacionada_a_la_pagina_web, name='nombre_para_django')

## Generar el nexo entre las vistas de la aplicación y del controlador

En el archivo `urls.py` del proyecto se realizan las siguientes modificaciones:
* En la importación de `path` se agrega `include` quedando: `from django.urls import path, include`

* En la lista `urlpatterns` agregar la dirección a la aplicación quedando:  
    
        `urlpatterns = [
            path("admin/", admin.site.urls),
            path("nombre_aplicacion", include("nombre_aplicacion.urls"))
        ]`

## Creando acciones adicionales en los html del template

Para poder ejecutar código python en la pagina web, se debe escribir cierto codigo estructurado por `Jinja` (https://jinja.palletsprojects.com/en/stable/)

    {%for columna in accion%}
        {{accion.nombre_columna_1}}
    {% endfor %}
    
    {% load statics %}

    {% include 'pagina_web.html' %}


## Crear modelos de la aplicación (Segunda parte)

Cuando debemos trabajar con imagenes y archivos, se deben configurar ciertas acciones adicionales.

Primero en el archivo de `models.py` agregamos la variable, como por ejemplo:

    imagen = models.ImageField("imagen", upload_to="productos/", blank=True, null=True)

Que significaría que la imagen se cargará en la carpeta "productos" y que puede ser blanco o nulo, ideal cuando se hace una modificación al modelo ya teniendo datos en el interior, así no genera error al generar la migración.

Segundo, configuramos el archivo `settings.py`. 
Al final, abajo el comando escrito de "`STATIC_URL`" se agregan:
* `MEDIA_URL = "/media/"`  (Esto es lo que se ve en la url al ver la imagen/archivo)
* `MEDIA_ROOT = BASE_DIR / "media"` (De donde irá a buscar la imagen/archivo)

Tercero, configuramos la dirección a utilizar durante el periodo de desarrollo o de "debug" en el archivo `urls.py` del proyecto. Para lo cual primero se importan:

* `from django.conf.urls.static import static`
* `from django.conf import settings`

Ahora en el mismo archivo, al final se agrega:

    if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=MEDIA_ROOT)

Ya teniendo los archivos modificados y el modelo modificado, se vuelve a migrar el modelo con los comandos `makemigrations` y `migrate`.

## Creando El CRUD (Create, Read, Update, Delete) para cada modelo

Este proceso puede ser por medio de funciones o de clases, a continuación trabajaremos con clases, en el archivo `views.py` de la aplicación.

### Leer

Se importa `from django.views.generic import ListView` y se agrega la clase para la lectura que hereda de `ListView`

    class Nombre_ModeloListView(ListView):
        model = Nombre_del_modelo_que_se_listara
        template_name = "plantilla_que_renderiza_el_listado_de_items_del_modelo.html"
        context_object_name = "nombre_de_contenido_o_modelo"

### Detallar

Se importa `from django.views.generic import DetailView` y se agrega la clase para detalle que hereda de `DetailView`

    class Nombre_ModeloDetailView(DetailView):
        model = Nombre_del_modelo_que_se_detallara
        template_name = "plantilla_que_renderiza_el_detalle_del_articulo_del_modelo.html"
        context_object_name = "nombre_de_contenido_o_modelo"

### Crear

Se importa `from django.views.generic import CreateView` y `from django.urls import reverse_lazy` y se agrega la clase para crear que hereda de `CreateView`

    class Nombre_ModeloDCreateView(CreateView):
        model = Nombre_del_modelo_que_se_detallara
        template_name = "plantilla_con formulario_para agregar_información_al_modelo.html"
        field = ['Variables','del','modelo','que se','necesita','ingresar']
        success_url = reverse_lazy("pagina_donde_se_redirige_una_vez_que_se_completa_la_tarea")

### Actualizar

Se importa `from django.views.generic import UpdateView` y `from django.urls import reverse_lazy` y se agrega la clase para detalle que hereda de `UpdateView`

    class Nombre_ModeloUpdateView(UpdateView):
        model = Nombre_del_modelo_que_se_actualizara
        template_name = "plantilla_con formulario_para agregar_información_al_modelo.html"
        field = ['Variables','del','modelo','que se','necesita','ingresar']
        success_url = reverse_lazy("pagina_donde_se_redirige_una_vez_que_se_completa_la_tarea") 

### Borrar

Se importa `from django.views.generic import DeleteView` y `from django.urls import reverse_lazy` el que me permite redirigir a una pagina después que la acción se complete y se agrega la clase para detalle que hereda de `DeleteView`

    class Nombre_ModeloDeleteView(DeleteView):
        model = Nombre_del_modelo_que_se_detallara
        template_name = "plantilla_que_renderiza_la confirmacion_de_borrar_item_d el_modelo.html"
        success_url = reverse_lazy("pagina_donde_se_redirige_una_vez_que_se_completa_la_tarea")


Una vez creadas las clases, se crean los templates necesarios para realizar las tareas del CRUD. Como con todo HTML nuevo, se debe realizar la conexión de las templates creadas con el archivo `urls.py` de la aplicación. 

En este archivo se debe importar las clases del CRUD desde `.views` y la path de las estas clases se agrega `.as_view()`, quedando:

    path("direccion/", Nombre_ClaseListView.as_view(), name="lista_items"),


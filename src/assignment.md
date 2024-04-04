# Funcionalidades básicas:
1. Desde la página de inicio recorrer todas las páginas almacenando: titulo (cuidado
elipsis “…”), calificación, precio, ruta a la ficha del libro.

    * Hacer diccionario con ID unica, los datos de los atributos y la ruta.

2. Desde la página de inicio recorrer todas las páginas y extraer todas las rutas a las fichas
de libros.

    * Iterar con lo de arriba

3. Desde la página principal extraer todas las categorías disponibles.
    *   Iterador de categorias
4. Dada una categoría extraer los nombres de los libros de dicha categoría.
    *   Mapear un diccionario al otro
5. Dada la ruta de una ficha obtener todos los datos del libro, incluyendo la ruta de la
imagen y los nombres de los libros asociados.

    * Mejor ruta de imagen que la imagen como tal 

6. Dado el nombre de un libro localizar la ruta de su ficha
    * Utilizar el mapeado

# Se pide:
Construye un programa de consola en Python que a través de un menú permita realizar las
siguientes operaciones sobre la web.

* Descargar una lista con los libros disponibles (información básica).
    * A disco
* Indicada una categoría descargar una lista con los libros disponibles (información
básica).
    * Bucle de lo de arriba
* Indicado un título de libro descargar la ficha.
* Descargar las fichas completas de todos los libros.
* Descargar las fichas completas de todos los libros incluyendo su categoría.
* Indicada una valoración descargar una lista con los libros disponibles (información
básica) cuya calificación sea igual o superior.
* Indicado un rango de precios, mínimo y máximo, descargar una lista con los libros
disponibles (información básica) cuyo precio se incluya en dicho rango.
* Permite seleccionar el formato de salida, json, csv, html.
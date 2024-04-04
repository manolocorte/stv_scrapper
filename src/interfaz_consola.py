from colorama import Fore, Style
from scrapper import Scrapper
class InterfazConsola:
    def __init__(self):
        self.formato_seleccionado = "json"
        self.respuestaActual = None
        self.scrapper = Scrapper()
        self.lista_nombres = None
        self.rating_min = None
        self.rating_max = None
        self.price_min = None
        self.price_max = None
        self.book_category_names = None

    def main_menu(self):
        exit = True 
        while exit:
            print(Fore.CYAN + Style.BRIGHT + "                  STV SCRAPPER                      ")
            print(Fore.YELLOW + "===================================================")
            print(Fore.GREEN + "0- Descargar una lista con las categorías disponibles")
            print(Fore.GREEN + "1- Descargar una lista con los libros disponibles")
            print(Fore.GREEN + "2- Descargar libros de una categoría")
            print(Fore.GREEN + "3- Descargar ficha de libro")
            print(Fore.GREEN + "4- Descargar las fichas completas de todos los libros")
            print(Fore.GREEN + "5- Descargar todos los libros superiores a valoración")
            print(Fore.GREEN + "6- Descargar todos los libros dentro de rango de precio")
            print(Fore.BLUE + f"7- Seleccionar formato de output (Actual es {self.formato_seleccionado})")
            print(Fore.RED + "8- Salir")
            print(Style.RESET_ALL + "\n \n \n")
            self.respuestaActual = input(Fore.YELLOW + "siguiente-chatarreo:" + Style.RESET_ALL)  # Python 3
            if self.respuestaActual != '8':
                self.respuesta()         
            else :
                exit = False

    def respuesta(self):
            if self.respuestaActual == '0':
                print("Ha entrado a la opción 0")
                self.scrapper.get_categorias_libros()
                self.book_category_names = list(self.scrapper.book_categories.keys())
            elif self.respuestaActual == '1':
                self.scrapper.get_nombre_libros()
                self.lista_nombres =  self.scrapper.book_names
            elif self.respuestaActual == '2':
                self.descargar_categoria()
            elif self.respuestaActual == '3':
                self.descargar_ficha_libro()
            elif self.respuestaActual == '4':
                self.scrapper.mapear(self.formato_seleccionado, completo=True)
            elif self.respuestaActual == '5':
                self.descargar_rating()
            elif self.respuestaActual == '6':
                self.descargar_rango_precio()
            elif self.respuestaActual == '7':
                self.seleccionar_ouput()                
            else :
                print("\nError en la opción seleccionada. Por favor introduzca una válida.")

    def seleccionar_ouput(self):
        salir = False
        while not salir:
            print(Fore.CYAN + Style.BRIGHT + "                  SELECCIONAR OUTPUT                   ")
            print(Fore.YELLOW + "===================================================")
            print(Fore.GREEN + "1- JSON")
            print(Fore.GREEN + "2- CSV")
            print(Fore.GREEN + "3- HTML")
            print(Fore.RED + "0- Volver")
            print(Style.RESET_ALL + "\n \n \n")
            respuesta_output = input(Fore.YELLOW + "siguiente-chatarreo:" + Style.RESET_ALL)  # Python 3

            if respuesta_output == '1':
                output = 'json'
                salir = True
                break
            elif respuesta_output == '2':
                output = 'csv'
                salir = True
                break
            elif respuesta_output == '3':
                output = 'html'
                salir = True
                break
            elif respuesta_output == '0':
                salir = True
                break
            else :
                print("\nError en la opción seleccionada. Por favor introduzca una válida.")

        self.formato_seleccionado = output


    def descargar_rango_precio(self):
        salir = False
        while not salir:
            print(Fore.BLUE + f"1- Cambiar precio mínimo (Actual es {self.price_min}):")
            print(Fore.BLUE + f"2- Cambiar precio máximo (Actual es {self.price_max}):")
            print(Fore.GREEN + f"3- Descargar libros en rango:")
            print(Fore.RED + "0- Volver")
            print(Style.RESET_ALL + "\n \n \n")
            respuesta_output = input(Fore.YELLOW + "siguiente-chatarreo:" + Style.RESET_ALL)  # Python 3

            if  respuesta_output == '0':
                salir = True
                break
            elif  respuesta_output == '1':
                respuesta_output = input(Fore.YELLOW + "precio mínimo:" + Style.RESET_ALL)  # Python 3
                if respuesta_output.isdigit():
                    self.price_min = respuesta_output
                
            elif  respuesta_output == '2':
                respuesta_output = input(Fore.YELLOW + "precio máximo:" + Style.RESET_ALL)  # Python 3
                if respuesta_output.isdigit():
                    self.price_max = respuesta_output
                
            elif  respuesta_output == '3':
                if self.price_min.isdigit() and self.price_max.isdigit():
                    self.scrapper.mapear( self.formato_seleccionado, min_price=self.price_min, max_price=self.price_max)
            else :
                print("\nError en la opción seleccionada. Por favor introduzca una válida.")

    def descargar_ficha_libro(self):
        salir = False
        if not self.scrapper.book_names:
            print(Fore.RED + "No hay libros disponibles, por favor seleccione la opción 1 para obtener la lista de libros disponibles")
            return
        
        print(Fore.BLUE + "Lista de libros disponibles:")
        for book in self.scrapper.book_names:
            print(Fore.YELLOW + book)
        while not salir:
            print(Fore.BLUE + " Por favor introduzca el nombre de el libro deseado (tiene que ser el nombre completo):")
            print(Fore.RED + "0- Volver")
            print(Style.RESET_ALL + "\n \n \n")
            respuesta_output = input(Fore.YELLOW + "siguiente-chatarreo:" + Style.RESET_ALL)  # Python 3

            if respuesta_output == '0':
                salir = True
                break
            elif respuesta_output.lower() not in self.scrapper.book_names:
                print(Fore.RED + "el libro no se encuentra en la lista, por favor introduzca un libro válido")
            else :
                print(Fore.GREEN + "Descargando ficha de libro...")
                self.scrapper.mapear(self.formato_seleccionado,completo=True,specific_name=respuesta_output.lower())

    def descargar_categoria(self):
        salir = False
        if not self.book_category_names:
            print(Fore.RED + "No hay libros disponibles, por favor seleccione la opción 0 para obtener la lista de categorias disponibles")
            return
        while not salir:
            print(Fore.BLUE + " Por favor introduzca el nombre de la categoria deseada (tiene que ser el nombre completo):")
            print(Fore.BLUE + "Lista de categorias disponibles:")
            for category in self.book_category_names:
                print(Fore.YELLOW + category)
            print(Fore.RED + "0- Volver")
            print(Style.RESET_ALL + "\n \n \n")
            respuesta_output = input(Fore.YELLOW + "siguiente-chatarreo:" + Style.RESET_ALL)  # Python 3

            if respuesta_output == '0':
                salir = True
                break
            elif respuesta_output.lower() not in self.book_category_names:
                print(Fore.RED + "La categoria no se encuentra en la lista, por favor introduzca una válida")
                print(category.BLUE + "Lista de categorías disponibles:")
                for book in self.book_category_names:
                    print(Fore.YELLOW + category)
                break
            elif respuesta_output.lower() in self.book_category_names:
                Scrapper.get_categoria(self.scrapper,respuesta_output.lower(),output_format=self.formato_seleccionado,completo=True)
                salir = True
                break
            else :
                print("\nError en la opción seleccionada. Por favor introduzca una válida.")



    def descargar_rating(self):
        salir = False
        while not salir:
            print(Fore.BLUE + f"1- Cambiar rating mínimo (Actual es {self.rating_min}):")
            print(Fore.BLUE + f"2- Cambiar rating máximo (Actual es {self.rating_max}):")
            print(Fore.GREEN + f"3- Descargar libros en rango:")
            print(Fore.RED + "0- Volver")
            print(Style.RESET_ALL + "\n \n \n")
            respuesta_output = input(Fore.YELLOW + "siguiente-chatarreo:" + Style.RESET_ALL)  # Python 3

            if  respuesta_output == '0':
                salir = True
                break
            elif  respuesta_output == '1':
                respuesta_output = input(Fore.YELLOW + "rating mínimo:" + Style.RESET_ALL)  # Python 3
                if respuesta_output.isdigit():
                    self.rating_min = respuesta_output
            elif  respuesta_output == '2':
                respuesta_output = input(Fore.YELLOW + "rating máximo:" + Style.RESET_ALL)  # Python 3
                if respuesta_output.isdigit():
                    self.rating_max = respuesta_output
            elif  respuesta_output == '3':
                if self.rating_min.isdigit() and self.rating_max.isdigit():
                    self.scrapper.mapear(self.formato_seleccionado, min_rating=self.rating_min, max_rating=self.rating_max)
                else:
                    print(Fore.RED + "Por favor introduzca un rating válido")
            else :
                print("\nError en la opción seleccionada. Por favor introduzca una válida.")





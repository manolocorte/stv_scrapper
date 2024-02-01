class InterfazConsola:
    formato_seleccionado = "json"
    respuestaActual =  None
    def main_menu(self):
        exit = True 
        while exit:
            print("                  STV SCRAPPER                      ")
            print("===================================================")
            print("1- Descargar una lista con los libros disponibles")
            print("2- Descargar libros de una categoría")
            print("3- Descargar ficha de libro")
            print("4- Descargar las fichas completas de todos los libros")
            print("5- Descargar todos los libros superiores a valoración")
            print("6- Descargar todos los libros dentro de rango de precio")
            print("7- Seleccionar formato de output")
            print("8- Salir")
            print("\n \n \n") 
            respuestaActual = input("siguiente-chatarreo:")  # Python 3
            
            print(f"La respuesta es {respuestaActual}")
            if respuestaActual == 1:
                self.descargar_todos_basico()
            elif respuestaActual == 2:
                self.descargar_categoria()
            elif respuestaActual == 3:
                self.descargar_ficha_libro()
            elif respuestaActual == 4:
                self.descargar_fichas_completas()
            elif respuestaActual == 5:
                self.descargar_rating()
            elif respuestaActual == 6:
                self.descargar_rango_precio()
            elif respuestaActual == 7:
                self.seleccionar_ouput()                
            elif respuestaActual == 8:
                exit = False
            else :
                print("\nError en la opción seleccionada. Por favor introduzca una válida.")
                



 
    # default constructor
    def __init__(self,formato_seleccionado='json'):
        pass

    def descargar_todos_basico():
        pass
    
    def descargar_categoria(self):
        pass
    
    def descargar_ficha_libro(self):
        pass
    
    def descargar_rating(self):
        pass
    
    def descargar_rango_precio(self):
        pass
    
    def descargar_fichas_completas(self):
        pass
    
    def seleccionar_ouput(self):
        pass
    
    def seleccionar_output(self):
        exit = False 
        respuestaActual =  None
        formato_seleccionado = "json"
        while not exit:
           #json, csv, html. 
            print("               Formatos disponibles                      ")
            print("===================================================")
            print("1- Json")
            print("2- CSV")
            print("3- HTML")
            print("4- Volver")
            print(f"\nEl formato actual de ouput es {formato_seleccionado}")
            print("\n \n \n") 
            self.respuestaActual = input("siguiente-chatarreo:")  # Python 3
            
            
            if respuestaActual == 1:
                self.formato_seleccionado = "json"
            elif respuestaActual == 2:
                self.formato_seleccionado = "csv"
            elif respuestaActual == 3:
                self.formato_seleccionado = "html"
            elif respuestaActual == 4:
                break
            else :
                print("\nError en la opción seleccionada. Por favor introduzca una válida.")
    

    
    
class data_box:
    id = "default"
    nombre = "default"
    rating = -1
    precio = -1
    ruta_ficha = "default"
    categoria = "default"

    outputs =['json','csv','html']  
    
    def __init__(self, datos):
        self.id = datos['id']
        self.nombre = datos['nombre']
        self.rating = datos['rating']
        self.precio = datos['precio']
        self.ruta_ficha = datos['ruta_ficha']
        self.categoria = datos['categoria']
        
    def export(self,output):
        if output not in self.outputs:
            print("Formato de salida aportado no válido, por favor intente otro")
        elif "json" in output:
            pass
        else:
            pass
    

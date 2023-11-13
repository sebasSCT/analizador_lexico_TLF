import tkinter as tk
from tkinter import ttk
from logica.Analizador import Analizador

class Ventana:
    def __init__(self, nombre, geometria):
        self.nombre = nombre
        self.geometria = geometria

        self.texto = None
        self.tabla = None

    def iniciarVentana (self):

        # Crear la ventana
        ventana = tk.Tk()
        ventana.title(self.nombre)
        ventana.geometry(self.geometria)

        # Crear un widget de texto
        texto = tk.Text(ventana, width=55, height=15)
        texto.pack(pady=10)

        # Crear un botón para obtener el texto ingresado
        # Obtenemos el texto desde la línea 1, carácter 0 hasta el final, excluyendo el último carácter (que es una línea en blanco)
        boton_obtener = tk.Button(ventana, text="Analizar", command= self.getCodigo(texto.get("1.0","end-1c")) )
        boton_obtener.pack(pady=10)

        # Crear una etiqueta para mostrar el resultado
        etiqueta_resultado = tk.Label(ventana, text="")
        etiqueta_resultado.pack(pady=10)

        # Crear una tabla (Treeview)
        columnas = ("Token","Lexema", "Categoría", "Posición")
        self.tabla = ttk.Treeview(ventana, columns=columnas, show="headings", selectmode="browse")

        for columna in columnas:
            self.tabla.heading(columna, text=columna)

        self.tabla.pack(pady=10)

        # Iniciar el bucle de eventos
        ventana.mainloop()

    def getCodigo(self, codigo):
        self.texto = codigo

        token = Analizador.analizar(self.texto)

        #self.agregar_fila(token)
        

    def agregar_fila(self, token):
        columna1 = token[0] 
        columna2 = token[1] 
        columna3 = token[2] 
        columna4 = token[3]
        self.tabla.insert("", "end", values=(columna1, columna2, columna3, columna4))



    

    



    

  
    

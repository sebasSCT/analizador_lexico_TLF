import tkinter as tk
from tkinter import ttk
from Analizador import Analizador

# Clase con la que se inicia la ventana y sus elementos
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
        boton_obtener = tk.Button(ventana, text="Analizar", command=lambda: self.getCodigo(texto.get("1.0","end-1c"), ventana))
        boton_obtener.pack(pady=10)

        # Crear una etiqueta para mostrar el resultado
        etiqueta_resultado = tk.Label(ventana, text="Tokens")
        etiqueta_resultado.pack(pady=10)

        # Iniciar el bucle de eventos
        ventana.mainloop()

    # Accion del boton
    def getCodigo(self, codigo, ventana):
        self.texto = codigo

        print(codigo)
        
        a = Analizador()
        tokens = a.analizar(self.texto)

        if self.tabla:
            self.tabla.destroy()

        self.tabla =self.crearTabla(ventana, tokens)
        
    
    def crearTabla (self, ventana, tokens):
        
        # Crear una tabla (Treeview)
        columnas = ("Palabra", "Categoría", "Posición")
        tabla = ttk.Treeview(ventana, columns=columnas, show="headings", selectmode="browse")

        # Agregar las columnas a la tabla
        for columna in columnas:
            tabla.heading(columna, text=columna)

        tabla.pack(pady=10)

        #Agregar tokens extraidos a la tabla
        for token in tokens:
            self.agregar_fila(token, tabla)

        return tabla
        
    # Funcion para agregar los tokens a la tabla
    def agregar_fila(self, token, tabla):
        columna1 = token.palabra
        columna2 = token.categoria.to_string()
        columna3 = 'Línea: ' + str(token.posicion[0]) + ' Columna: ' + str(token.posicion[1])
        
        tabla.insert("", "end", values=(columna1, columna2, columna3))
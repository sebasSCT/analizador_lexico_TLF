from enum import Enum

class Categoria (Enum):
    NO_RECONOCIDO = 1
    ENTERO = 2
    DECIMAL = 3
    IDENTIFICADOR = 4
    PALABRA_RESERVADA = 5
    CADENA_CARACTERES = 6
    COMENTARIO_LINEA = 7
    COMENTARIO_BLOQUE = 8
    OPERADOR_ARITMETICO = 9
    OPERADOR_COMPARACION = 10
    OPERADOR_LOGICO = 11
    OPERADOR_INCREMENTO = 12
    OPERADOR_DECREMENTO = 13
    APERTURA_PARENTESIS = 14
    CIERRE_PARENTESIS = 15
    APERTURA_LLAVES = 16
    CIERRE_LLAVES = 17
    TERMINAL = 18
    SEPARADOR = 19
    HEXADECIMAL = 20
    OPERADOR_ASIGNACION = 21

    def to_string(self):
        
        return f"{self.name}"
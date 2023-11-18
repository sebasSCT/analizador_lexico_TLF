from modelo.Token import Token
from modelo.Categoria import Categoria

#Clase en la que se analiza el codigo retornando los tokens encontrados
class Analizador:
    def __init__(self):
        
        self.tokens = []
        self.codigo = ""
        self.indice = 0
        self.matriz = []

        #Palabras reservadas
        self.reservadas0 = ['tarea', 'clase']
        self.reservadas1 = [ 'A', 'R', 'P']
        self.reservadas2 = ['ent', 'dob', 'car', 'v', 'f']
        self.reservadas3 = ['si', 'sino', 'bucle']

        # Operadores de comparación
        self.comparacion0 = ['mayor', 'menor', 'igual', 'diferente']

    #Metodo principal
    def analizar (self, codigo):

        self.codigo = codigo
        self.iniciarMatriz(codigo)
        
        print(repr(self.codigo))

        # Se recorre el codigo fuente y se guardan los tokens que devuelve en cada iteracion
        while self.indice < len(self.codigo):

            self.tokens.append(self.extraerToken())
            self.indice += 1
        
        # Se eliminan los tokens que esten nulos (None)
        for token in self.tokens:
            if token is None: self.tokens.remove(token)
    
        return self.tokens

    # clase en la que se comprueba la categoria de los tokens encontrados
    def extraerToken (self):

        # extraer Entero
        Token = self.entero()
        if Token != None: return Token
        
        # extraer Decimal
        Token = self.decimal()
        if Token != None: return Token

        # extraer Identificador
        Token = self.identificadores()
        if Token != None: return Token

        # extraer reservadas
        Token = self.reservadas()
        if Token != None: return Token

        #extraer operadores aritmeticos
        Token = self.aritmeticos()
        if Token != None: return Token

        #extraer operadores comparacion
        Token = self.comparacion()
        if Token != None: return Token

        #extaer operadores logicos
        Token = self.logicos()
        if Token != None: return Token

        # extraer operadores de asignacion
        #Token = self.asignacion()
        #if Token != None: return Token

        # extraer operadores de incremento/decremento
        #Token = self.incdec()
        #if Token != None: return Token

        # No reconocido
        return self.noReconocido()

    def logicos (self):

        if (self.codigo[self.indice].isalpha()):

            inicio = self.indice

            if self.codigo[self.indice] in ('y', 'o'):
                return Token(self.codigo[inicio:self.indice + 1], Categoria.OPERADOR_LOGICO, self.posicion(inicio))
            if self.indice + 1 < len(self.codigo):
                if self.codigo[inicio] == 'n' and self.codigo[self.indice + 1] == 'o':
                    self.indice += 1
                    return Token(self.codigo[inicio:self.indice + 1], Categoria.OPERADOR_LOGICO, self.posicion(inicio))
        
        return None
            
    def comparacion (self):
        
        if (self.codigo[self.indice].isalpha()):

            inicio = self.indice

            for op in self.comparacion0:
                if (self.indice + len(op) < len(self.codigo) and self.codigo[inicio: inicio + len(op)]) == op:
                    self.indice += len(op)
                    if (self.codigo[self.indice] == '>'):
                        return Token(self.codigo[inicio:self.indice + 1], Categoria.OPERADOR_RELACIONAL, self.posicion(inicio))

        return None
    
    def aritmeticos (self):
        
        if self.codigo[self.indice] in ('+', '-', '*', '/'):
            return Token(self.codigo[self.indice], Categoria.OPERADOR_ARITMETICO, self.posicion(self.indice))

        return None
    
    def reservadas (self):

        if self.codigo[self.indice] in ('_', '/', '#', '~'):

            inicio = self.indice
            valido = False

            match (self.codigo[self.indice]):
                case '_':
                    for ind in self.reservadas0:
                        if self.codigo[inicio + 1: inicio + 1 + len(ind)] == ind:
                            self.indice += len(ind)
                            valido = True
                case '/':
                    if self.indice == len(self.codigo) - 1 and self.codigo[self.indice + 1] != '/':
                        return None
                    for ind in self.reservadas1:
                        if self.codigo[inicio + 2: inicio + 2 + len(ind)] == ind:
                            self.indice += len(ind) + 1
                            valido = True
                case '#':
                    for ind in self.reservadas2:
                        if self.codigo[inicio + 1: inicio + 1 + len(ind)] == ind:
                            self.indice += len(ind)
                            valido = True
                case '~':
                    for ind in self.reservadas3:
                        if self.codigo[inicio + 1: inicio + 1 + len(ind)] == ind:
                            self.indice += len(ind)
                            valido = True

            return Token(self.codigo[inicio:self.indice + 1], Categoria.PALABRA_RESERVADA, self.posicion(inicio)) if valido else None
        
        return None

    def identificadores (self):
        
        if self.codigo[self.indice] == '@':
            inicio = self.indice

            if not self.codigo[self.indice + 1].isalpha() : return None
            self.indice += 1

            while self.indice < len(self.codigo) and self.es_ascii(self.codigo[self.indice]):
                if self.codigo[self.indice] in (' ', '@', '\n'): 
                    self.indice -= 1
                    break
                self.indice += 1

            if len(self.codigo[inicio: self.indice]) > 9:
                self.indice = inicio
                return None

            return Token(self.codigo[inicio:self.indice + 1], Categoria.IDENTIFICADOR, self.posicion(inicio))
        
        return None

    def decimal (self):
        
        if self.codigo[self.indice].isdigit():
            
            inicio = self.indice

            while self.indice < len(self.codigo) and self.codigo[self.indice].isdigit():

                self.indice += 1
            
            if self.codigo[self.indice] == ',':
                self.indice += 1

                while self.indice < len(self.codigo) and self.codigo[self.indice].isdigit():

                    self.indice += 1
            
            return Token(self.codigo[inicio:self.indice], Categoria.DECIMAL, self.posicion(inicio))
    
        return None       

    def entero (self):

        if self.codigo[self.indice].isdigit():
            
            inicio = self.indice
            while self.indice < len(self.codigo) and self.codigo[self.indice].isdigit():
                if self.indice + 1 < len(self.codigo) and self.codigo[self.indice + 1] == ',':
                    self.indice = inicio
                    return None
                self.indice += 1
            
            return Token(self.codigo[inicio:self.indice], Categoria.ENTERO, self.posicion(inicio))

        return None

    def noReconocido (self):

        if self.codigo[self.indice] in (' ', '\n', '\t') :
            if self.indice < len(self.codigo) - 1:
                self.indice += 1
                return self.extraerToken()
            return None
        else:
            return Token(self.codigo[self.indice:self.indice+1], Categoria.NO_RECONOCIDO, self.posicion(self.indice))
        
        return False
    
    # funcion para comprobar si el caracter ingresado pertenece a ASCII
    def es_ascii (self, caracter):
        
        try:

            valor_ascii = ord(caracter)

            return 0 <= valor_ascii <= 127
        except TypeError:
            return None

    # se inica la matriz que representa numericamente la posicion de los caracteres del codigo
    def iniciarMatriz (self, codigo):
        
        aux = []

        for i in range(len(codigo)):
            if codigo[i] == '\n':
                self.matriz.append(aux[:])
                aux.clear()
                continue
            aux.append(i)

        self.matriz.append(aux)

    # busca la posicion del indice en la matriz que representa al codigo
    def posicion (self, indice):

        for i in range (len(self.matriz)):
            for j in range (len(self.matriz[i])):
                if self.matriz[i][j] == indice:
                    return [i + 1, j + 1]
            
            
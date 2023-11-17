from modelo.Token import Token
from modelo.Categoria import Categoria

class Analizador:
    def __init__(self):
        
        self.tokens = []
        self.codigo = ""
        self.indice = 0
        self.matriz = []

       

    def analizar (self, codigo):

        self.codigo = codigo
        self.iniciarMatriz(codigo)
        
        print(repr(self.codigo))

        while self.indice < len(self.codigo):

            self.tokens.append(self.extraerToken())
            self.indice += 1
        
        for token in self.tokens:
            if token is None: self.tokens.remove(token)
    
        return self.tokens

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

        # No reconocido
        return self.noReconocido()

   

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
            
            
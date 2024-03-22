# -*- coding: utf-8 -*-
'''
    Aitana Martínez Rey: aitana.martinez@udc.es
    Uxío Merino Currás: uxio.merino@udc.es
'''

# Importación de librerías
import sys
from sly import Lexer, Parser
import pandas as pd
 
class SQLLexer(Lexer):
    # 1. DEFINIMOS LOS TOKENS PARA LA GRAMÁTICA
 
    tokens = { 'SELECT', 'FROM', 'JOIN', 'JOINTYPE', 'WHERE', 'LOAD', 'FILENAME', 'NAME', 
              'EXIT', 'REAL', 'ENTERO','COMMA', 'OPERADOR', 'ASTERISCO', 
              'PUNTOCOMA', 'AND', 'OR', 'LPAREN', 'RPAREN', 'AS', 'ON', 
              'COMILLA_SIMPLE', 'COMILLA_DOBLE'}
   
    ignore_newline = r'\r?\n'
    ignore = ' \t'
   
    # 2. EXPRESIONES REGULARES
   
    SELECT = r'SELECT|select'
    FROM = r'FROM|from'
    JOIN = r'JOIN|join'
    WHERE = r'WHERE|where'
    EXIT = r'EXIT|exit'
    LOAD = r'LOAD|load'
    AS = r'AS|as'
    ON = r'ON|on'
    AND = r'AND|and'
    OR = r'OR|or'
    JOINTYPE = r'OUTER|INNER|LEFT|RIGHT|outer|inner|left|right'
    REAL = r'-?[0-9]+\.[0-9]+'
    ENTERO = r'-?[0-9]+'
    COMMA = r','
    PUNTOCOMA = r';'
    OPERADOR = r'>=|<=|!=|<|>|='
    LPAREN = r'\('
    RPAREN = r'\)'  
    FILENAME = r'\w+\.csv'
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

    ASTERISCO = r'\*'
    COMILLA_SIMPLE = r'\''
    COMILLA_DOBLE = r'\"'
   
    # 3. MÉTODOS
 
    def REAL(self, t):
        t.value = float(t.value)
        return t
   
    def OPERADOR(self, t): # PARA USAR QUERY
        if t.value == '=': t.value = "=="
        return t
 
    def ENTERO(self, t):
        t.value = int(t.value)
        return t
 
    def ignore_newline(self, t):
        self.lineno += 1
 
class SQLParser(Parser):
    # SIMBOLOS TERMINALES  
    tokens = SQLLexer.tokens

    # PRECEDENCIAS
    precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'LPAREN', 'RPAREN'),
    
    )
 
    # REGLAS DE PRODUCCIÓN Y ACCIONES SEMÁNTICAS
    def __init__(self):
        super().__init__()
        # Un diccionario para almacenar los DataFrames cargados
        self.dataframes = {}
        self.selected_columns = []
        self.df = None
        self.jointype = None
        self.join = False
        self.on = None
        self.where = False
        self.condition = False
        self.cond_mult = False
        self.conditions = []  # Lista para almacenar múltiples condiciones
        self.operadores = []
 
    @_('exit', 'load','select')
    def axioma(self,p):
        return p
    
    # EXIT       
    @_('EXIT')
    def exit(self, p):
        print("Programa terminado.")
        # Salir del programa
        sys.exit()

    # LOAD
    @_('LOAD FILENAME AS NAME PUNTOCOMA')
    def load(self, p):
        filename = p.FILENAME
        name = p.NAME
        # Cargar el archivo CSV en un DataFrame de Pandas y guardarlo en el diccionario
        self.dataframes[name] = pd.read_csv(filename)
        print(f'Se ha cargado correctamente el archivo {filename} con el nombre {name}')

    # SELECT
    @_('SELECT fields FROM NAME jointype join where PUNTOCOMA')
    def select(self, p):
        name = p.NAME
        fields = p.fields

        if self.df is None:
            self.df = self.dataframes[name]
       
        if fields == '*':
            self.selected_columns = list(self.df.columns)
           
        if self.join == True:
            for columna in self.df.columns:
                if columna in self.dataframes[self.tabla_join].columns and columna != self.on:
                    # Renombrar las columnas que se repiten
                    self.df.rename(columns={columna: f"{columna}_0"}, inplace=True)
                    self.dataframes[self.tabla_join].rename(columns={columna: f"{columna}_1"}, inplace=True)  
                
            if self.jointype is not None:
                self.df = pd.merge(self.dataframes[self.tabla_join], self.df, on=self.on, how=self.jointype)
            else:
                self.df = pd.merge(self.dataframes[self.tabla_join], self.df, on=self.on)
                
        if self.where == True:
            if len(self.conditions) == 1:
                self.df = self.df.query(self.conditions[0])
            else: 
                self.conditions = [elemento for elemento in self.conditions if elemento is not None]
                self.conditions = self.conditions[::-1]

                
                expresion = ""
                for condicion, operador in zip(self.conditions, self.operadores):
                    expresion += f"({condicion}) {operador} "
                expresion += self.conditions[-1] 
    
                self.df = self.df.query(expresion)


        # Mostrar las columnas seleccionadas
        print(self.df[self.selected_columns])
        # Reiniciamos as variables
        self.selected_columns = []
        self.df = None
        self.join = False
        self.jointype = None
        self.conditions = []
        self.condition = False
        self.expr = ''
        self.operadores = []
        # Devolver los campos seleccionados y el nombre de la tabla
        return self.selected_columns, name
    
    # Definimos o baleiro
    @_('')
    def empty(self, p):
        pass

    # Reglas para a cláusula WHERE
    @_('WHERE condition')
    def where(self, p):
        self.where = True
        self.condition=True
        self.conditions.append(p.condition)
        return None

    # MAS DE UNA CONDICION   
    @_('condition AND condition')
    def condition(self, p):
        # Almacenar las condiciones en la lista
        self.cond_mult = True

        self.conditions.append(p.condition0)
        self.conditions.append(p.condition1)
        
        self.operadores.append('and')
        return None
    
    @_('condition OR condition')
    def condition(self, p):
        self.cond_mult = True

        self.conditions.append(p.condition0)
        self.conditions.append(p.condition1)
        
        self.operadores.append('or')
        return None
    
    # PARENTESIS  
    @_('LPAREN condition RPAREN')
    def condition(self, p):
        return (p.condition)
    
    # POSIBILIDADES CONDICION
    @_('NAME OPERADOR REAL')
    def condition(self, p):
        # Construir una condición
        return f"{p.NAME} {p.OPERADOR} {p.REAL}"
       
    @_('NAME OPERADOR ENTERO')
    def condition(self, p):
        # Construir una condición
        return f"{p.NAME} {p.OPERADOR} {p.ENTERO}"
       
    @_('NAME OPERADOR COMILLA_SIMPLE NAME COMILLA_SIMPLE')
    def condition(self, p):
        # Construir una condición
        return f"{p.NAME0} {p.OPERADOR} '{p.NAME1}'"
   
    @_('NAME OPERADOR COMILLA_DOBLE NAME COMILLA_DOBLE')
    def condition(self, p):
        # Construir una condición
        return f"{p.NAME0} {p.OPERADOR} '{p.NAME1}'"
    
    # SI NO EXISTE
    @_('empty')  
    def where(self, p):
        pass
    
    # Reglas para o join    
    @_('empty')
    def join(self, p):
        pass
   
    @_('empty')
    def jointype(self, p):
        pass
    # TIPO DE JOIN
    @_('JOINTYPE')
    def jointype(self, p):
  
        self.jointype = p.JOINTYPE.lower()
        pass
   
    @_('JOIN NAME ON NAME')
    def join(self, p):
        self.tabla_join = p.NAME0
        self.join = True
        self.on = p.NAME1
        
    # Reglas para a seleccion de columnas
    @_('ASTERISCO')
    def fields(self, p):
        return '*'
        
    @_('columns COMMA NAME', 'NAME')
    def columns(self, p):
        self.selected_columns.append(p.NAME)
   
    @_('columns')
    def fields(self, p):
        return p
    
    # ERRORES
    def error(self, token):
        if token:
            print(f"Error sintáctico en la posicion {token.index}: Token inesperado '{token.value}'")
        else:
            print("Error sintáctico: la sentencia SQL no es correcta")
        self.restart()
 
# No debéis modificar el comportamiento de esta sección
if __name__ == '__main__':
 
    lexer = SQLLexer()
    parser = SQLParser()
 
    while True:
        try:
            text = input(' > ')
        except EOFError:
            break
        if text:

            parser.parse(lexer.tokenize(text))
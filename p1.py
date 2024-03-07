'''
    Aitana Martínez Rey: aitana.martinez@udc.es
    Uxío Merino Currás: uxio.merino@udc.es
'''

import sys

from sly import Lexer

# Se proporciona LogLexer como el analixador léxico de base que debéis completar.
# Podéis implementar lexers adicionales si decidís realizar un análisis léxico condicional.


class LogLexer(Lexer):
    '''
    Lexer base 
    '''
    # Definición de tokens necesarios

    tokens = {'DATA', 'MANANA', 'TARDE', 'NOITE', 'MACHINE_NAME', 'MENSAXE'}
    # Partes a ignorar
    ignore = r'( \t\n)'
    ignore_sshd = r'sshd\[\d+\]'
    
    # Expresiones regulares de los tokens
    DATA = r'[a-zA-Z]{3}\s+\d{1,2}'
    MANANA = r'(0[8-9]|1[0-5]):(\d{2}):(\d{2})'
    TARDE = r'(1[6-9]|2[0-3]):(\d{2}):(\d{2})'
    NOITE = r'(0[0-7]):(\d{2}):(\d{2})'
    NEWLINE = r'\n'
    MENSAXE = r'\:\s+'
    MACHINE_NAME = r'[a-zA-Z0-9_]+'

    
    
    # Inicializamos los contadores
    def __init__(self):

        # Eventos totales
        self.counter = 0

        #  Eventos por trimestre
        self.trimestre = {'T1': 0, 'T2': 0, 'T3': 0, 'T4': 0}
        self.tr = ' '
        self.accepted_T1 = 0
        self.failed_T1 = 0
        self.invalid_T1 = 0
        self.accepted_T2 = 0
        self.failed_T2 = 0
        self.invalid_T2 = 0
        self.accepted_T3 = 0
        self.failed_T3 = 0
        self.invalid_T3 = 0
        self.accepted_T4 = 0
        self.failed_T4 = 0
        self.invalid_T4 = 0

        # Eventos por horario
        self.horario = {'Mañan': 0, 'Tarde': 0, 'Noite': 0}
        self.h = ' '
        self.accepted_Mañan = 0
        self.failed_Mañan = 0
        self.invalid_Mañan = 0
        self.accepted_Tarde = 0
        self.failed_Tarde = 0
        self.invalid_Tarde = 0
        self.accepted_Noite = 0
        self.failed_Noite = 0
        self.invalid_Noite = 0

        # Máquinas
        self.machines = {}
        self.nombre_maquina = ''
        self.machine_accepted = {}
        self.machine_failed = {}
        self.machine_invalid = {}

        # Mensajes
        self.accepted = 0
        self.failed = 0
        self.invalid = 0
        self.otros = 0

        # Usuario
        self.usuarios = {}
        self.estado = ''
        self.usuario = ''
        self.usuarios_aceptados = {}
        self.usuarios_rexeitados = {}
        self.usuarios_invalidos = {}

        # IP
        self.ip = ''

        # CLASE A
        self.accepted_a_publica = 0
        self.a_pub = 0
        self.failed_a_publica = 0
        self.invalid_a_publica = 0
        self.dicc_a_publica = {'accepted': 0, 'failed': 0, 'invalid': 0}

        self.accepted_a_privada = 0
        self.a_priv = 0
        self.failed_a_privada = 0
        self.invalid_a_privada = 0
        self.dicc_a_privada =  {'accepted': 0, 'failed': 0, 'invalid': 0}

        # CLASE B
        self.accepted_b_publica = 0
        self.b_pub = 0
        self.failed_b_publica = 0
        self.invalid_b_publica = 0
        self.dicc_b_publica = {'accepted': 0, 'failed': 0, 'invalid': 0}

        self.accepted_b_privada = 0
        self.b_priv = 0
        self.failed_b_privada = 0
        self.invalid_b_privada = 0
        self.dicc_b_privada = {'accepted': 0, 'failed': 0, 'invalid': 0}

        # CLASE C
        self.accepted_c_publica = 0
        self.c_pub = 0
        self.failed_c_publica = 0
        self.invalid_c_publica = 0
        self.dicc_c_publica =  {'accepted': 0, 'failed': 0, 'invalid': 0}

        self.accepted_c_privada = 0
        self.c_priv = 0
        self.failed_c_privada = 0
        self.invalid_c_privada = 0
        self.dicc_c_privada = {'accepted': 0, 'failed': 0, 'invalid': 0}
        
        # Puertos
        self.puerto = ''
        self.reserved_ports = {'accepted': 0, 'failed': 0, 'invalid': 0}
        self.not_reserved_ports = {'accepted': 0, 'failed': 0, 'invalid': 0}
        self.reserved = 0
        self.not_reserved = 0

    def error(self, t): 
        self.index += 1     
    
    # Definicion de paso a nueva linea
    def NEWLINE(self, t):
        self.lineno += 1

    def DATA(self, t):
        # Actualizamos o contador total de eventos
            self.counter += 1
            
            month = str(t.value).split(' ')[0]
            if month in ['Jan', 'Feb', 'Mar']:
                self.trimestre['T1'] += 1
                self.tr = 'T1'
            elif month in ['Apr', 'May', 'Jun']:
                self.trimestre['T2'] += 1
                self.tr = 'T2'
            elif month in ['Jul', 'Aug', 'Sep']:
                self.trimestre['T3'] += 1
                self.tr = 'T3'
            else:
                self.trimestre['T4'] += 1
                self.tr = 'T4'
                
            return t
    # Eventos por la mañana
    def MANANA(self, t):
        self.h = 'Mañan'
        self.horario['Mañan'] += 1
        return t

    # Eventos por la tarde
    def TARDE(self, t):
        self.h = 'Tarde'
        self.horario['Tarde'] += 1
        return t
    
    # Eventos por la noche
    def NOITE(self, t):
        self.h = 'Noite'
        self.horario['Noite'] += 1
        return t
    
    # Numero de eventos por maquina
    def MACHINE_NAME(self, t):
        
        # Guarda el nombre de la máquina en la variable de instancia
        nombre_maquina = t.value.strip().lower()
        self.nombre_maquina = nombre_maquina
        # Si la maquina ya estaba guardada en la clave en el diccionario 
        # se suma al valor, sino se guarda con el estado
        if self.nombre_maquina in self.machines.keys():
            self.machines[self.nombre_maquina]['count'] += 1
        else:
            self.machines[self.nombre_maquina] = {'count': 1, 'estado': {}}
        return t    

    # Para el mensaje llamamos a un nuevo lexer
    def MENSAXE(self, t):
        self.begin(LexerRespuesta)
        return t

    # Función para la impresión de los resultados XML de contadores y diccionarios
    def print_output(self):
        '''
        Función encargada de mostrar el resultado final tras realizar el análisis léxico.
        Debéis implementarla como consideréis oportuno, mostrando por salida estándar los
        contadores indicados en el enunciado según el formato especificado.
        '''

        print("<counters>")
        print("<overall>")
        print(f"<total>{self.counter}</total>")
        print(f"<accepted>{self.accepted}</accepted>")
        print(f"<failed>{self.failed}</failed>")
        print(f"<invalid>{self.invalid}</invalid>")
        print(f"<other>{self.otros}</other>")
        print("</overall>")

        print("<grouped_by_date>")
        for trimestre, count in self.trimestre.items():
            print(f"<{trimestre}>{count}</{trimestre}>")
        print("</grouped_by_date>")

        print("<grouped_by_time>")
        for horario, count in self.horario.items():
            print(f"<{horario.lower()}>{count}</{horario.lower()}>")
        print("</grouped_by_time>")
        
        print("<grouped_by_machine>")
        for machine, valor in self.machines.items():
            print(f"<machine name=\"{machine}\">{valor['count']}</machine>")
        print("</grouped_by_machine>")

        print("<grouped_by_user>")
        for user, count in self.usuarios.items():
            print(f"<user name=\"{user}\">{count['counts']}</user>")
        print("</grouped_by_user>")
        
        print("<grouped_by_ip>")
        print(f"<ip class=\"a\" type=\"public\">{self.a_pub}</ip>")
        print(f"<ip class=\"a\" type=\"private\">{self.a_priv}</ip>")
        print(f"<ip class=\"b\" type=\"public\">{self.b_pub}</ip>")
        print(f"<ip class=\"b\" type=\"private\">{self.b_priv}</ip>")
        print(f"<ip class=\"c\" type=\"public\">{self.c_pub}</ip>")
        print(f"<ip class=\"c\" type=\"private\">{self.c_priv}</ip>")
        print("</grouped_by_ip>")
       
        print("<grouped_by_port>")
        print(f"<port type=\"reserved\">{self.reserved}</port>")
        print(f"<port type=\"not_reserved\">{self.not_reserved}</port>")
        print("</grouped_by_port>")
        print("<grouped_by_type>")
        print("<accepted>")
        print("<grouped_by_date>")
        print(f"<T1>{self.accepted_T1}</T1>")
        print(f"<T2>{self.accepted_T2}</T2>")
        print(f"<T3>{self.accepted_T3}</T3>")
        print("</grouped_by_date>")
        print("<grouped_by_time>")
        print(f"<mañan>{self.accepted_Mañan}</mañan>")
        print(f"<tarde>{self.accepted_Tarde}</tarde>")
        print(f"<noite>{self.accepted_Noite}</noite>")
        print("</grouped_by_time>")
        print("<grouped_by_machine>")
        for machine, valor in self.machine_accepted.items():
            print(f"<machine name=\"{machine}\">{valor['count']}</machine>")
        print("</grouped_by_machine>")
        print("<grouped_by_user>")

        for user, count in self.usuarios_aceptados.items():
            print(f"<user name=\"{user}\">{count}</user>")
        print("</grouped_by_user>")
        print("<grouped_by_ip>")
        print(f"<ip class=\"a\" type=\"public\">{self.dicc_a_publica['accepted']}</ip>")
        print(f"<ip class=\"a\" type=\"private\">{self.dicc_a_privada['accepted']}</ip>")
        print(f"<ip class=\"b\" type=\"public\">{self.dicc_b_publica['accepted']}</ip>")
        print(f"<ip class=\"b\" type=\"private\">{self.dicc_b_privada['accepted']}</ip>")
        print(f"<ip class=\"c\" type=\"public\">{self.dicc_c_publica['accepted']}</ip>")
        print(f"<ip class=\"c\" type=\"private\">{self.dicc_c_privada['accepted']}</ip>")
        print("</grouped_by_ip>")
        print("<grouped_by_port>")
        print(f"<port type=\"reserved\">{self.reserved_ports['accepted']}</port>")
        print(f"<port type=\"not_reserved\">{self.not_reserved_ports['accepted']}</port>")
        print("</grouped_by_port>")
        print("</accepted>")
        print("<failed>")
        print("<grouped_by_date>")
        print(f"<T1>{self.failed_T1}</T1>")
        print(f"<T2>{self.failed_T2}</T2>")
        print(f"<T3>{self.failed_T3}</T3>")
        print("</grouped_by_date>")
        print("<grouped_by_time>")
        print(f"<mañan>{self.failed_Mañan}</mañan>")
        print(f"<tarde>{self.failed_Tarde}</tarde>")
        print(f"<noite>{self.failed_Noite}</noite>")
        print("</grouped_by_time>")
        print("<grouped_by_machine>")
        for machine, valor in self.machine_failed.items():
            print(f"<machine name=\"{machine}\">{valor['count']}</machine>")
        print("</grouped_by_machine>")
        print("<grouped_by_user>")
        for user, count in self.usuarios_rexeitados.items():
            print(f"<user name=\"{user}\">{count}</user>")
        print("</grouped_by_user>")
        print("<grouped_by_ip>")
        print(f"<ip class=\"a\" type=\"public\">{self.dicc_a_publica['failed']}</ip>")
        print(f"<ip class=\"a\" type=\"private\">{self.dicc_a_privada['failed']}</ip>")
        print(f"<ip class=\"b\" type=\"public\">{self.dicc_b_publica['failed']}</ip>")
        print(f"<ip class=\"b\" type=\"private\">{self.dicc_b_privada['failed']}</ip>")
        print(f"<ip class=\"c\" type=\"public\">{self.dicc_c_publica['failed']}</ip>")
        print(f"<ip class=\"c\" type=\"private\">{self.dicc_c_privada['failed']}</ip>")
        print("</grouped_by_ip>")
        print("<grouped_by_port>")
        print(f"<port type=\"reserved\">{self.reserved_ports['failed']}</port>")
        print(f"<port type=\"not_reserved\">{self.not_reserved_ports['failed']}</port>")
        print("</grouped_by_port>")
        print("</failed>")
        print("<invalid>")
        print("<grouped_by_date>")  
        print(f"<T1>{self.invalid_T1}</T1>")
        print(f"<T2>{self.invalid_T2}</T2>")
        print(f"<T3>{self.invalid_T3}</T3>")
        print("</grouped_by_date>")
        print("<grouped_by_time>")
        print(f"<mañan>{self.invalid_Mañan}</mañan>")
        print(f"<tarde>{self.invalid_Tarde}</tarde>")
        print(f"<noite>{self.invalid_Noite}</noite>")
        print("</grouped_by_time>")
        print("<grouped_by_machine>")
        for machine, valor in self.machine_invalid.items():
            print(f"<machine name=\"{machine}\">{valor['count']}</machine>")
        print("</grouped_by_machine>")
        print("<grouped_by_user>")
        for user, count in self.usuarios_invalidos.items():
            print(f"<user name=\"{user}\">{count}</user>")
        print("</grouped_by_user>")
        print("<grouped_by_ip>")
        print(f"<ip class=\"a\" type=\"public\">{self.dicc_a_publica['invalid']}</ip>")
        print(f"<ip class=\"a\" type=\"private\">{self.dicc_a_privada['invalid']}</ip>")
        print(f"<ip class=\"b\" type=\"public\">{self.dicc_b_publica['invalid']}</ip>")
        print(f"<ip class=\"b\" type=\"private\">{self.dicc_b_privada['invalid']}</ip>")
        print(f"<ip class=\"c\" type=\"public\">{self.dicc_c_publica['invalid']}</ip>")
        print(f"<ip class=\"c\" type=\"private\">{self.dicc_c_privada['invalid']}</ip>")
        print("</grouped_by_ip>")
        print("<grouped_by_port>")
        print(f"<port type=\"reserved\">{self.reserved_ports['invalid']}</port>")
        print(f"<port type=\"not_reserved\">{self.not_reserved_ports['invalid']}</port>")
        print("</grouped_by_port>")
        print("</invalid>")
        print("</grouped_by_type>")
        print("</counters>")
        pass


# Lexer para validación del mensaje        
class LexerRespuesta(Lexer):
    # Definición de tokens
    tokens = {'ACEPTADA', 'REXEITADA', 'INVALIDA', 'OTROS'}
    ignore = r'( \t\n)'
    
    # Expresiones regulares posibles
    ACEPTADA = r'Accepted password for'
    INVALIDA = r'Invalid user|Failed password for invalid user'
    REXEITADA = r'Failed password for'  
    OTROS = r'.+'
   
   # Contador de errores
    def error(self, t): 
        self.index += 1

    # Se guarda en el diccionario de maquinas aceptadas con el numero de mensajes aceptados por maquina, por trmiestre
    # por hora y el estado
    def ACEPTADA(self, t):
        if self.nombre_maquina not in self.machine_accepted:
            self.machine_accepted[self.nombre_maquina] = {'count': 0, 'estado': {'accepted': 0}}
        # Incrementa el contador de eventos aceptados para la máquina actual
        self.machine_accepted[self.nombre_maquina]['count'] += 1
        self.machine_accepted[self.nombre_maquina]['estado']['accepted'] += 1
        
        # Incrementa el contador general de eventos aceptados
        self.accepted += 1
        # Aceptaciones por fecha
        if self.tr == 'T1':
            self.accepted_T1 += 1
        elif self.tr == 'T2':
            self.accepted_T2 += 1
        elif self.tr == 'T3':
            self.accepted_T3 += 1
        else:
            self.accepted_T4 += 1

        
        if self.h == 'Mañan':
            self.accepted_Mañan += 1
        elif self.h == 'Tarde':
            self.accepted_Tarde += 1
        else:
            self.accepted_Noite += 1
        
        # Reinicia las variables de máquina y estado
        self.nombre_maquina = ''
        self.estado = 'ACEPTADA'
        # LLama al lexer de usuario
        self.begin(UsuarioLexer)  
        return t

    # Se guarda en el diccionario de maquinas rechazadas con el numero de mensajes aceptados por maquina, por trmiestre
    # por hora y el estado
    def REXEITADA(self, t):
        if self.nombre_maquina not in self.machine_failed:
            self.machine_failed[self.nombre_maquina] = {'count': 0, 'estado': {'failed': 0}}
        # Incrementa el contador de eventos aceptados para la máquina actual
        self.machine_failed[self.nombre_maquina]['count'] += 1
        self.machine_failed[self.nombre_maquina]['estado']['failed'] += 1
        
        # Incrementa el contador general de eventos aceptados
        self.failed += 1
        
        if self.tr == 'T1':
            self.failed_T1 += 1
        elif self.tr == 'T2':
            self.failed_T2 += 1
        elif self.tr == 'T3':
            self.failed_T3 += 1
        else:
            self.failed_T4 += 1
        
        if self.h == 'Mañan':
            self.failed_Mañan += 1
        elif self.h == 'Tarde':
            self.failed_Tarde += 1
        else:
            self.failed_Noite += 1
        
        # Reinicia las variables de máquina y estado
        self.nombre_maquina = ''
        self.estado = 'REXEITADA'
        # LLama al lexer de usuario
        self.begin(UsuarioLexer)  
        return t         
    
    # Se guarda en el diccionario de maquinas invalidas con el numero de mensajes aceptados por maquina, por trmiestre
    # por hora y el estado
    def INVALIDA(self, t):        
        if self.nombre_maquina not in self.machine_invalid:
            self.machine_invalid[self.nombre_maquina] = {'count': 0, 'estado': {'invalid': 0}}
        # Incrementa el contador de eventos aceptados para la máquina actual
        self.machine_invalid[self.nombre_maquina]['count'] += 1
        self.machine_invalid[self.nombre_maquina]['estado']['invalid'] += 1
        
        # Incrementa el contador general de eventos aceptados
        self.invalid += 1
        
        if self.tr == 'T1':
            self.invalid_T1 += 1
        elif self.tr == 'T2':
            self.invalid_T2 += 1
        elif self.tr == 'T3':
            self.invalid_T3 += 1
        else:
            self.invalid_T4 += 1

        
        if self.h == 'Mañan':
            self.invalid_Mañan += 1
        elif self.h == 'Tarde':
            self.invalid_Tarde += 1
        else:
            self.invalid_Noite += 1
        
        # Reinicia las variables de máquina y estado
        self.nombre_maquina = ''
        self.estado = 'INVALIDA'
        # LLama al lexer de usuario
        self.begin(UsuarioLexer)  
        return t         
    
    # En oto caso se hace una llamada al log lexer y no se procesa el usuario
    def OTROS(self, t):
        # Se suma uno a contador de otros
        self.otros += 1
        self.begin(LogLexer)
        return t


# Clase para usuarios para su clasificacion
class UsuarioLexer(Lexer):
    # Definicion de tokens
    tokens = {'USUARIO'}
    ignore = r'( \n)'
    # Expresión regular
    USUARIO = r'[^\s]+'

    def error(self, t): 
        self.index += 1

    # Añadimos los usuarios en caso de que no estén a un diccionario específico según su estado
    def USUARIO(self, t):
        self.usuario = t.value

        if self.usuario in self.usuarios:
            if self.estado == 'ACEPTADA':
                self.usuarios_aceptados[self.usuario] += 1
            elif self.estado == 'REXEITADA':
                self.usuarios_rexeitados[self.usuario] += 1
            elif self.estado == 'INVALIDA':
                self.usuarios_invalidos[self.usuario] +=  1

            # Verifica si la clave 'counts' ya existe en el diccionario del usuario
            if 'counts' in self.usuarios[self.usuario]:
                self.usuarios[self.usuario]['counts'] += 1
            else:
                # Si no existe, inicialízala con el valor 1
                self.usuarios[self.usuario]['counts'] = 1
        else:
            # Si el usuario no existe en el diccionario, inicializa su entrada con 'counts' = 1
            if self.estado == 'ACEPTADA':
                self.usuarios_aceptados[self.usuario] = 1
            elif self.estado == 'REXEITADA':
                self.usuarios_rexeitados[self.usuario] = 1
            elif self.estado == 'INVALIDA':
                self.usuarios_invalidos[self.usuario] =  1

            self.usuarios[self.usuario] = {'counts': 1}

         
        # LLamamos al lexer para IPs
        self.begin(IPLexer)
        return t


# Clase para Ips y su clasificación por clase y tipo
class IPLexer(Lexer):
    # Definimos los tokens referentes a las IPs
    tokens = {'FROM','CLASE_A_PRIVADA', 'CLASE_A_PUBLICA', 'CLASE_B_PRIVADA', 'CLASE_B_PUBLICA', 'CLASE_C_PRIVADA', 'CLASE_C_PUBLICA'}

    # Ignoramos el salto de linea y la ausencia de ip
    ignore = r'[^\s]+'
    ignore_linea = r'\n'
   
    

    # Definimos las expresiones regulares para las clases de IP
    CLASE_A_PRIVADA = r'10(\.(1[0-9][0-9]|2[0-4][0-9]|25[0-5]|[1-9][0-9]?|\d)){3}'
    CLASE_A_PUBLICA = r'(12[0-7]|1[0-1][0-9]|[1-9][0-9]?|\d)(\.(1[0-9][0-9]|2[0-4][0-9]|25[0-5]|[1-9][0-9]?|\d)){3}'


    CLASE_B_PRIVADA = r'172(\.1[6-9]|2[0-9]|[3][0-1])(\.(1[0-9][0-9]|2[0-4][0-9]|25[0-5]|[1-9][0-9]|[0-9])){2}'
    CLASE_B_PUBLICA = r'(12[8-9]|1[3-8][0-9]|19[0-1])(\.(1[0-9][0-9]|2[0-4][0-9]|25[0-5]|[1-9][0-9]|[0-9])){3}' 

    CLASE_C_PRIVADA = r'192\.168(\.(1[0-9][0-9]|2[0-4][0-9]|25[0-5]|[1-9][0-9]|[0-9])){2}'
    CLASE_C_PUBLICA = r'(19[2-8]|2[0-1][0-9]|22[0-3])(\.(1[0-9][0-9]|2[0-4][0-9]|25[0-5]|[1-9][0-9]|[0-9])){3}' 


    def error(self, t): 
        self.index += 1
       
    
    def ignore_linea(self, t):
        self.begin(LogLexer)

    # Clase A: clasificación por estado
    def CLASE_A_PRIVADA(self, t):
        self.ip = t.value
        
        if self.estado == 'ACEPTADA':
            self.dicc_a_privada['accepted'] += 1
        elif self.estado == 'REXEITADA':
            self.dicc_a_privada['failed'] += 1
        else:
            self.dicc_a_privada['invalid'] += 1

        self.a_priv += 1
        # LLamada a puerto Lexer
        self.begin(PuertoLexer)
        return t
    
    # Clase A: clasificación por estado
    def CLASE_A_PUBLICA(self, t):
        self.ip = t.value
        
        if self.estado == 'ACEPTADA':
            self.dicc_a_publica['accepted'] += 1
        elif self.estado == 'REXEITADA':
            self.dicc_a_publica['failed'] += 1
        else:
            self.dicc_a_publica['invalid'] += 1

        self.a_pub += 1
        # LLamada a puerto Lexer
        self.begin(PuertoLexer)
        return t
    
    # Clase B: clasificación por estado
    def CLASE_B_PRIVADA(self, t):
        self.ip = t.value
        
        if self.estado == 'ACEPTADA':
            self.dicc_b_privada['accepted'] += 1
        elif self.estado == 'REXEITADA':
            self.dicc_b_privada['failed'] += 1
        else:
            self.dicc_b_privada['invalid'] += 1

        self.b_priv += 1
        # LLamada a puerto Lexer
        self.begin(PuertoLexer)
        return t
    
    # Clase B: clasificación por estado
    def CLASE_B_PUBLICA(self, t):
        self.ip = t.value
        
        if self.estado == 'ACEPTADA':
            self.dicc_b_publica['accepted'] += 1
        elif self.estado == 'REXEITADA':
            self.dicc_b_publica['failed'] += 1
        else:
            self.dicc_b_publica['invalid'] += 1

        self.b_pub += 1
        # LLamada a puerto Lexer
        self.begin(PuertoLexer)
        return t
    
    # Clase C: clasificación por estado
    def CLASE_C_PRIVADA(self, t):
        self.ip = t.value
        
        if self.estado == 'ACEPTADA':
            self.dicc_c_privada['accepted'] += 1
        elif self.estado == 'REXEITADA':
            self.dicc_c_privada['failed'] += 1
        else:
            self.dicc_c_privada['invalid'] += 1

        self.c_priv += 1
        # LLamada a puerto Lexer
        self.begin(PuertoLexer)
        return t
    
    # Clase C: clasificación por estado
    def CLASE_C_PUBLICA(self, t):
        self.ip = t.value
        
        if self.estado == 'ACEPTADA':
            self.dicc_c_publica['accepted'] += 1
        elif self.estado == 'REXEITADA':
            self.dicc_c_publica['failed'] += 1
        else:
            self.dicc_c_publica['invalid'] += 1

        self.c_pub += 1
        # LLamada a puerto Lexer
        self.begin(PuertoLexer)
        return t


# Clase que nos permite clasificar el puerto en reservado y no reservado y por su estado
class PuertoLexer(Lexer):
    # Definimos tokens para puertos reservados y no reservados
    tokens = {'RESERVED_PORT', 'NOT_RESERVED_PORT'} 
    ignore = r'\t'
    ignore_l =  r'\n'

    # Expresiones regulares
    RESERVED_PORT = r'port\s+(0|102[0-4]|10[0-1][0-9]):?(?=\D|$)'
    NOT_RESERVED_PORT = r'port\s+(102[5-9]|10[2-9][0-9]|[1-9][0-9]{2,4}|[2-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-6]):?(?=\D|$)'

    def error(self, t): 
        self.index += 1
    
    def ignore_l(self,t):
       
        self.begin(LogLexer)
    
    # Para reservados los gusrdamos en un diccionario valor es si es aceptado, rechazado o invalido
    def RESERVED_PORT(self, t):
        
        self.port = t.value
       
        if self.estado == 'ACEPTADA':
            self.reserved_ports['accepted'] += 1
        elif self.estado == 'REXEITADA':
            self.reserved_ports['failed'] += 1
        else:
            self.reserved_ports['invalid'] += 1

        # Sumamos al contador de puertos resrevados   
        self.reserved += 1
        return t
    # Para  NO reservados los guardamos en un diccionario valor es si es aceptado, rechazado o invalido
    def NOT_RESERVED_PORT(self, t):
 
        self.port = t.value
        
        if self.estado == 'ACEPTADA':
            self.not_reserved_ports['accepted'] += 1
        elif self.estado == 'REXEITADA':
            self.not_reserved_ports['failed'] += 1
        else:
            self.not_reserved_ports['invalid'] += 1
        
        # Sumamos al contador de puertos NO reservados  
        
        self.not_reserved += 1
        return t


# AQUÍ NO SE HAN REALIZADO CAMBIO
if __name__ == '__main__':

    # Inicializa el Lexer principal.
    lexer = LogLexer()

    # Lee íntegramente el fichero proporcionado por entrada estándar
    text = sys.stdin.read()

    tokens = None

    # Procesa los tokens (análisis léxico) y e invoca la función que muestra la salida
    if text:
        list(lexer.tokenize(text, lineno=0))
        lexer.print_output()
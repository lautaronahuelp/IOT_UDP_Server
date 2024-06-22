import datetime

#Traceback (most recent call last):
#  File "D:\LAUTARO\PYTHON\udp-server\server.py", line 129, in <module>
#    comandoAEnviar = commandList.enviarComando()
#  File "D:\LAUTARO\PYTHON\udp-server\ListaComandos.py", line 59, in enviarComando
#    if comandoTimeout == None and datetime.datetime.now() - comando['ultEnviado'] > 0.005:
#TypeError: unsupported operand type(s) for -: 'datetime.datetime' and 'int'

class ListaDispositivos:
    
    def __init__(self):
        #{nroserie, direccion, ultRecep, secuencia}
        self.listaDispositivos = []
        self.actualizo = False

    def actualizoLista(self):
        self.actualizo = True
    
    def estaActualizada(self):
        if self.actualizo:
            self.actualizo =  False
            return True
        else:
            return False

    def agregarDispositivo(self, dispositivo, direccion):
        existeDispositivo = False
        if len(self.listaDispositivos) > 0:
            for device in self.listaDispositivos:
                if device['nroserie'] == dispositivo:
                    existeDispositivo = True
                    device['direccion'] = direccion
                    device['ultRecep'] = datetime.datetime.now()
        if not(existeDispositivo):
            #{account, address, ultRecep, secuencia}
            self.listaDispositivos.append({'nroserie': dispositivo, 'direccion': direccion, 'ultRecep': datetime.datetime.now(), 'secuencia': 0,})
            self.ordenarLista()
        self.actualizoLista()

    def recibioTest(self, direccion):
        print("RECIBIO TEST")
        if len(self.listaDispositivos) > 0:
            for device in self.listaDispositivos:
                if device['direccion'] == direccion:
                    device['ultRecep'] = datetime.datetime.now()
                    self.actualizoLista()
                    return True
        return False

    def existeDispositivo(self, nroserie):
        for device in self.listaDispositivos:
                if device['nroserie'] == nroserie:
                    return True
        return False

    def obtenerSecuencia(self, nroserie):
        for dispositivo in self.listaDispositivos:
                if dispositivo['nroserie'] == nroserie:
                    return dispositivo['secuencia']

    def obtenerDispositivo(self, nroserie):
        pass
    
    def obtenerDireccion(self, nroserie):
        if len(self.listaDispositivos) > 0:
            for device in self.listaDispositivos:
                if device['nroserie'] == nroserie:
                    return device['direccion']
        return None

    def ordenarLista(self):
        self.listaDispositivos.sort(key = lambda d : d['nroserie'])

    def imprimeLista(self):
        if self.estaActualizada():
            print("LISTA DISPOSITIVOS:")
            for i in self.listaDispositivos:
                print(i)
import datetime
ENVIOS_MAX = 5#CONVERTIR ESTAS CONST A VARIABLES DEL CONSTRUCTOR
ENVIOS_TIMEOUT = 500#ms

class ListaComandos:
    

    def __init__(self):
        #{nroserie, accion, valor, secuencia, ultEnviado, conteo}
        self.listaComandos = []
        self.enProceso = []#{nroserie}
        self.comandoEnPreparacion = None #indice del comando en preparacion
        self.actualizo = False

    def actualizoLista(self):
        self.actualizo = True
    
    def estaActualizada(self):
        if self.actualizo:
            self.actualizo =  False
            return True
        else:
            return False

    def agregarComando(self, comando):#RECIBIR COMANDO
        comando['secuencia'] = None
        self.listaComandos.append(comando)
        self.actualizoLista()

    def aumentaConteo(self, nroserie, secuencia):
        for comando in self.listaComandos:
            if comando['nroserie'] == nroserie and comando['secuencia'] == secuencia:
                comando['conteo'] += 1
                comando['ultEnviado'] = datetime.datetime.now()
                self.actualizoLista()

    def preparaComando(self):
        #busca un comando para preparar, devuelve True o False
        #   1- comando para un dispositivo que no tiene otro comando pendiente, osea no estaEnProceso
        bandera = False

        for index, comando in enumerate(self.listaComandos):
            if not(self.estaEnProceso(comando['nroserie'])):
                bandera = True
                self.comandoEnPreparacion = index
                break
        
        return bandera
    
    def hayComandoEnPreparacion(self):
        if self.comandoEnPreparacion != None:
            return True
        else:
            return False

    def devuelveNroSerie(self):
        #devuelve nro de serie del comando en preparacion
        if self.hayComandoEnPreparacion():
            return self.listaComandos[self.comandoEnPreparacion]['nroserie']


    def asignarDispositivo(self, secuencia):
        #asigna secuencia y direccion al comando en preparacion
        #asigna nroserie a enProceso
        if self.comandoEnPreparacion != None:
            self.listaComandos[self.comandoEnPreparacion]['secuencia'] = secuencia
            self.enProceso.append(self.listaComandos[self.comandoEnPreparacion]['nroserie'])
            self.comandoEnPreparacion = None
            self.actualizoLista()
    
    def eliminaComandoEnPreparacion(self):
        if self.comandoEnPreparacion != None:
            self.listaComandos.pop(self.comandoEnPreparacion)
            print("COMANDO POPEADO")
            self.actualizoLista()

    def enviarComando(self):
        #busca un comando para enviar
        #   1- comando listo a enviarse (se establecio secuencia y direccion)
        #   2- si no hay comando listo, comando aun sin ack que paso el timeout 500ms
        #devuelve comando #ver si devuelve None
        comandoConteoCero = None
        comandoTimeout = None
        for comando in self.listaComandos:
            if comando['secuencia'] != None:#tema elegir comandos para enviar
                if comandoConteoCero == None and comando['conteo'] == 0:
                    if comando != comandoTimeout:
                        comandoConteoCero = comando
            
                restaTimeout = datetime.datetime.now() - comando['ultEnviado']
            
                if comandoTimeout == None and comando['conteo'] < ENVIOS_MAX and (restaTimeout.total_seconds() * 1000) > ENVIOS_TIMEOUT:
                    if comando != comandoConteoCero:
                        comandoTimeout = comando

                if comandoTimeout != None and comandoConteoCero != None:
                    break
        
        if comandoConteoCero != None:
            print('conteo cero')
            self.aumentaConteo(comandoConteoCero['nroserie'], comandoConteoCero['secuencia'])
            self.actualizoLista()
            return comandoConteoCero
        else:
            #print('timeout')
            if comandoTimeout != None:
                self.aumentaConteo(comandoTimeout['nroserie'], comandoTimeout['secuencia'])
                self.actualizoLista()
            return comandoTimeout
    
    def estaEnProceso(self, nroSerie):
        if self.enProceso.count(nroSerie) == 0:
            return False
        else:
            return True
    
    def limpiaLista(self):
        listaAEliminar = []
        for index, comando in enumerate(self.listaComandos):
            restaTimeout = datetime.datetime.now() - comando['ultEnviado']
            if comando['conteo'] == ENVIOS_MAX and (restaTimeout.total_seconds() * 1000) > ENVIOS_TIMEOUT:#VER TEMA ELIMINA EL QUE SE ENVIO POR ULTIMA VEZ <=IMPORTANTE!!!
                listaAEliminar.append(index)
        
        listaAEliminar.sort(reverse=True)

        for index in listaAEliminar:
            nroserieAEliminar = self.listaComandos[index]['nroserie']
            self.enProceso.remove(nroserieAEliminar)
            self.listaComandos.pop(index)
            
        
        if len(listaAEliminar) > 0:
            self.actualizoLista()
        
        
    def ackRecibido(self, ack):#RECIBE SECUENCIA Y CUENTA
        print(">ingreso ACK")
        indexEliminar = -1
        for index, comando in enumerate(self.listaComandos):
            if comando['nroserie'] == ack['nroserie'] and comando['secuencia'] == int(ack['secuencia']):
                indexEliminar = index
        
        if indexEliminar != -1:
            self.listaComandos.pop(indexEliminar)
            self.enProceso.remove(ack['nroserie'])
        else:
            pass#si el ack es de un indice que ya no tiene comando, debe aumentar la secuencia en la ListaEquipos y avisar al frontend
        
        self.actualizoLista()

    def imprimeLista(self):
        if self.estaActualizada():
            print("LISTA COMANDOS:")
            for i in self.listaComandos:
                print(i)

    
import socket
import datetime
from ListaComandos import ListaComandos
from ListaDispositivos import ListaDispositivos


listaDispositivos = ListaDispositivos()

listaComandos = ListaComandos()

#PROTOCOLO: <LF>CHECLLLL,CCCCCC,SSSS,KKKK,V,DATETIMESTAMP<CR>
#\n17660018,aa1232,0023,kbyc,/11234\r
#V -> LARGO VARIABLE
#EN iden V ES LA SECUENCIA DE COMANDOS DEL DISPOSITIVO
#
#
#
#
#MENSAJES DE PRUEBA:
#IDEN PRUEBA: <LF>ea4c0011,aa5678,0001,iden<CR>
#KBYC PRUEBA: <LF>7d040018,aa5678,0001,kbyc,/11234<CR>
#AKC KBYC PRUEBA: <LF>fb360010,aa5678,0000,ack<CR>(<LF>fc060018,aa5678,0000,kbyc,/11234<CR>)
#


def _crc_stamp(msg: str | None) -> str | None:
        """Calculate the CRC of the msg. SIN LF Y CR"""
        if msg is None:  # pragma: no cover
            return None
        crc = 0
        for letter in str.encode(msg):
            temp = letter
            for _ in range(0, 8):
                temp ^= crc & 1
                crc >>= 1
                if (temp & 1) != 0:
                    crc ^= 0xA001
                temp >>= 1
        return ("%x" % crc).lower().zfill(4)+("%x" % len(msg)).lower().zfill(4)

#comandoUno = ",aa1232,0023,kbyc,/11234"

#print(_crc_stamp(comandoUno) + comandoUno)


def _veri_protocolo(message):#MEJORAR METODO DE COMPROBACION DEL STRING, MAS ESTRICTO
    band = True
    messageStriped = message.strip("\n\r")
    #PROTOCOLO: <LF>CHECLLLL,CCCCCC,SSSS,KKKK,V<CR>
    #\n17660018,aa1232,0023,kbyc,/11234\r
    #V -> LARGO VARIABLE
    for ch in messageStriped:
        orden = ord(ch)
        if not((orden > 32 and orden < 57) or (orden > 96 and orden < 123)):
            band = False
    if band:
        if _crc_stamp(messageStriped[8:]) == messageStriped[:8]:
            return True
    return False

def _proc_protocolo(message, address):
    messageStriped = message.strip("\n\r")
    listTokens = messageStriped.rsplit(",")
    if listTokens[3] == "iden":
        listaDispositivos.agregarDispositivo(listTokens[1], address)
        return True
    if listTokens[3] == "kbyc":
        listaComandos.agregarComando({'nroserie': listTokens[1], 'accion': "kbyc", 'valor': listTokens[4], 'conteo': 0, 'ultEnviado': datetime.datetime(1, 1, 1, 0, 0, 0, 0), }) ##se le asigna secuencia cuando lo va empieza a enviar
        return True
    if listTokens[3] == "ack":
        #for index, comando in commandList:
        #    if comando['nroserie'] == listTokens[1] and comando['secuencia'] == listTokens[2]:
        #        commandList.pop(index)
        #        break
        listaComandos.ackRecibido({'nroserie': listTokens[1], 'secuencia': listTokens[2],})
    return False

   
               
     

localIP     = "192.168.100.4"
localPort   = 54000
bufferSize  = 1024

 

msgFromServer       = "Hello UDP Client"

bytesToSend         = str.encode(msgFromServer)

# Create a datagram socket

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

 

# Bind to address and ip

UDPServerSocket.bind((localIP, localPort))

 

print("UDP server up and listening")

UDPServerSocket.setblocking(False)

# Listen for incoming datagrams

while(True):
    
    hayData = True
    
    try:
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    except:
        
        hayData = False

    if hayData:
        message = bytesAddressPair[0]

        address = bytesAddressPair[1]

        messageDecoded = message.decode("utf-8")

        if messageDecoded == "@":
            if not(listaDispositivos.recibioTest(address)):
                #\n17660018,aaaaaa,aaaa,iden\r
                print("@NO EXISTE ENVIA IDEN")
                response = ",aaaaaa,aaaa,iden"
                UDPServerSocket.sendto(str.encode(("\n%s%s\r") % (_crc_stamp(response), response)), address)
    
        if _veri_protocolo(messageDecoded):
            if _proc_protocolo(messageDecoded, address):
                #"xccccllll,aaaaaa,aaaa,ackx"
                response = (",%s,%s,ack" % (messageDecoded[10:16], messageDecoded[17:21]))
                UDPServerSocket.sendto(str.encode(("\n%s%s\r") % (_crc_stamp(response), response)), address)
    
    if listaComandos.preparaComando():
        nroserie = listaComandos.devuelveNroSerie()
        if listaDispositivos.existeDispositivo(nroserie):
            secuencia = listaDispositivos.obtenerSecuencia(nroserie)
            listaComandos.asignarDispositivo(secuencia)
        else:
            print("NO EXISTE DISPOSITIVO %s" % nroserie)
            listaComandos.eliminaComandoEnPreparacion()
    
    #convertir objeto y mandarlo
    comandoAEnviar = listaComandos.enviarComando()
    if comandoAEnviar != None:
        #PROTOCOLO: <LF>CHECLLLL,CCCCCC,SSSS,KKKK,V<CR>
        secuenciaString = ("%s" % comandoAEnviar['secuencia']).zfill(4)
        comando = (",%s,%s,%s,%s" % (comandoAEnviar['nroserie'], secuenciaString,
                                      comandoAEnviar['accion'], comandoAEnviar['valor']))
        direccion = listaDispositivos.obtenerDireccion(comandoAEnviar['nroserie'])
        if direccion != None:
            UDPServerSocket.sendto(str.encode(("\n%s%s\r") % (_crc_stamp(comando), comando)), direccion)

    listaDispositivos.imprimeLista()
    listaComandos.imprimeLista()

    listaComandos.limpiaLista()
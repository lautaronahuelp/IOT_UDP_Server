#PROTOCOLO: <LF>checllll,kkk,ssss,aaaaaaaaaaaa,rr,v,datetimestamp<CR>
#\n17660018,aa1232,0023,kbyc,/11234\r
#V -> LARGO VARIABLE
#EN iden V ES LA SECUENCIA DE COMANDOS DEL DISPOSITIVO
#
#DDMMAAAAHHMMSSUNN
#   ->DD: DIA EN 2 DIGITOS
#   ->MM: MES EN 2 DIGITOS
#   ->AAAA: AÑO EN 4 DIGITOS
#   ->HH: HORA EN DOS DIGITOS
#   ->MM: MINUTO EN DOS DIGITOS
#   ->SS: SEGUNDO EN DOS DIGITOS
#   ->U: HUSO => + O -
#   ->NN: DIFERENCIA HORARIA EN  DIGITOS
#
#TOKENS: idn, ack, nak, kbc, cid, tst, sta, prg
#
#
#MENSAJES DE PRUEBA:
#solicita identificacion: <LF>ccccllll,idn,,,,,02072024204156-03<CR>
#◙ccccllll,idn,,,,,02072024204156-03♪
#◙d9360019,idn,,,,,02072024204156-03♪
#envia identificacion: <LF>checllll,idn,0001,aaaaaaaa5678,23,v,datetimestamp<CR>      
#comando teclado: <LF>checllll,kbc,0001,aaaaaaaa5678,21,/11234,datetimestamp<CR>
#ack: <LF>checllll,ack,0001,aaaaaaaa5678,20,,datetimestamp<CR>
#nak: <LF>checllll,nak,0001,aaaaaaaa5678,20,,datetimestamp<CR>
#
#IDEN PRUEBA: <LF>ea4c0011,aa5678,0001,iden<CR>(new: <LF>ccccllll,idn,0001,aa5678,datetimestamp<CR>)
#KBYC PRUEBA: <LF>7d040018,aa5678,0001,kbyc,/11234<CR>
#AKC KBYC PRUEBA: <LF>fb360010,aa5678,0000,ack<CR>(<LF>fc060018,aa5678,0000,kbyc,/11234<CR>)
#NAK PRUEBA:  <LF>,aa5678,0000,nak<CR> (SE RECIBIO COMANDO PERO NO SE PUEDE ENVIAR AL DISPOSITIVO)
#
#TEMA SECUENCIA!
#
#TEMA ESTADO (sta) -> REPORTA CAMBIO DE ESTADO
#   RESPECTO ARMADOS: (pdralsi)d: desarmado/r: armado presente/ a:armado ausente/ l:armado parcial/ s: armando tiempo de salida/ i: armado sin tiempo de salida
#       -> pdras (part1: desarmada, part2: armada presente, part3:armada ausente, part4:en tiempo de salida)
#   RESPECTO ZONAS: (nebc)n: anulada/e: en alarma/b: abierta/c: cerrada
#       -> ! -> ninguna zona cumple la condicion (n! ninguna anulada)
#       -> ZZ -> zona que cumple la condicion en dos digitos (b010432 -> z1 z3 y z32 abiertas)
#   RESPECTO FALLAS: fallas presentes
#   RESPECTO MEMORIA: ?????
#   RESPECTO TECLADO REMOTO: debe reportar lo que indica el teclado (iconos: PRO, MEM, BYP, CHI, FUE)
#

class ProtocoloIOT:
    tokens = ["idn", "ack", "nak", "kbc", "cid", "tst", "sta", "prg"]

    def __init__(self, stringInicial = None):
        #ingresa stringInicial = "<LF>CHECLLLL,KKKK,SSSS,CCCCCC,V,DATETIMESTAMP<CR>"
        self._stringOriginal = ""
        self._stringLimpio = None

        if stringInicial != None:
            self._stringOriginal = stringInicial
    
        self._crcStamp = ""
        self._token = ""
        self._secuencia = 0
        self._nroserie = ""
        self._senial = 0
        self._valor = ""
        self._timestamp = ""
        self._valido = False
    
    def __str__(self):
        return ("\n%s,%s\r" % (self._crcStamp, self._token, ("%d" % self._secuencia).zfill(4), self._nroserie, self._senial, self._valor, self._timestamp))

    def esValido(self, stringProtocolo = None):#MEJORAR METODO DE COMPROBACION DEL STRING, MAS ESTRICTO
        #<LF>checllll,kkk,ssss,aaaaaaaaaaaa,rr,v,datetimestamp<CR>
        band = True
        position = [ -1, -1 ]
        stripeado = ""

        if stringProtocolo == None:
            stringProtocolo = self._stringOriginal
        
        position[0] = stringProtocolo.find("◙")
        position[1] = stringProtocolo.find("♪")
        print("STRING>%s<" % stringProtocolo)
        print("POSICIONES %d,%d" % (position[0],position[1]))
        if position[0] != -1 and position[1] != -1 and position[0] < position[1]:
            stripeado = stringProtocolo[(position[0] + 1):position[1]]
            
            if (stripeado.count(",") == 6):
                for ch in stripeado:
                    orden = ord(ch)
                    if not((orden > 32 and orden < 57) or (orden > 96 and orden < 123)):
                        band = False

                if band:
                    self._stringLimpio = stripeado
                    if not(self.genCRCStamp() == stripeado[:8]) or not(self.tokens.count(stripeado[9:12]) == 1):
                        band = False 
                
            else:
                band = False
        else:
                band = False
        
        self._valido = band

        return self._valido
    
    def genCRCStamp(self) -> str | None:
        """Calculate the CRC of the msg. SIN LF Y CR"""
        if self._stringLimpio is None:  # pragma: no cover
            return None
        crc = 0
        for letter in str.encode(self._stringLimpio[8:]):
            temp = letter
            for _ in range(0, 8):
                temp ^= crc & 1
                crc >>= 1
                if (temp & 1) != 0:
                    crc ^= 0xA001
                temp >>= 1
        self._crcStamp = ("%x" % crc).lower().zfill(4)+("%x" % len(self._stringLimpio[8:])).lower().zfill(4)
        return self._crcStamp

    def procesarString(self):
        #<LF>checllll,kkk,ssss,aaaaaaaaaaaa,rr,v,datetimestamp<CR>
        if(self._valido):
            stringDescontruido = self._stringLimpio.rsplit(",")
    def setCuenta(self, nroserie):
        pass

    def setSecuencia(self, secuencia):
        pass

    def setComando(self, comando, valor = None):
        pass
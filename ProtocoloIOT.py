#PROTOCOLO: <LF>CHECLLLL,KKKK,SSSS,CCCCCC,V,DATETIMESTAMP<CR>
#\n17660018,aa1232,0023,kbyc,/11234\r
#V -> LARGO VARIABLE
#EN iden V ES LA SECUENCIA DE COMANDOS DEL DISPOSITIVO
#
#TOKENS: idn, ack, nak, kbc, cid, tst,
#
#
#MENSAJES DE PRUEBA:
#solicita idn: <LF>ccccllll,idn,datetimestamp<CR>
#IDEN PRUEBA: <LF>ea4c0011,aa5678,0001,iden<CR>(new: <LF>ccccllll,idn,0001,aa5678,datetimestamp<CR>)
#KBYC PRUEBA: <LF>7d040018,aa5678,0001,kbyc,/11234<CR>
#AKC KBYC PRUEBA: <LF>fb360010,aa5678,0000,ack<CR>(<LF>fc060018,aa5678,0000,kbyc,/11234<CR>)
#NAK PRUEBA:  <LF>,aa5678,0000,nak<CR> (SE RECIBIO COMANDO PERO NO SE PUEDE ENVIAR AL DISPOSITIVO)

class ProtocoloIOT:

    def __init__(self, stringInicial = None):
        #ingresa stringInicial = "<LF>CHECLLLL,KKKK,SSSS,CCCCCC,V,DATETIMESTAMP<CR>"
        self._stringCompleto = ""
        if stringInicial != None:
            self._stringCompleto = stringInicial
        else:
            self._crcStamp = ""
            self._token = ""
            self._secuencia = 0
            self._nroserie = ""
            self._valor = ""
            self._timestamp = ""
            self._valido = False
    
    def __str__(self):
        return ("\n%s,%s\r" % (self._crcStamp, self._token,))

    def esValido(self, stringProtocolo = None):#MEJORAR METODO DE COMPROBACION DEL STRING, MAS ESTRICTO
        band = True
        if stringProtocolo == None:
            stringProtocolo = self._stringCompleto
        position = [ -1, -1 ]
        position[0] = stringProtocolo.find('\n')
        position[1] = stringProtocolo.find('\r')
        if position[0] != -1 and position[1] != -1 and position[0] < position[1]:
            stripeado = stringProtocolo[(position[0] + 1):position[1]]
            for ch in stripeado:
                orden = ord(ch)
                if not((orden > 32 and orden < 57) or (orden > 96 and orden < 123)):
                    band = False
            if band:
                if self.genCRCStamp(stripeado[8:]) == stripeado[:8]:
                    if stringProtocolo == None:
                        self._valido = True
                    return True
        if stringProtocolo == None:
            self._valido = False
        return False

    def setCuenta(self, nroserie):
        pass

    def setSecuencia(self, secuencia):
        pass

    def setComando(self, comando, valor = None):
        pass

    def genCRCStamp(self) -> str | None:
        """Calculate the CRC of the msg. SIN LF Y CR"""
        if self.stringSinCRC is None:  # pragma: no cover
            return None
        crc = 0
        for letter in str.encode(self.stringSinCRC):
            temp = letter
            for _ in range(0, 8):
                temp ^= crc & 1
                crc >>= 1
                if (temp & 1) != 0:
                    crc ^= 0xA001
                temp >>= 1
        return ("%x" % crc).lower().zfill(4)+("%x" % len(self.stringSinCRC)).lower().zfill(4)
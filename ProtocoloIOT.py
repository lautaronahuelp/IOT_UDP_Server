#PROTOCOLO: <LF>CHECLLLL,CCCCCC,SSSS,KKKK,V,DATETIMESTAMP<CR>
#\n17660018,aa1232,0023,kbyc,/11234\r
#V -> LARGO VARIABLE
#EN iden V ES LA SECUENCIA DE COMANDOS DEL DISPOSITIVO
#
#TOKENS: idn, ack, nak, kbc, cid, tst,
#
#
#MENSAJES DE PRUEBA:
#IDEN PRUEBA: <LF>ea4c0011,aa5678,0001,iden<CR>
#KBYC PRUEBA: <LF>7d040018,aa5678,0001,kbyc,/11234<CR>
#AKC KBYC PRUEBA: <LF>fb360010,aa5678,0000,ack<CR>(<LF>fc060018,aa5678,0000,kbyc,/11234<CR>)
#NAK PRUEBA:  <LF>,aa5678,0000,nak<CR> (SE RECIBIO COMANDO PERO NO SE PUEDE ENVIAR AL DISPOSITIVO)

class ProcotoIOT:

    def __init__(self, stringInicial = None):
        #ingresa stringInicial = "<LF>CHECLLLL,CCCCCC,SSSS,KKKK,V,DATETIMESTAMP<CR>"
        if stringInicial != None:
            self.stringCompleto = stringInicial
        else:
            self.crcStamp = ""
            self.nroserie = ""
            self.secuencia = 0
            self.token = ""
            self.valor = ""
            self.timestamp = ""

    def esValido():
        pass

    def _veri_protocolo(self, stringProtocolo = None):#MEJORAR METODO DE COMPROBACION DEL STRING, MAS ESTRICTO
        band = True
        if stringProtocolo != None:
            messageStriped = stringProtocolo.strip("\n\r")
            #PROTOCOLO: <LF>CHECLLLL,CCCCCC,SSSS,KKKK,V<CR>
            #\n17660018,aa1232,0023,kbyc,/11234\r
            #V -> LARGO VARIABLE
            for ch in messageStriped:
                orden = ord(ch)
                if not((orden > 32 and orden < 57) or (orden > 96 and orden < 123)):
                    band = False
            if band:
                if self.genCRCStamp(messageStriped[8:]) == messageStriped[:8]:
                    return True
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
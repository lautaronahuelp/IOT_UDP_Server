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

class ProcotoIOT:

    def __init__(self, stringInicial = None):
        if stringInicial != None:
            self.stringInicial = stringInicial

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
        self.crcStamp = ("%x" % crc).lower().zfill(4)+("%x" % len(self.stringSinCRC)).lower().zfill(4)
        return self.crcStamp
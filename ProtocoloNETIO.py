#<ide=70710494|00=58388E5C|01=123456|03=74|04=FFFF|!34EF>
class ProtocoloNetio:
    _tokens = ["ide", "00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16"]
    _tokensSinValor = ["07", "08"]

    def __init__(self, stringInicial = None):
        #ingresa stringInicial = "<LF>CHECLLLL,KKKK,SSSS,CCCCCC,V,DATETIMESTAMP<CR>"
        self._stringOriginal = ""
        self._stringLimpio = None

        if stringInicial != None:
            self._stringOriginal = stringInicial
        
        else:
            self._crcStamp = ""
            self._token = ""
            self._secuencia = 0
            self._nroserie = ""
            self._senial = 0
            self._valor = ""
            self._timestamp = ""
            self._schecker = ""
            self._achecker = ""
            self._hbCuenta = ""
            self._cid = ""
            self._progString = ""
            self._panelString = ""
            self._ioread = ""
            self._owrite = ""
            self._panelStatus = ""
            self._csrSecuencia= 0
            self._valido = False
            self._esAck = False
            self._esNack = False
            
    
    def __str__(self):
        return ("\n%s,%s\r" % (self._crcStamp, self._token, ("%d" % self._secuencia).zfill(4), self._nroserie, self._senial, self._valor, self._timestamp))

    def esValidoCRC(self):
        #<ide=70710494|00=58388E5C|01=123456|03=74|04=FFFF|!34EF>
        band = False

        if self._stringOriginal != None:
            protocoloLength = len(self._stringOriginal)
            if protocoloLength >= 18 and self._stringOriginal.startswith("ide") and self._stringOriginal[-5] == "!":
                stringSpliteado = self._stringOriginal.split("!")
                stringParaCRC = stringSpliteado[0] + "!"
                bytesString = str.encode(stringParaCRC)
        
                if ("%x" % ProtocoloNetio.crc_ccitt_16(bytesString)).upper().zfill(4) == stringSpliteado[1]:
                    band = True
                    self._stringLimpio = self._stringOriginal

        self._valido = band
        
        return self._valido
    
    def crc_ccitt_16(data):
        crc = 0xFFFF  
        for byte in data:
            crc ^= (byte << 8) 
            for _ in range(8):
                if crc & 0x8000:  
                    crc = (crc << 1) ^ 0x1021  
                else:
                    crc <<= 1  

                crc &= 0xFFFF 

        return crc

    def procesarString(self):
        #<LF>checllll,kkk,ssss,aaaaaaaaaaaa,rr,v,datetimestamp<CR>
        diccionarioProtocolo = {}
        if(self.esValidoCRC()):
            stringDescontruido = self._stringLimpio.rsplit("|")
            for sp in stringDescontruido:
                if sp.find("=") != -1:
                    campoDes = sp.split("=")
                    if(self._tokens.count(campoDes[0]) == 1):
                        diccionarioProtocolo[campoDes[0]] = campoDes[1]
                        if(campoDes[0] == "ide"):
                            self._nroserie = campoDes[1]
                        elif(campoDes[0] == "00"):
                            self._timestamp = campoDes[1]
                        elif(campoDes[0] == "01"):
                            self._schecker = campoDes[1]
                        elif(campoDes[0] == "02"):
                            self._achecker = campoDes[1]
                        elif(campoDes[0] == "03"):
                            self._senial = int(campoDes[1])
                        elif(campoDes[0] == "04"):
                            self._hbCuenta = campoDes[1]
                        elif(campoDes[0] == "05"):
                            self._cid = int(campoDes[1])
                        elif(campoDes[0] == "07"):
                            sec = "0x" + campoDes[1]
                            self._secuencia = int(sec)
                        elif(campoDes[0] == "09"):
                            self._progString = campoDes[1]
                        elif(campoDes[0] == "10"):
                            self._panelString = campoDes[1]
                        elif(campoDes[0] == "11"):
                            self._ioread = campoDes[1]
                        elif(campoDes[0] == "12"):
                            self._owrite = campoDes[1]
                        ##FALTAN PROBAR 13 Y 14
                        elif(campoDes[0] == "15"):
                            self._panelStatus = campoDes[1]
                        elif(campoDes[0] == "16"):
                            self._csrSecuencia= int(campoDes[1])
                elif(sp == self._tokensSinValor[0]):#07
                    diccionarioProtocolo[sp] = True
                    self._esAck = True
                elif(sp == self._tokensSinValor[1]):#08
                    diccionarioProtocolo[sp] = True
                    self._esNack = True
                else:
                    self._crcStamp = sp.strip("!")


            return True
        
        return False

    def setCuenta(self, nroserie):
        pass

    def setSecuencia(self, secuencia):
        pass

    def setComando(self, comando, valor = None):
        pass
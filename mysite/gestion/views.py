from django.shortcuts import render, get_object_or_404
from .models import Comando

#tema udp
import socket
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

# Create your views here.
def lista_comandos(request):
    comandos = Comando.objects.all()
    return render(request, 'gestion/lista_comandos.html', { 'comandos': comandos, })

def envia_comando(request, pk):
    comando = get_object_or_404(Comando, pk=pk)
    address = ("192.168.100.4", 54000)
    localIP     = "192.168.100.4"
    localPort   = 50000
    bufferSize  = 1024
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind((localIP, localPort))
    response = ",aa5678,0000,kbyc,%s" % comando.comando
    UDPServerSocket.sendto(str.encode(("\n%s%s\r") % (_crc_stamp(response), response)), address)
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    messageDecoded = bytesAddressPair[0].decode("utf-8")
    if messageDecoded == "ok":
        enviado =  "ENVIADO!"
    elif messageDecoded == "tuki":
        enviado = "ACK ERRONEO"
    else:
        enviado = "ack indefinido"
    UDPServerSocket.close()
    return render(request, 'gestion/envia_comandos.html', { 'enviado': enviado })
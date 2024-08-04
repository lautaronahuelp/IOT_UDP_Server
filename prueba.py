#import datetime
# position = [ -1, -1 ]
# proto = "abs\nCHECLLLL,CCCCCC,SSSS,KKKK,V\rd"
# position[0] = proto.find('\n')
# position[1] = proto.find('\r')
# if position[0] != -1 and position[1] != -1 and position[0] < position[1]:
#     stripeado = proto[(position[0] + 1):position[1]]
# print("PROTO:")
# print(proto)
# print("STRIPEADO:")
# print(stripeado)

# """fruits = []

# fruits.append({'id': 0, 'nombre': "cherry"})
# fruits.append({'id': 1, 'nombre': "banana"})
# fruits.append({'id': 2, 'nombre': "apple"})

# #fruits.sort()

# for fruit in fruits:
#     print(fruit['id'])
#     print(fruit['nombre'])"""

# def orden(dict):
#     return dict['id']

# fruits = []

# fruits.sort()

# fruits.append({'id': 1, 'nombre': "cherry"})
# fruits.append({'id': 2, 'nombre': "banana"})
# fruits.append({'id': 3, 'nombre': "apple"})

# #fruits.sort()
# print("---")
# for fruit in fruits:
#     print(fruit)

# fruits.sort(key=orden)

# print("---")
# for fruit in fruits:
#     print(fruit)

# fruits.append({'id': 1, 'nombre': "anana"})

# print("---")
# for fruit in fruits:
#     print(fruit)
# #datetime.datetime(1, 1, 1, 0, 0, 0, 0)
# objeto = {}

# date = datetime.datetime.now()
# date2 = datetime.datetime(2024, 6, 17, 17, 20, 0, 0)

# date3 = date - date2

# print(date3)
# millis = date3.total_seconds() * 1000
# print(millis)

#objeto['date'] = date

#print(objeto)
#print(objeto['date'])

# import socket

# localIP     = "192.168.100.4"
# localPort   = 54000
# bufferSize  = 1024

 

# msgFromServer       = "Hello UDP Client"

# bytesToSend         = str.encode(msgFromServer)

# # Create a datagram socket

# UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

 

# # Bind to address and ip

# try:
#     UDPServerSocket.bind((localIP, localPort))
# except:
#     print("segundo puerto")
#     UDPServerSocket.bind((localIP, 54001))

 

# print("UDP server up and listening")

# UDPServerSocket.close()
#◙ccccllll,idn,,,,,02072024204156-03♪
#◙2632001a,idn,,,,,02072024204156-03♪
#import sys
#from ProtocoloIOT import ProtocoloIOT

#stringRecibido = input("Ingrese string: ")

#eventoRecibido = ProtocoloIOT(stringRecibido)

#print(eventoRecibido.esValido())

#print(eventoRecibido.genCRCStamp())

#print(eventoRecibido.esValido())

#print(eventoRecibido)

from ProtocoloNETIO import ProtocoloNetio

stringRecibido = input("Ingrese string: ")

recibido = ProtocoloNetio(stringRecibido)

print(recibido.procesarString())
print(recibido._crcStamp)


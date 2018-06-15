import socket               # Import socket module
from threading import Thread
import time
import json



def getStatus(jsonCliente):
	json_dat = json.loads(jsonCliente);

	print "Cliente: "+json_dat['_Cliente__nombre']
	print "Cuentas:"
	print "id Saldo"
	total=0
	for cuenta in json_dat['_Cliente__cuentas']:
		print str(cuenta['_Cuenta__id'])+"  "+(cuenta['_Cuenta__saldo'])
		total=total+float(cuenta['_Cuenta__saldo'])

	print "Saldo Total: "+str(total)


def bandeja():
	global status
	global s
	while 1:
		men=s.recv(1024)
		try:
			getStatus(men)
		except:
			print str("\n")+men

		if "Adios" in men:
			status=True
			break
def caja():
	global s
	global status
	while 1:
		msg=raw_input("\033[1;32;40m-")
		s.sendall(str(msg))
		if status:
			break


s = socket.socket()         # Create a socket object
host='localhost'
#host = '172.31.103.224' 			# Get local machine name
port = 33012                # Reserve a port for your service.
status=False
s.connect((host, port))


listaHilos=[]
listaHilos.append(Thread(target=bandeja, args=()).start())
listaHilos.append(Thread(target=caja, args=()).start())
menAnt=""
while 1:
	
	if status:
		
		break

s.close                     # Close the socket when donee

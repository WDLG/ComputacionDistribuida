import socket               # Import socket module
from threading import Thread
import time

#print "Ingresa el mensaje "
#msg=input()


def bandeja():
	global status
	global s
	while 1:
		men=s.recv(1024)
		print str("\n")+men
		if "Adios" in men:
			status=True
			break
def caja():
	global s
	global status
	while 1:
		msg=raw_input("-")
		s.sendall(str(msg))
		if status:
			break


s = socket.socket()         # Create a socket object
host = 'localhost' 			# Get local machine name
port = 33012                # Reserve a port for your service.
status=False
s.connect((host, port))

#Thread(target=bandeja, args=()).start()
#Thread(target=caja, args=()).start()
listaHilos=[]
listaHilos.append(Thread(target=bandeja, args=()).start())
listaHilos.append(Thread(target=caja, args=()).start())
menAnt=""
while 1:
	"""
	Thread(target=bandeja, args=()).start()
	Thread(target=caja, args=()).start()
    """
	if status:
		"""
		for h in listaHilos:
			h.join()
		"""
		break

	"""
	men=s.recv(1024)
	print men
	if men==None or men in "Por favor ingresa tu nickname":
		msg=raw_input("<you>: ")
		s.sendall(str(msg))
    """
	#time.sleep(3)
	#msg=raw_input("<you>: ")
	#s.sendall(str(msg))
	"""
	if men=="Adios":
		break
	"""

	"""
	if str(s.recv(1024))=='Adios':
		break
	"""
s.close                     # Close the socket when donee
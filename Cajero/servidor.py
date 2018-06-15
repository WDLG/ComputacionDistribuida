import socket
import sys
import traceback
import time
import re
from models import *
from threading import Thread
import json


#HOST = '172.31.106.17'   # Symbolic name, meaning all available 
HOST = 'localhost'
#interfaces
PORT = 33012 # Arbitrary non-privileged port

listaClientes=[]
patron_chp=re.compile('CHAT@[a-zA-Z]+')
patron_chg=re.compile('CHATG@')


print("\033[1;31;40m INICIO\n")


class Cliente_session():
    def __init__(self,ip,port,nickname,conn):
        self.ip=ip 
        self.port=port
        self.nickname=nickname
        self.conn=conn
    

def buscarCliente(nombre):
    try:
        id=Clientes(nombre).getId()
        if id:
            print "Cliente Encontrado"
            return True
        else:
            print "Cliente no encontrado:"
            return False
    except:
            print "Cliente no encontrado:"
            return False


def getStatus(nombre):
    cliente=Clientes(nombre)
    cc=CC(cliente.getId())
    cliente=Cliente(cc,nombre,cc.getCuentas())
    return str(json.dumps(cliente, default=jsonDefault))

def jsonDefault(object):
    return object.__dict__



def inicializar_servidor():
    global listaClientes
    print "---------------------------------------------------------------------"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Socket created"
    print "---------------------------------------------------------------------"

    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print "Bind failed. Error Code: " + str(sys.exc_info())
        sys.exit()

    s.listen(5)       # limite de concurrencia para 5 clientes
    print "El socket esta escuchando..."

    # Bucle que atiende a los clientes
    while True:
        connection, address = s.accept()
        ip, port = str(address[0]), str(address[1])
        #print "Conectado con: " + ip + ":" + port

        try:
            Thread(target=establecer_session_cliente, args=(connection, ip, port)).start()
        except:
            print "Error al crear el hilo."
            traceback.print_exc()
    s.close()


def establecer_session_cliente(conn, ip, port):
    activo = True
    has_nickname=False
    cliente=None
    modo_consulta=False
    mod=None
    menu="Escriba:\n Saldo, para consultar el estado de las cuentas \n BYE, para salir"
    while activo:
        #Recibir mensaje del cliente
        if has_nickname==False:
            conn.sendall("Por favor ingresa tu nickname")
            msg_entrada = conn.recv(1024)
            if buscarCliente(msg_entrada):
                has_nickname=True

            if "BYE" in msg_entrada:
                activo=salir_session(conn)
            elif has_nickname:
                cliente=Cliente_session(ip,port,msg_entrada,conn)
                print cliente.nickname+" se ha conectado con: "+cliente.ip+":"+cliente.port
                listaClientes.append(cliente)
                conn.sendall("***********Sesion establecida en el sistema ***************\n"+menu+"\n")
                has_nickname=True
        else: 
            msg_entrada = conn.recv(1024)
            print "El nombre del cliente es: "+cliente.nickname
            reply=""

            if 'saldo' in msg_entrada.lower():
                try:
                    conn.sendall(getStatus(cliente.nickname))
                except:
                    conn.sendall('Hubo problemas al realizar la consulta')
            else:
                conn.sendall("*****************************************************\n"+menu+"\n")

            
            if 'BYE' in msg_entrada:
                conn.sendall('Adios')
                activo=False
            
            


            

    print "SESSION CERRADA :( "


inicializar_servidor()


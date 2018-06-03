import socket
import sys
import traceback
import time
from threading import Thread



HOST = 'localhost'   # Symbolic name, meaning all available interfaces
PORT = 33012 # Arbitrary non-privileged port

listaClientes=[]



class Mensaje():
    def __init__(self,cliente_origen,cliente_destino,mensaje):
        self.cliente_origen=cliente_origen
        self.cliente_destino=cliente_destino
        self.raw_mensaje=mensaje
        self.hora_envio=time.strftime("%H:%M:%S") 
        self.fecha_envio=time.strftime("%d/%m/%Y")
        

    def establecer_formato(self):
        return self.cliente_origen+": "+self.raw_mensaje+"--"+str(self.fecha_envio)+": "+str(self.hora_envio)

class Cliente():
    def __init__(self,ip,port,nickname,conn):
        self.ip=ip 
        self.port=port
        self.nickname=nickname
        self.conn=conn
    


def interprete_comandos(comando):
    arr=comando.split("@")
    """
    if len(arr)!=2 and not "CHAT" in arr[0] and not "" in arr[1]:
        print "No existe el comando 0"
        return "No existe el comando"
    elif not "" in arr[1]:
        return "CPri",arr[1],arr[0]
    """
    if "CHATG@" in comando:
        return "CGlo",None,None

def borrarCliente(nombre):
    global listaClientes
    cliente_del=buscarCliente(nombre)
    listaClientes.remove(cliente_del)
    print "Se ha eliminado el cliente: "+nombre

def buscarCliente(nickname):
    ip=None
    port=None
    obj=None
    for clente in listaClientes:
        print clente.nickname

    for cliente in listaClientes:
        if cliente.nickname==nickname:
            ip=cliente.ip
            port=cliente.port
            obj=cliente
            break
    return obj


def enviarMensajeGlobal(cliente_origen,msg):
    global listaClientes
    for clienteOBJ in listaClientes:
        if clienteOBJ.nickname!=cliente_origen.nickname:
            reply=Mensaje(cliente_origen.nickname,clienteOBJ,msg).establecer_formato()
            clienteOBJ.conn.sendall(reply)

def enviarMensaje(cliente,cliente_destino,msg):
        reply=Mensaje(cliente.nickname,cliente_destino,msg).establecer_formato()
        cliente=buscarCliente(cliente_destino)
        cliente.conn.sendall(reply)

def salir_session(conn):
    print "Client is requesting to quit"
    reply="Adios"
    conn.sendall('Adios')
    print "Conexion  closed"
    return False


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
        print "Conectado con: " + ip + ":" + port

        try:
            Thread(target=establecer_session_cliente, args=(connection, ip, port)).start()
        except:
            print "Error al crear el hilo."
            traceback.print_exc()
    s.close()


def establecer_session_cliente(conn, ip, port):
    activo = True
    activo_privado=False
    has_nickname=False
    cliente=None
    clienteOBJ=None
    modo_chat_privado=False
    modo_chat_publico=False
    mod=None

    while activo:
        #Recibir mensaje del cliente
        if has_nickname==False:
            conn.sendall("Por favor ingresa tu nickname")
            msg_entrada = conn.recv(1024)
            if "BYE" in msg_entrada:
                activo=salir_session(conn)
            else:
                cliente=Cliente(ip,port,msg_entrada,conn)
                listaClientes.append(cliente)
                conn.sendall("****Sesion establecida*****")
                has_nickname=True
        else: 
            msg_entrada = conn.recv(1024)
            if modo_chat_privado==False and modo_chat_publico==False:
                mod=interprete_comandos(msg_entrada)
                reply=""

            if "CPri" in mod[0] and modo_chat_privado==False and modo_chat_publico==False:
                modo_chat_privado=True
                reply="\nModo chat privado con: "+mod[1]
                conn.sendall(reply)
                msg_entrada=""
                clienteOBJ=mod[1]

            if "CGlo" in mod[0] and modo_chat_privado==False and modo_chat_publico==False:
                modo_chat_publico=True
                reply="\nModo chat publico !!!!"
                conn.sendall(reply)
                msg_entrada=""
                #clienteOBJ=mod[1]
                
            if modo_chat_publico:
                enviarMensajeGlobal(cliente,msg_entrada)

            if modo_chat_privado:
                enviarMensaje(cliente,clienteOBJ,msg_entrada)

            if "#S" in msg_entrada and modo_chat_privado==True:
                modo_chat_privado=False
                conn.sendall("\nSalio chat privado\n")

            if "#S" in msg_entrada and modo_chat_publico==True:
                modo_chat_publico=False
                conn.sendall("\nSalio chat publico\n")

            if "BYE" in msg_entrada and modo_chat_privado==False and modo_chat_publico==False:
                activo=salir_session(conn)
                borrarCliente(cliente)


            if modo_chat_privado==False and modo_chat_publico==False:
                print "Cliente0: " +str(msg_entrada)
                reply="SERVIDOR..OK\n"
                conn.sendall(reply)

            

    print "SESSION CERRADA :( "


inicializar_servidor()

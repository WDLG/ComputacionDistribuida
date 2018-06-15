from settings import Conexion
import json


class Clientes():
	def __init__(self,nombre):
		self.__nombre=nombre

	def getId(self):
		conexion=Conexion()
		return conexion.executar("select idCliente from Cliente where Nombre='"+str(self.__nombre)+"';")[0][0]


class Cliente():
	def __init__(self,id,nombre,cuentas):
		self.__id=id
		self.__nombre=nombre
		self.__cuentas=cuentas

	
	

class Cuenta():
	def __init__(self,lista):
		self.__id=lista[0]
		self.__saldo=str(lista[1])

	def getSaldo(self):
		return self.__saldo

	def __str__(self):
		return str(self.__saldo)


class CC():
	def __init__(self,id_cliente):
		self.__id_cliente=id_cliente
		self.__id_cuentas=self._getId()

	def _getId(self):
		conexion=Conexion()
		datos=conexion.executar('select idCuenta from CC where idCliente='+str(self.__id_cliente))
		return [ dato[0] for dato in datos ]
		
		

	def getCuentas(self):
		conexion=Conexion()
		listaCuentas=[]
		for id in self.__id_cuentas:
			listaCuentas.append(Cuenta(conexion.executar('select * from Cuenta where idCuenta='+str(id))[0]))
		return listaCuentas



#Servidor
def getStatus(nombre):
	cliente=Clientes(nombre)
	cc=CC(cliente.getId())
	cliente=Cliente(cc,nombre,cc.getCuentas())
	return str(json.dumps(cliente, default=jsonDefault))

def jsonDefault(object):
    return object.__dict__


#Cliente
"""
def getStatus(jsonCliente)
	json_dat = json.loads(jsonCliente);

	print "Cliente: "+json_dat['_Cliente__nombre']
	print "Cuentas:"
	print "id Saldo"
	total=0
	for cuenta in json_dat['_Cliente__cuentas']:
		print str(cuenta['_Cuenta__id'])+"  "+(cuenta['_Cuenta__saldo'])
		total=total+float(cuenta['_Cuenta__saldo'])

	print "Saldo Total: "+str(total)
"""










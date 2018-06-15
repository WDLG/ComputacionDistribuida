#!/usr/bin/python

import MySQLdb


class Conexion():
	def __init__(self):
		self.__db_conn=MySQLdb.connect('localhost','andres','123','cajero')
		self.__cursor=self.__db_conn.cursor()

	def executar(self,query):
		self.__cursor.execute(query)
		return self.__cursor.fetchall()

	def close(self):
		self.__db_conn.close()

"""
conexion = Conexion('localhost','andres','123','sgoa3')

print (conexion.execute('select * from usuarios_profesor'))
"""
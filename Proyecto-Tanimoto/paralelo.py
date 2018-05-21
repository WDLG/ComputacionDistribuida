import argparse
import numpy as np
import math
import threading
import time



class myThread(threading.Thread):
   def __init__(self,listaArchivos,tuplas=None,tid):
      threading.Thread.__init__(self)
      self.listaArchivos=listaArchivos
      self.listaParcial = []
      self.tuplas=tuplas
      self.tid=tid

   def set_proceso(self):
        if self.tuplas!=None:
            for tupla in self.tuplas:
               self.listaParcial=self.listaParcial+calcularCompuesto(self.listaArchivos[tupla[0]],self.listaArchivos[tupla[1]])

   def run(self):
      self.listaParcial=self.listaParcial+calcularSingular(self.listaArchivos[self.tid])
      self.set_proceso()
      print "Termino el hilo "+str(self.tid)+". Total de distancias calculadas: "+str(len(self.listaParcial))




def cargarDatos(nombre):
        raw_data=open(str(nombre),"r")
        datos=np.loadtxt(raw_data,dtype='str',delimiter=",")
        Valores=datos[:,1]
        Etiquetas=datos[0:,0]
        return Valores,Etiquetas
        
def calcularCompuesto(archivoA,archivoB):
        #Cargando datos
        DatosA=cargarDatos(archivoA)
        DatosB=cargarDatos(archivoB)
        listAux=[]
        bothAB=0
        onlyA=0
        onlyB=0
        for i in range(0,len(DatosA[0])):
                for j in range(0,len(DatosB[0])):     
                        orig="{0:8b}".format(int(DatosB[0][j],16))
                        sublista="{0:8b}".format(int(DatosA[0][i],16))
                        for k in range(0,n):
                            if orig[k]=='1' and orig[k]==sublista[k]:
                                    bothAB=bothAB+1
                            elif orig[k]=='1':
                                    onlyA=onlyA+1
                            elif sublista[k]=='1':
                                    onlyB=onlyB+1

                        val=1-bothAB/(onlyA+onlyB+bothAB+0.000)
                        cad=str(DatosA[1][i])+","+str(DatosB[1][j])+","+str(val)
                        listAux.append(cad+"\n")
        #Valor que el hilo retorna
        #out.put(listAux)
        return listAux
        
def calcularSingular(archivo):
        #Cargar informacion
        Datos=cargarDatos(archivo)
        #Asignar informacion  
        Valores=Datos[0]
        Etiquetas=Datos[1]
        #Inicializar variables
        listAux=[]
        bothAB=0
        onlyA=0
        onlyB=0
        for i in range(0,len(Valores)):
                
                for j in range(i,len(Valores)):     
                        
                        if i!=j:
                        	orig="{0:8b}".format(int(Valores[j],16))
                        	sublista="{0:8b}".format(int(Valores[i],16))
                        	for k in range(0,n):
                        		if orig[k]=='1' and orig[k]==sublista[k]:
                        		 		bothAB=bothAB+1
                        		elif orig[k]=='1':
                        				onlyA=onlyA+1
                        		elif sublista[k]=='1':
                        				onlyB=onlyB+1

                                val=1-bothAB/(onlyA+onlyB+bothAB+0.000)
                                cad=str(Etiquetas[i])+","+str(Etiquetas[j])+","+str(val)
                                listAux.append(cad+"\n")
        #Valor que el hilo retorna
        #out.put(listAux)
        return listAux

def multiCalculador(archivo,listaArchivos,tid):
    listaT=[]
    listaT=listaT+ calcularSingular(archivo)
    for i in range(tid,len(listaArchivos)):
            if i!=tid:
                listaT=listaT+calcularCompuesto(archivo,listaArchivos[i])
    return listaT

def guardar(listaCad):
        archivo = open(str(output), "a")
        
        for i in range(0,len(listaCad)):
            archivo.write(listaCad[i])  
                                  
        archivo.close()


#SECCION PRINCIPAL DEL PROGRAMA


ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", type=str,default="", help="ubicacion de la ruta de los archivos de entrada")
ap.add_argument('-i','--input',type=str, required=True,action='append',nargs = '*',help='help: ruta al archivo de entrada')
ap.add_argument("-b", "--bitnumber", required=True,type=int,help="longitud en bits de cada valor")
ap.add_argument("-o", "--output", type=str, default="out.csv",help="ruta al archivo de salida")
args = vars(ap.parse_args())

Etiquetas=None
Valores=None
n=args["bitnumber"]
listaArchivos=[args["path"]+file for file in args["input"][0]]
output=args["output"]



tinicial=time.time()




listaTotal=[]
listaHilos=[]

tuplas_t1=[[0,1],[1,3]]
tuplas_t2=[[0,2],[2,3]]
tuplas_t3=[[0,3]]
tuplas_t4=[[1,2]]
lista_general=[tuplas_t1,tuplas_t2,tuplas_t3,tuplas_t4]

print "Total de hilos que se crearan: "+str(len(listaArchivos))+"..\n"
#CREAR HILOS


print "Comenzando a calcular las distancias....\n"
for i in range(0,len(listaArchivos)):
    listaHilos.append(myThread(listaArchivos,lista_general[i], i))



#COMENZAR HILO
for hilo in listaHilos:
    hilo.start()

for hilo in listaHilos:
    hilo.join()

#JUNTAR RESULTADOS (MERGE)
for hilo in listaHilos:
    listaTotal=listaTotal+hilo.listaParcial



print "Se han terminado de calcular las distancias.\nGuardando resultados parciales....\n"
guardar(listaTotal)
print"-----------------------------------------------------------"
print "Total de calculos realizados: "+str(len(listaTotal))

print"-----------------------------------------------------------"
print "DISTANCIAS TANIMOTO GUARDADAS Y CALCULADAS CON EXITO!!!"

tfinal=time.time()
print "Tiempo total de procesamiento (segundos): "+str(tfinal-tinicial)

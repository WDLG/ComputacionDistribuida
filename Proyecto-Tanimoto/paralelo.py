import argparse
import numpy as np
import math
import threading
import time



class myThread(threading.Thread):
   def __init__(self,listaArchivos,tid,tuplas):
      threading.Thread.__init__(self)
      self.listaArchivos=listaArchivos
      self.listaParcial = []
      self.tuplas=tuplas
      self.tid=tid

   def set_proceso(self):
        try:
                for tupla in self.tuplas:

                    self.listaParcial=self.listaParcial+calcularCompuesto(self.listaArchivos[int(tupla[0])],self.listaArchivos[int(tupla[1])])

        except:
                    self.listaParcial=self.listaParcial
   def run(self):
      self.listaParcial=self.listaParcial+calcularSingular(self.listaArchivos[self.tid])
      self.set_proceso()
      print "Termino el hilo "+str(self.tid)+". Total de distancias calculadas: "+str(len(self.listaParcial))




def convertirHex_Bin(cadena):
        return "{0:8b}".format(int(cadena,16))
        

def EcuacionTanimoto(valores):
        return valores[0]/(valores[1]+valores[2]+valores[0]+0.000)


def get_tanimoto_values(cadenaA,cadenaB):
        global n
        
        bothAB=0
        onlyA=0
        onlyB=0
        
        cadenaA=convertirHex_Bin(cadenaA)
        cadenaB=convertirHex_Bin(cadenaB)
        for i in range(0,n):
                if cadenaA[i]=='1' and cadenaA[i]==cadenaB[i]:
                        bothAB=bothAB+1
                elif cadenaA[i]=='1':
                        onlyA=onlyA+1
                elif cadenaB[i]=='1':
                        onlyB=onlyB+1 
        return bothAB,onlyA,onlyB      
     
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
                        val=1-EcuacionTanimoto(get_tanimoto_values(DatosB[0][j],DatosA[0][i]))
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
                           val=1-EcuacionTanimoto(get_tanimoto_values(Valores[j],Valores[i]))
                           cad=str(Etiquetas[i])+","+str(Etiquetas[j])+","+str(val)
                           listAux.append(cad+"\n")
        #Valor que el hilo retorna
        #out.put(listAux)
        return listAux


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

tuplas_t1=[[0,1]]
tuplas_t2=None
lista_general=[tuplas_t1,tuplas_t2]

print "Total de hilos que se crearan: "+str(len(listaArchivos))+"..\n"
#CREAR HILOS


print "Comenzando a calcular las distancias....\n"
for i in range(0,len(listaArchivos)):
    listaHilos.append(myThread(listaArchivos,i,lista_general[i]))



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

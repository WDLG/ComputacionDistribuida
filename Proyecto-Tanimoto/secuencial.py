import numpy as np
import argparse
import time


ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", type=str,default="", help="ubicacion de la ruta del archivo de entrada")
ap.add_argument("-i", "--input", required=True,type=str, help="nombre del archivos")
ap.add_argument("-b", "--bitnumber", required=True,type=int,help="longitud en bits de cada valor")
ap.add_argument("-o", "--output", type=str, default="out.csv",help="ruta al archivo de salida")
args = vars(ap.parse_args())

Etiquetas=None
Valores=None
n=args["bitnumber"]
master_file=args["path"]+args["input"]
output=args["output"]


def cargarDatos(nombre):
        global Etiquetas
        global Valores
        raw_data=open(str(nombre),"r")
        #cargar los datos como una matriz numpy
        datos=np.loadtxt(raw_data,dtype='str',delimiter=",")
        #separar datos
        Valores=datos[:,1]
        Etiquetas=datos[0:,0]
        print len(Valores)
        print len(Etiquetas)

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

        
def calcular():
        global Valores
        lis=[]
        
        for i in range(0,len(Valores)):
                
                
                if i==len(Valores):
                        break
                
                for j in range(i,len(Valores)):     
                        if j==len(Valores):
                                break
                        if i!=j: 
                                val=1-EcuacionTanimoto(get_tanimoto_values(Valores[j],Valores[i]))
                                cad=str(Etiquetas[i])+","+str(Etiquetas[j])+","+str(val)
                                lis.append(cad+"\n")
                                #guardarArchivo(cad)
        return lis



def guardar(listaCad):
        archivo = open(str(output), "a")
        for i in range(0,len(listaCad)):
            archivo.write(listaCad[i])                        
            
        archivo.close()
               
        



tinicial=time.time()
print "Cargando Datos......\n"
cargarDatos(master_file)
print"Calculando distancias........"
resultado=calcular()
print"Se han calculado las distancias"
print"Guardando distancias.."
guardar(resultado)
print"-------------------------------------------"
print"Total de calculos realizados: "+str(len(resultado))
print"-------------------------------------------"
print "DISTANCIAS TANIMOTO GUARDADAS Y CALCULADAS CON EXITO!!!"
tfinal=time.time()
print "TIEMPO TOTAL DE EJECUCION: "+str(tfinal-tinicial)

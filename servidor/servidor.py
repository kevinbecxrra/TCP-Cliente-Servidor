import socket
import os
import time
import traceback
from threading import Thread
from datetime import datetime

UDP_IP = '0.0.0.0' #Parámetro para fijar dirección genérica en la configuración del socket.
UDP_PORT = 8000 #Puerto TCP de escucha (recepción de peticiones) en el servidor.

log_info = []

#Clase que establece hilos de conexión con los clientes que envíen petición de enlace.
class ClientThread(Thread): 

    def __init__(self,id,ip,port,sock,filename): 
        Thread.__init__(self) 
        self.id = id
        self.ip = ip 
        self.port = port 
        self.sock = sock
        self.filename = filename
        print (f"Nueva conexión desde {(ip,port)}. Cliente {id} listo para recibir.") #Confirmación de conexión con cada cliente.

    #Función run realiza el envío del mensaje solicitado de manera persistente utilizando el socket y el hilo abierto previamente.
    def run(self): 
        try:
            filesize = os.path.getsize(filename)
            self.sock.sendto(f'FILE###{filename}###SIZE###{filesize}'.encode(), (self.ip, self.port))
            time.sleep(1)
            # Algoritmo de lectura y envío.
            print(f"Enviando arvhivo a cliente {(self.ip, self.port)}")
            with open(filename, "rb") as f:
                start_time = time.time()
                while True:  
                    bytes_read = f.read(BUFFER_SIZE)
                    if not bytes_read:
                        break  
                    self.sock.sendto(bytes_read, (self.ip, self.port)) 
                finish_time = time.time()

            time.sleep(1)
            self.sock.sendto(''.encode(), (self.ip, self.port))     

            # Recoleccion de info para el log
            conn_info = dict()
            conn_info["Client ID"] = self.id
            conn_info["Client IP"] = self.ip
            conn_info["Client PORT"] = self.port            
            conn_info["Transfer time"] = "%s miliseconds" % ((finish_time - start_time)*1000)

            log_info.append(conn_info)
        except:
            traceback.print_exc()
            self.sock.close()


#Inicio del programa

#Selección de archivo
print("Los archivos disponibles son:\n1. 100 MB\n2. 250 MB\n")
seleccion_arch = int(input("Ingrese el número del archivo que desea enviar: "))
filename = "servidor/files/"
if(seleccion_arch == 1): filename += "100MB.txt"
elif (seleccion_arch == 2): filename += "250MB.txt"

#Selección tamaño de los fragmentos
bs = int(input("Ingrese el tamaño en bytes de los fragmentos que se van a enviar (max 64 KB): "))
BUFFER_SIZE = bs if bs > 4096 else 4096

#Selección num de clientes
num_clientes = int(input("Ingrese el número de clientes a conectar: "))

#Creación del socket
udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
udpsock.bind((UDP_IP, UDP_PORT)) 
threads = [] 

print ("Servidor escuchando en el puerto", UDP_PORT) 

id = 0
while len(threads) < num_clientes and len(threads) <= 25:
    try:
        data, (ip, port) = udpsock.recvfrom(512)
        newthread = ClientThread(id,ip,port, udpsock, filename) 
        threads.append(newthread) 
        id += 1
    except:
        udpsock.close()
        print("Socket cerrado")
        break

for t in threads:
    t.start()
    t.join()


#Creación del log
fecha = datetime.now()
filesize = os.path.getsize(filename)
log_name = f"{fecha.year}-{fecha.month}-{fecha.day}-{fecha.hour}-{fecha.minute}-{fecha.second}-log.txt"

file_log = open(f"servidor/Logs/{log_name}", "x")

file_log.write(f"LOG {fecha}\n\n")
file_log.write(f"Archivo enviado: {filename.split('/')[2]}\n")
file_log.write(f"Tamaño archivo: {filesize} bytes\n")
file_log.write(f"Número de conexiones: {len(log_info)}\n\n")
file_log.write(f"Información de conexiones: \n")

for data in log_info:
    elements = list(data.items())
    elements.sort()
    for (key,val) in elements:
        file_log.write(f"\t{key}: {val}\n")
    file_log.write(f"\n")

file_log.close()

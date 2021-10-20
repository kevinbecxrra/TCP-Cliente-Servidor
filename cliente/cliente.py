import socket
import traceback
import time
from threading import Thread
from datetime import datetime

UDP_IP = '0.0.0.0' #Parámetro para fijar dirección genérica en la configuración del socket. Es IP genérica pues no depende de otro servidor para responder.
UDP_PORT = 3000 #Puerto TCP de escucha (recepción de peticiones) en el servidor.
BUFFER_SIZE = 4096 #tamaño del buffer de empaquetamiento en máquina.
SERVER_IP = input("Ingrese la dirección IP del servidor: ")
SERVER_PORT = 8000
SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)
BLOCK_SIZE = 4096
DOWNLOADS_PATH = "cliente/ArchivosRecibidos/"

log_info = []
file_dict = dict()


class ServerThread(Thread):
    def __init__(self,id,sock):
        Thread.__init__(self)
        self.id = id
        self.sock = sock
        self.port = UDP_PORT+self.id

    def run(self):        
        try:
            conn_info = dict()
            self.sock.bind((UDP_IP, self.port))
            self.sock.sendto("HELLO".encode(), SERVER_ADDRESS)
            print(f"Conexión establecida con el servidor {SERVER_ADDRESS}. Cliente {self.id} listo para recibir")
        
            data, address = self.sock.recvfrom(BUFFER_SIZE)
            if len(data) > 0:
                info = data.decode().split("###")
                archivo = info[1].split("/")[2]
                tamano = int(info[3])

                file_dict["name"] = archivo
                file_dict["size"] = tamano
                
                # Descarga del archivo
                file = open(f"{DOWNLOADS_PATH}Cliente{self.id}-Prueba-{num_clientes}_{archivo}", 'wb')
                print(f"Cliente {self.id} descargando archivo {(archivo,tamano)}")
                recibidos = 0
                start_time = time.time()
                while True:
                    descarga, address = self.sock.recvfrom(BUFFER_SIZE)
                    if len(descarga) < 1: break
                    file.write(descarga)
                    recibidos += len(descarga)
                finish_time = time.time()
                file.close()
                print(f"Fin descarga Cliente {self.id}")

                # Recoleccion de info para el log
                
                conn_info["Client ID"] = self.id
                conn_info["Client IP"] = UDP_IP
                conn_info["Client PORT"] = self.port
                conn_info["Transfer time"] = "%s miliseconds" % ((finish_time - start_time)*1000)

                
                log_info.append(conn_info)
            else:
                raise Exception("No se recibió la primera información desde el servidor")
        
        except:
            traceback.print_exc()
        
        finally:
            self.sock.close()



#Inicio del programa
num_clientes = int(input("Ingrese el número de conexiones que desea realizar con el servidor: "))

threads = []
for i in range(num_clientes):
    mysock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    connection = ServerThread(i,mysock)
    connection.start()
    threads.append(connection)

for t in threads:
    t.join()
    
#Creación del log
fecha = datetime.now()
log_name = f"{fecha.year}-{fecha.month}-{fecha.day}-{fecha.hour}-{fecha.minute}-{fecha.second}-log.txt"

file_log = open(f"cliente/Logs/{log_name}", "w")

file_log.write(f"LOG {fecha}\n\n")
file_log.write(f"SERVER IP: {SERVER_IP}\n")
file_log.write(f"SERVER PORT: {SERVER_PORT}\n")
file_log.write(f"Archivo recibido: {file_dict['name']}\n")
file_log.write(f"Tamaño archivo: {file_dict['size']} bytes\n")
file_log.write(f"Número de conexiones: {len(log_info)}\n\n")
file_log.write(f"Información de conexiones: \n")

for data in log_info:
    elements = list(data.items())
    elements.sort()
    for (key,val) in elements:
        file_log.write(f"\t{key}: {val}\n")
    file_log.write(f"\n")

file_log.close()

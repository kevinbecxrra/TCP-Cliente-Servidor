# TCP-Cliente-Servidor

Aquí se encuentra el código de las aplicaciones Cliente y Servidor del Laboratorio 3.

Integrantes grupo 3:
* María Camila Terán
* Kevin Camilo Becerra
* Andrés Felipe Delgado
* Nicolás Ortega

En la rama `main` se encuentra la implementación TCP. En la rama `UDP-implementation` se encuentra la implementación con UDP.

Para correr las aplicaciones es necesario primero dirigirse a la carpeta `/servidor/files` y ejecutar el script de generación de archivos:

```bash
python generate_files.py
```

Luego, se debe correr el servidor y posteriormente el cliente desde el directorio raíz con los siguientes comandos:

Servidor:
```
python servidor/servidor.py
```

Cliente:
```
python cliente/cliente.py
```

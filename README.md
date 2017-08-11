# ElectriCERT
Implementación de un sistema para emitir certificados en blockchain para la Escuela de Ingeniería Eléctrica de la Universidad de Costa Rica. Basado en el código abierto Blockcerts. 

# Instalación
Antes de empezar se deben tener los siguientes programas instalados:
* Python 2.7
* Python 3.5 o superior
* Python Virtual Enviroment
* BitcoinCore
  - Puede guiarse utilizando los siguientes links: BitcoinCore para [cualquier OS](https://github.com/bitcoin/bitcoin/tree/master/doc) o especifícamente para [OSX](https://github.com/bitcoin/bitcoin/blob/master/doc/build-osx.md)
  - BitcoinCore utiliza un archivo de configuración usualmente llamado [bitcoin.conf](https://es.bitcoin.it/wiki/Ejecuci%C3%B3n_de_Bitcoin#Archivo_de_configuraci.C3.B3n_Bitcoin.conf). En este repositorio se encuentra un archivo de configuración que puede tomar como ejemplo.

# Cert-tools
La aplicación Cert-tools se utiliza para crear los certificados en formato JSON, a partir de una tabla que contiene las identidades de los certificados que se vayan a crear. Los certificados son llamados __unsigned certificates__ y se pasan como entradas al Cert-issuer.     

Para utilizar la herramineta, primero se instalan todos los requirimientos de Python.   
`> cd cert-tools`    
`> pip install .`     
Luego se debe configurar la aplicacion. El archivo de configuración se llama confx.ini.
Algunos parámetros importantes a cambiar son:
* certificate_description: la descripción del certificado. 
* certificate_title: el título del certificado. 
* roster: el archivo roster.csv es el archivo que debe contener los nombres de los recipientes de los certificados a emitir. 
* issuer_public_key: la llave pública obtenida de BitcoinCore. 
* issuer_id: es un archivo .json que contiene los datos del emisor.

Cert-tools se puede correr de dos maneras:
* Utilizando los scripts de Python: `> create-certificate-template -c confx.ini` y `>instantiate-certificate-batch -c confx.ini`
* Corriendo el script `>./script-tools.sh`. Este script copia automáticamente los certificados a la carpeta dentro de cert-issuer. 

# Cert-issuer

Cert-issuer se utiliza para emitir los certificados en el Blockchain. Para utilizar Cert-issuer, es necesario que BitcoinCore esté corriendo. También se necesita tener una llave pública con su respectiva llave privada. La llave privada debe escribirse un archivo llamado __pk_issuing.txt__ dentro de la carpeta __data__. El script dentro de Cert-issuer utiliza Python 3, por lo tanto se debe utilizar esta version así como instalar todas las librerias para esta. O bien, utilizar un [ambiente virtual](https://stackoverflow.com/questions/23842713/using-python-3-in-virtualenv) con Python 3.

Al igual que con Cert-tools, primero se instalan todos los requirimientos de Python.   
`> cd cert-tools`    
`> pip install .`

Luego se debe configurar la aplicación mediante el archivo confx.ini.
Algunos parámetros importantes a cambiar son:
* issuing_address = la llave pública obtenida de Bitcoin Core.
* usb_name = el directorio donde se almacena el archivo pk_issuing.
* key_file = pk_issuing.txt, archivo que contiene la llave privada.

Cert-issuer se puede correr de dos maneras:
* Utilizando el script de Python: `> python3 issue_certificates.py -c confx.ini`
* Corriendo el script `>./script-issuer.sh`. Este script activa el virtual enviroment y copia automáticamente los certificados a la carpeta dentro de cert-viewer. 

# Cert-viewer

Cert-viewer se utiliza para ver y verificar los certificados emitidos con el Cert-issuer. Esta herramienta corre en la red local y se puede ver en cualquier explorador de internet. Los certificados a visualizar deben estar en la carpeta __cert_data__. Cert-viewer utiliza Python 2.7.

Esta herramienta cuenta también con un archivo de configuracioón confx2.ini. 
En este, es necesario agregar los nombres de los certificados recientemente emitidos. 

Cert-issuer se puede correr de dos maneras:
* Utilizando el script de Python: `> python run.py -c confx2.ini`
* Corriendo el script `>./script-viewer.sh`. Este script a su vez llama a otro script de python que actualiza los nombres de los certificados en el confx2.ini. 


# BitcoinCore
Una vez se tiene instalado y corriendo BitcoinCore, se debe obtener una dirección de recepcion (llave pública) y su respectiva llave privada.
* La llave pública se puede obtener desde la ventana de BitcoinCore, accediendo a Archivo>Direcciones de Recepcion.
* La llave privada se puede obtener abriendo la consola de comandos (Ayuda>Ventana de Depuración) y corriendo el commando  
`> dumprivkey "llavepublica"`


**Nota:** Este proyecto se validó en Mac OSX y en Ubuntu, utilizando la red Testnet del Bitcoin blockchain. 
**Nota2:** Se recomienda utilizar los scripts automatizados: script-tools, script-issuer, script-viewer y script. Este último tiene la única función de llamar a los anteriores.  

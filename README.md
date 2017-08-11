# ElectriCERT
Implementación de un sistema para emitir certificados en un blockchain para la Escuela de Ingeniería Eléctrica de la Universidad de Costa Rica. Basado en el proyecto abierto Blockcerts. 

# Instalación
Antes de empezar se deben tener los siguientes programas instalados:
* Python 2.7
* Python 3.5 o superior
* Python Virtual Enviroment
* BitcoinCore
  - Puede guiarse utilizando los siguientes links: BitcoinCore para [cualquier OS](https://github.com/bitcoin/bitcoin/tree/master/doc) o especifícamente para [OSX](https://github.com/bitcoin/bitcoin/blob/master/doc/build-osx.md)
  - BitcoinCore utiliza un archivo de configuración usualmente llamado [bitcoin.conf](https://es.bitcoin.it/wiki/Ejecuci%C3%B3n_de_Bitcoin#Archivo_de_configuraci.C3.B3n_Bitcoin.conf). En este repositorio se encuentra un archivo de configuración que puede tomar como ejemplo.

# Cert-tools
Primero se instalan todos los requirimientos de Python.
`> cd cert-tools`
`> pip install .`
Luego se debe configurar la aplicacion. El archivo de configuración se llama confx.ini.
Algunos parámetros importantes a cambiar son:
* certificate_description: la descripción del certificado. 
* certificate_title: el título del certificado. 
* roster: el archivo roster.csv es el archivo que debe contener los nombres de los recipientes de los certificados a emitir. 
* issuer_public_key: la llave pública obtenida de BitcoinCore. 
* issuer_id: es un archivo .json que contiene los datos del emisor. 

# BitcoinCore
Una vez se tiene instalado y corriendo BitcoinCore, se debe obtener una dirección de recepcion (llave pública) y su respectiva llave privada.
* La llave pública se puede obtener desde la ventana de BitcoinCore, accediendo a Archivo>Direcciones de Recepcion.
* La llave privada se puede obtener abriendo la consola de comandos (Ayuda>Ventana de Depuración) y corriendo el commando
`> dumprivkey "llavepublica"`


**Nota:** Este proyecto se validó en Mac OSX y en Ubuntu, utilizando la red Testnet del Bitcoin blockchain. 


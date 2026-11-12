# Chat por consola con Python

Chat en tiempo real desarrollado con Python y sockets TCP, que permite conectar varios dispositivos para intercambiar mensajes mediante la consola.

El proyecto utiliza programación multihilo para atender simultáneamente a varios clientes y permite identificar a los participantes mediante nombres de usuario.

## Características

- Comunicación entre varios clientes mediante TCP.
- Envío y recepción de mensajes en tiempo real.
- Atención simultánea de conexiones mediante hilos.
- Registro y comprobación de nombres de usuario.
- Notificación cuando un usuario se desconecta.
- Interfaz de consola mejorada mediante `prompt_toolkit`.

## Tecnologías y librerías

- **Python 3:** lenguaje de programación.
- **socket:** comunicación mediante sockets TCP.
- **threading:** ejecución simultánea de tareas.
- **sys:** gestión de argumentos y salida del programa.
- **re:** validación del formato de direcciones IPv4.
- **pathlib:** gestión de rutas de archivos.
- **prompt_toolkit:** mejora de la entrada de texto en consola.

## Obtener el proyecto

Clona el repositorio:

**Windows y Linux:**

```bash
git clone URL_DEL_REPOSITORIO
cd chat-consola
```

## Instalación

Crea un entorno virtual e instala las dependencias.

**Windows (PowerShell):**

```powershell
python -m venv env
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\env\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Linux:**

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Ejecución

### 1. Iniciar el servidor

En el equipo que funcionará como servidor, ejecuta:

```bash
python server.py
```

El servidor quedará a la espera de conexiones entrantes utilizando el puerto TCP `50324`.

### 2. Conectar un cliente

Desde otro equipo, ejecuta:

```bash
python cliente.py IP_DEL_SERVIDOR
```

Ejemplo:

```bash
python cliente.py 192.168.0.7
```

Sustituye la dirección por la IP local del equipo donde se está ejecutando el servidor.

### 3. Utilizar el chat

Al conectarse, el cliente deberá introducir un nombre de usuario disponible.

Una vez registrado, podrá enviar y recibir mensajes desde la consola.

Para salir del chat, escribe:

```text
exit
```

## Almacenamiento de usuarios

Los nombres de usuario se almacenan en el archivo:

```text
usuarios/
└── users.txt
```

La ruta se construye automáticamente utilizando la ubicación de `server.py`, por lo que no es necesario modificarla manualmente en el código.

## Conexión entre redes

Los dispositivos pueden conectarse desde una misma red local utilizando la dirección IP del equipo servidor.

Para permitir conexiones a traves de internet utilize la IP Publica. Es necesario configurar el **redireccionamiento de puertos (Port Forwarding)** en el router, dirigiendo el puerto TCP `50324` hacia la dirección IP local del equipo servidor. También debe permitirse ese puerto en el firewall.

Esto permite que diferentes personas, incluso desde otras redes, puedan conectarse al servidor y comunicarse.

**Nota de seguridad:** exponer un servidor directamente a Internet implica riesgos. Antes de utilizarlo públicamente, se recomienda implementar autenticación adecuada, cifrado de las comunicaciones y medidas de protección contra conexiones no autorizadas.

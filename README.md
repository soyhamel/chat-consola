# Chat por consola con Python

Chat en tiempo real desarrollado con Python y sockets TCP, que permite conectar varios dispositivos para intercambiar mensajes mediante la consola.

## Librerías

- `socket`: comunicación TCP.
- `threading`: atención simultánea de clientes.
- `sys`: gestión del programa.
- `prompt_toolkit`: mejora la entrada de texto en consola.

## Obtener el proyecto

Clona el repositorio:

**Windows y Linux:**

```bash
git clone URL_DEL_REPOSITORIO
cd chat-consola
```

Instala las dependencias:

**Windows:**

```powershell
python -m venv env
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

1. Ejecuta `server.py` en el equipo que funcionará como servidor.
2. Configura la dirección IP del servidor en `cliente.py`.

```
cliente.connect(('IP SERVIDOR', 50324))
```

3. Ejecuta `cliente.py` desde los dispositivos que quieran conectarse.
4. Cambia la ruta del archivo `users.txt`.

```
with open(r'RUTA_ARCHIVO', 'a') as archivo:
```

## Conexión entre redes

Los dispositivos pueden conectarse desde la misma red utilizando la IP local del servidor.

Para permitir conexiones desde otras redes, es necesario configurar el **redireccionamiento de puertos (Port Forwarding)** en el router, dirigiendo el puerto TCP `50324` hacia la IP local del equipo servidor. También debe permitirse ese puerto en el firewall.

Esto permite que diferentes personas, incluso desde otras redes, puedan conectarse y chatear.

**Nota:** Exponer el servidor a Internet implica riesgos de seguridad. Se recomienda implementar medidas de protección antes de utilizarlo públicamente.
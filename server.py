import socket, threading
from pathlib import Path

clientes = []  # Almacena los sockets de los clientes conectados.
BASE_DIR = Path(__file__).resolve().parent

RUTA_USUARIOS = BASE_DIR / 'usuarios' / 'users.txt'
RUTA_CREAR_FILE = BASE_DIR / 'usuarios'

with open(RUTA_USUARIOS, 'w') as archivo:
    archivo.write('')


def conexion(cliente_actual, direccion):
    nombre_usuario = ''
    print(f'Cliente conectado: {direccion[0]}')
    clientes.append(cliente_actual)

    with open(RUTA_USUARIOS, 'r', encoding='utf-8') as archivo:
        for linea in archivo:
            c_actual, nombres = linea.split(':', 1)

            if c_actual == str(cliente_actual):
                nombre_usuario = nombres
                break

    try:
        while True:
            # Recibe el mensaje y elimina el salto de línea final.
            mensaje_cliente = cliente_actual.recv(1024).decode('utf-8').rstrip('\n')
            
            if mensaje_cliente == 'exit':
                for cliente in clientes:
                    cliente.sendall(f'{nombre_usuario.strip()} SE DESCONECTO\n'.encode())
                cliente_actual.close()
                
                if cliente_actual in clientes:
                    clientes.remove(cliente_actual)
                
                break

            for cliente in clientes:
                if len(clientes) == 1:
                    mensaje_cliente = b'No hay usuarios conectados actualmente, intentelo mas tarde.\n'
                    cliente_actual.sendall(mensaje_cliente)

                elif cliente is not cliente_actual:
                    print(nombre_usuario)
                    cliente.sendall(f'{nombre_usuario.strip()}: {mensaje_cliente}\n'.encode())

    except ConnectionAbortedError:
        print(f'Cliente desconectado: {direccion[0]}')
        clientes.remove(cliente_actual)
        cliente_actual.close()
        
    except ConnectionResetError:
        # Detecta la desconexión y elimina el cliente de la lista.
        print(f'Cliente desconectado: {direccion[0]}')
        clientes.remove(cliente_actual)
        cliente_actual.close()


def crear_user(cliente_actual):
    usuarios_encontrados = ''
    lista_nombres = []
    zzz = ''
    nombre = ''

    # Abre el archivo donde se almacenan las IP y sus respectivos usuarios.
    try:
        with open(RUTA_USUARIOS, 'r', encoding='utf-8') as usuarios:

            usuarios_encontrados = usuarios.read()
            print(usuarios_encontrados)

            for usuario in usuarios_encontrados.splitlines():
                usuario = str(usuario)
                zzz, nombre = usuario.split(':', 1)
                lista_nombres.append(nombre)

            while True:
                try:
                    usuario_registrado = cliente_actual.recv(1024).decode('utf-8')
                except ConnectionAbortedError, ConnectionResetError:
                    pass

                # verifica si el usuario agregado esta disponible
                if not usuario_registrado in lista_nombres:
                    cliente_actual.sendall(b'ok')
                    break
                else:
                    # Indica al cliente que debe registrar un nombre.
                    cliente_actual.sendall(b'nofound')
                    print('El nombre de usuario ya existe, vuelva a intentar.')

            # Guarda la nueva relación entre IP y nombre de usuario.
            with open(RUTA_USUARIOS, 'a', encoding='utf-8') as archivo:
                archivo.write(f'{cliente_actual}:{usuario_registrado}\n')


            # return cliente_actual.sendall(usuario_registrado.encode())
        
    except FileNotFoundError:
        RUTA_CREAR_FILE.mkdir(exist_ok=True)
        (RUTA_CREAR_FILE / 'users.txt').touch(exist_ok=True)

        return cliente_actual.sendall('ERROR\nNo se pudo agg el nombre. Vuelva a intentarlo'.encode())


# Crea el socket del servidor utilizando IPv4 y TCP.
server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.bind(('0.0.0.0', 50324))  # Asocia el servidor a todas las interfaces de red.
server.listen()  # Permite recibir conexiones entrantes.


def funciones_hilo(cliente_actual, direccion):
    crear_user(cliente_actual)
    conexion(cliente_actual, direccion)

while True:
    print('Esperando conexion')

    cliente_actual, direccion = server.accept()  # Acepta una conexión entrante.

    # Crea un hilo independiente para las funciones
    hilo = threading.Thread(
        target=funciones_hilo,
        args=(cliente_actual, direccion)
    )

    hilo.start()
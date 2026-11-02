import socket, threading

clientes = []  # Almacena los sockets de los clientes conectados.

def conexion(cliente_actual, direccion):
    print(f'Cliente conectado: {direccion[0]}')
    clientes.append(cliente_actual)

    try:
        while True:
            # Recibe el mensaje y elimina el salto de línea final.
            mensaje_cliente = cliente_actual.recv(1024).decode('utf-8').rstrip('\n')

            for cliente in clientes:
                if len(clientes) == 1:
                    # Indicador 0: no existen otros usuarios conectados.
                    existen = 0
                    mensaje_cliente = b'No hay usuarios conectados actualmente, intentelo mas tarde.\n'
                    cliente_actual.sendall(f'{existen}|{mensaje_cliente.decode("utf-8")}\n'.encode('utf-8'))

                elif cliente is not cliente_actual:
                    # Indicador 1: existen otros usuarios y se reenvía el mensaje.
                    existen = 1
                    cliente.sendall(f'{existen}|{mensaje_cliente}\n'.encode('utf-8'))

    except ConnectionAbortedError:
        print(f'Cliente desconectado: {direccion[0]}')
        clientes.remove(cliente_actual)
        cliente_actual.close()
        
    except ConnectionResetError:
        # Detecta la desconexión y elimina el cliente de la lista.
        print(f'Cliente desconectado: {direccion[0]}')
        clientes.remove(cliente_actual)
        cliente_actual.close()


def crear_user(cliente_actual, direccion):
    usuario_encontrado = ''
    lista_nombre = []

    # Abre el archivo donde se almacenan las IP y sus respectivos usuarios.
    try:
        with open(r'C:\Users\dermi\OneDrive\Desktop\proyectos-reales\chat-consola\usuarios\users.txt', 'r') as usuarios:
            usuario_encontrado = ''

            direcciones = usuarios.read()

            for linea in direcciones.splitlines():
                # Separa la dirección IP del nombre de usuario.
                direccion_archivo, nombre = linea.split(':', 1)
                lista_nombre.append(nombre)

                # Comprueba si la IP ya tiene un usuario registrado.
                if direccion[0] == direccion_archivo:
                    usuario_encontrado = nombre
                    return cliente_actual.sendall(usuario_encontrado.encode())

            if usuario_encontrado == '':
                while True:
                    # Indica al cliente que debe registrar un nombre.
                    no_found = b'nofound'
                    cliente_actual.sendall(no_found)

                    usuario_encontrado = cliente_actual.recv(1024).decode('utf-8')

                    # Comprueba que el nombre elegido no esté registrado.
                    if not usuario_encontrado in lista_nombre:
                        break

                    print('El nombre de usuario ya existe, vuelva a intentar.')

                # Guarda la nueva relación entre IP y nombre de usuario.
                with open(r'C:\Users\dermi\OneDrive\Desktop\proyectos-reales\chat-consola\usuarios\users.txt', 'a') as archivo:
                    archivo.write(f'{direccion[0]}:{usuario_encontrado}\n')

                return cliente_actual.sendall(usuario_encontrado.encode())
    except FileNotFoundError:
        return cliente_actual.sendall('El archivo users.txt no existe comuniquese con el dueño del servidor (Hamel la kbra) pa que lo solucione'.encode())


# Crea el socket del servidor utilizando IPv4 y TCP.
server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.bind(('0.0.0.0', 50324))  # Asocia el servidor a todas las interfaces de red.
server.listen()  # Permite recibir conexiones entrantes.


while True:
    print('Esperando conexion')

    cliente_actual, direccion = server.accept()  # Acepta una conexión entrante.
    
    # Comprueba o registra el usuario.
    hilo_nombre = threading.Thread(
        target=crear_user,
        args=(cliente_actual, direccion)  
    )
    
    hilo_nombre.start()

    # Crea un hilo independiente para atender al cliente.
    hilo = threading.Thread(
        target=conexion,
        args=(cliente_actual, direccion)
    )

    hilo.start()
import socket, threading, sys
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout


# Crea el socket del cliente utilizando IPv4 y TCP.
cliente = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

cliente.settimeout(4)  # Establece un tiempo máximo de espera para las operaciones de recepción.


def recibir_mensaje():
    buffer = b''  # Almacena temporalmente los datos recibidos.

    while True:
        try:
            datos = cliente.recv(1024)  # Recibe hasta 1024 bytes.

            if not datos:
                break

            buffer += datos  # Acumula los datos recibidos.

            # Procesa los mensajes completos identificados por un salto de línea.
            while b'\n' in buffer:
                respuesta, buffer = buffer.split(b'\n', 1)

                if not respuesta:
                    continue

                # Separa el indicador del contenido del mensaje.
                existen, mensaje = respuesta.decode('utf-8').split('|', 1)

                if existen == '1':
                    print(f'Cliente: {mensaje}')
                else:
                    print(f'{mensaje}')

        except TimeoutError:
            pass
        except ConnectionResetError:
            print('El servidor se ha desconectado.')
            sys.exit()
        except BrokenPipeError:
            print('El servidor se ha desconectado.')
            sys.exit()


try:
    # Establece la conexión con el servidor y recibe el nombre del usuario.
    cliente.connect(('IP SERVIDOR', 50324))
    nombre_usuario = cliente.recv(1024).decode('utf-8')

    # Si no existe un usuario registrado, solicita uno nuevo.
    if nombre_usuario == 'nofound':
        nombre_usuario = input('Ingrese su nombre de usuario> ')
        cliente.sendall(nombre_usuario.encode())

except ConnectionRefusedError as error:
    print(f'Intente conectarse mas tarde: {error}')
    sys.exit()
except TimeoutError as error:
    print(f'No se pudo conectar al servidor')
    sys.exit()


sesion = PromptSession()

# Ejecuta la recepción de mensajes en un hilo independiente.
hilo = threading.Thread(
    target=recibir_mensaje,
    daemon=True
)

hilo.start()

# Permite escribir mensajes mientras se reciben otros de forma simultánea.
with patch_stdout():
    while True:
        mensaje = sesion.prompt(f'{nombre_usuario}>')
        cliente.sendall((mensaje + '\n').encode('utf-8'))

cliente.close()
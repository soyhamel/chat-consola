import socket, threading, sys, re
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout

print('Escriba "exit" en minuscula para salir del chat.')

# Crea el socket del cliente utilizando IPv4 y TCP.
cliente = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

cliente.settimeout(4)  # Establece un tiempo máximo de espera para las operaciones de recepción.

if len(sys.argv) != 2:
    print('Uso incorrecto.')
    print(f'Ejemplo: python {sys.argv[0]} 192.168.1.10')
    sys.exit(1)

ip_server = sys.argv[1]

n = re.search(r'(\b25[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}', ip_server)

if not n:
    print('IP incorrecta, vuelva a intentar.')
    sys.exit()


print(f'IP {ip_server} ingresada correctamente. Esperando conexión...')



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
                mensaje = respuesta.decode('utf-8')

                print(f'{mensaje}')

        except TimeoutError:
            pass
        except ConnectionResetError:
            print('El servidor se ha desconectado.')
            sys.exit()
        except BrokenPipeError:
            print('El servidor se ha desconectado.')
            sys.exit()
        except OSError as error:
            print('La conexión ha sido cerrada.')
            break


try:
    # Establece la conexión con el servidor y recibe el nombre del usuario.
    cliente.connect((ip_server, 50324))

    nombre_usuario = input('Ingrese su nombre de usuario> ')
    cliente.sendall(nombre_usuario.encode())


    # Si no existe un usuario registrado, solicita uno nuevo.
    while True:
        respuesta = cliente.recv(1024).decode('utf-8')

        if respuesta == 'nofound':
            print('Usuario ya existe. Vuelva a intentarlo')
            
            nombre_usuario = input('Ingrese su nombre de usuario> ')
            cliente.sendall(nombre_usuario.encode())
        
        elif respuesta == 'ok':
            print('Usuario registrado correctamente.')
            break

except ConnectionRefusedError as error:
    print(f'Intente conectarse mas tarde: {error}')
    sys.exit()
except TimeoutError as error:
    print(f'No se pudo conectar al servidor')
    sys.exit()


sesion = PromptSession()

# Ejecuta la recepción de mensajes en un hilo independiente.
try:
    hilo = threading.Thread(
        target=recibir_mensaje,
        daemon=True
    )
    hilo.start()
except:
    pass


# Permite escribir mensajes mientras se reciben otros de forma simultánea.
with patch_stdout():
    while True:
        mensaje = sesion.prompt(f'{nombre_usuario}> ')

        if mensaje == '':
            continue

        try:
            cliente.sendall((mensaje + '\n').encode())
            if mensaje == 'exit':
                cliente.close()
                sys.exit()
        except BrokenPipeError as e:
            print(f'Error servidor desconectado: {e}')
        except ConnectionResetError as e:
            print(f'Error servidor desconectado: {e}')
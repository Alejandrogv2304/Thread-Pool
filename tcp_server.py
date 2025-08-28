import socket
import threading
import logging
from datetime import datetime

# Configuración del logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tcp_server.log'),
        logging.StreamHandler()
    ]
)

class TCPCharCounterServer:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.socket = None
        self.running = False
        
    def count_last_char_occurrences(self, message):
        """
        Cuenta las ocurrencias del último carácter en el mensaje completo
        
        Args:
            message (str): El mensaje recibido
            
        Returns:
            dict: Diccionario con información del conteo
        """
        if not message:
            return {
                'message': message,
                'last_char': None,
                'count': 0,
                'error': 'Mensaje vacío'
            }
        
        last_char = message[-1]
        count = message.count(last_char)

        with open("pares.txt", "a") as archivo_pares, open("impares.txt", "a") as archivo_impares:
         # Supongamos que tienes una lista de números o un cálculo
           
          if count % 2 == 0:
            archivo_pares.write(str(count) + "\n")   # Guardar pares en pares.txt
          else:
            archivo_impares.write(str(count) + "\n") # Guardar impares en impares.txt
        
        return {
            'message': message,
            'last_char': last_char,
            'count': count,
            'message_length': len(message)
        }
    
    def handle_client(self, client_socket, client_address):
        """
        Maneja la conexión de un cliente individual
        """
        logging.info(f"Nueva conexión desde {client_address}")
        
        try:
            while self.running:
                # Recibir datos del cliente
                data = client_socket.recv(1024).decode('utf-8').strip()
                
                if not data:
                    break
                
                logging.info(f"Mensaje recibido de {client_address}: '{data}'")
                
                # Procesar el mensaje
                result = self.count_last_char_occurrences(data)
                
                # Crear respuesta
                if 'error' in result:
                    response = f"ERROR: {result['error']}\n"
                else:
                    response = (
                        f"RESULTADO:\n"
                        f"Mensaje: '{result['message']}'\n"
                        f"Último carácter: '{result['last_char']}'\n"
                        f"Ocurrencias: {result['count']}\n"
                        f"Longitud total: {result['message_length']}\n"
                        f"---\n"
                    )
                
                # Enviar respuesta al cliente
                client_socket.send(response.encode('utf-8'))
                logging.info(f"Respuesta enviada a {client_address}: {result}")
                
        except Exception as e:
            logging.error(f"Error manejando cliente {client_address}: {e}")
        finally:
            client_socket.close()
            logging.info(f"Conexión cerrada con {client_address}")
    
    def start_server(self):
        """
        Inicia el servidor TCP
        """
        try:
            # Crear socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Bind y listen
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            self.running = True
            
            logging.info(f"Servidor iniciado en {self.host}:{self.port}")
            logging.info("Esperando conexiones...")
            
            while self.running:
                try:
                    # Aceptar conexiones
                    client_socket, client_address = self.socket.accept()
                    
                    # Crear hilo para manejar cliente
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except socket.error as e:
                    if self.running:
                        logging.error(f"Error aceptando conexión: {e}")
                    
        except Exception as e:
            logging.error(f"Error iniciando servidor: {e}")
        finally:
            self.stop_server()
    
    def stop_server(self):
        """
        Detiene el servidor
        """
        self.running = False
        if self.socket:
            self.socket.close()
        logging.info("Servidor detenido")

def main():
    # Configuración del servidor
    HOST = '0.0.0.0'  # Cambiar si necesitas acceso externo
    PORT = 5050         # Puerto a utilizar
    
    # Crear y iniciar servidor
    server = TCPCharCounterServer(HOST, PORT)
    
    try:
        server.start_server()
    except KeyboardInterrupt:
        logging.info("Deteniendo servidor...")
        server.stop_server()

if __name__ == "__main__":
    main()
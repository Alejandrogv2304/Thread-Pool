import socket
import time

def test_tcp_client(host='localhost', port=5050, messages=None):
    """
    Cliente de prueba para el servidor TCP
    """
    if messages is None:
        messages = [
            "hello",
            "programming",
            "aaaaaa",
            "test message",
            "python rocks",
            "1234554321",
            "a",
            ""  # Mensaje vacío para probar manejo de errores
        ]
    
    print(f"Conectando al servidor {host}:{port}")
    
    try:
        # Crear conexión
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        print("Conexión establecida\n")
        
        for i, message in enumerate(messages, 1):
            print(f"=== Prueba {i} ===")
            print(f"Enviando: '{message}'")
            
            # Enviar mensaje
            client_socket.send((message + '\n').encode('utf-8'))
            
            # Recibir respuesta
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Respuesta del servidor:\n{response}")
            
            time.sleep(1)  # Pausa entre mensajes
        
        print("Todas las pruebas completadas")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        print("Conexión cerrada")

if __name__ == "__main__":
    test_tcp_client()
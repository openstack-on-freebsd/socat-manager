import argparse
import socket

def send_request(action, device, port):
    client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        client_socket.connect("/tmp/socket_service.sock")
        
        request = f"{action} {device} {port}"
        client_socket.send(request.encode())
        
        response = client_socket.recv(1024).decode()
        print(response)
    
    except ConnectionError:
        print("Unable to connect to the server.")
    
    finally:
        client_socket.close()

def main():
    parser = argparse.ArgumentParser(description="Unix socket client for the server.")
    parser.add_argument("action", choices=["ADD", "DEL"], help="Action to perform (ADD or DEL)")
    parser.add_argument("device", type=str, help="Device name")
    parser.add_argument("port", type=int, help="Port number")
    
    args = parser.parse_args()
    
    send_request(args.action, args.device, args.port)

if __name__ == "__main__":
    main()


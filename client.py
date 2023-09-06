import argparse
import socket

def send_request(action, device, port):
    # 创建Unix socket连接
    client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        # 连接到服务器的Unix socket
        client_socket.connect("/tmp/socket_service.sock")
        
        # 发送请求
        request = f"{action} {device} {port}"
        client_socket.send(request.encode())
        
        # 接收和打印服务器的响应（如果有）
        response = client_socket.recv(1024).decode()
        print(response)
    
    except ConnectionError:
        print("无法连接到服务器。")
    
    finally:
        client_socket.close()

def main():
    parser = argparse.ArgumentParser(description="Unix socket client for the server.")
    parser.add_argument("action", choices=["ADD", "DEL"], help="Action to perform (ADD or DEL)")
    parser.add_argument("device", type=str, help="Device name")
    parser.add_argument("port", type=int, help="Port number")
    
    args = parser.parse_args()
    
    # 发送请求到服务器
    send_request(args.action, args.device, args.port)

if __name__ == "__main__":
    main()


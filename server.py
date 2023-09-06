import os
import signal
import socket
import subprocess
import sys
import time

# Unix socket file path
SOCKET_PATH = "/tmp/socket_service.sock"

# File to store socat process information
PID_FILE = "socat_pid.txt"

def create_socat_process(device, port):
    # Construct the socat command
    # Example: /usr/local/bin/socat file:/dev/nmdm21B,ispeed=9600,ospeed=9600,raw,echo=0 tcp-listen:10014,bind=0.0.0.0,reuseaddr,fork
    socat_cmd = [
        "/usr/local/bin/socat",
        f"FILE:{device},ispeed=9600,ospeed=9600,raw,echo=0",
        f"TCP-LISTEN:{port},bind=0.0.0.0,fork,reuseaddr"
    ]
    
    # Use subprocess to run socat in the background
    socat_process = subprocess.Popen(socat_cmd, preexec_fn=os.setsid)  # Use os.setsid to create a new process group
    return socat_process

def save_pid_to_file(pid, device, port):
    with open(PID_FILE, "a") as file:
        file.write(f"{pid} {device} {port}\n")

def check_pid_file():
    if not os.path.exists(PID_FILE):
        with open(PID_FILE, "w") as file:
            file.write("")

def handle_zombies():
    while True:
        try:
            # Reap child processes
            _, status = os.waitpid(-1, os.WNOHANG)
            if _ == 0:
                break
        except OSError:
            break

def main():
    try:
        # Check and create the PID file
        check_pid_file()
        
        # Create a Unix socket
        server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server_socket.bind(SOCKET_PATH)
        server_socket.listen(1)
        print("Waiting for connections...")
        
        # Main loop
        while True:
            connection, client_address = server_socket.accept()
            try:
                data = connection.recv(1024).decode()
                if not data:
                    continue

                # Parse the parameters
                action, device, port = data.split()
                
                if action == "ADD":
                    # Create a socat process
                    socat_process = create_socat_process(device, port)
                    save_pid_to_file(socat_process.pid, device, port)
                    print(f"Generated socat process, PID: {socat_process.pid}")

                elif action == "DEL":
                    # Find and terminate the socat process based on device and port
                    with open(PID_FILE, "r") as file:
                        lines = file.readlines()
                    for line in lines:
                        pid, dev, p = line.strip().split()
                        if dev == device and p == port:
                            # Send SIGTERM to the process group (including socat and its child processes)
                            os.killpg(int(pid), signal.SIGTERM)
                            print(f"Terminated socat process, PID: {pid}")
                            # Remove the line from the file
                            lines.remove(line)
                            with open(PID_FILE, "w") as file:
                                file.writelines(lines)
                            break
            except Exception as e:
                print(f"An error occurred: {e}")
            finally:
                connection.close()
                # Handle zombies
                handle_zombies()

    except KeyboardInterrupt:
        print("Service has been terminated.")
        os.unlink(SOCKET_PATH)
        sys.exit(0)

if __name__ == "__main__":
    main()


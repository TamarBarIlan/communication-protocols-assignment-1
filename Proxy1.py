import socket
import threading
import time
from threading import Lock


PROXY_1_IP = '127.0.0.1'
PROXY_1_PORT = 5000

PROXY_2_IP = '127.0.0.3'
PROXY_2_PORT = 5002

DIODE_IP= '127.0.0.2'
DIODE_PORT = 5001

BUFFER_SIZE = 8192

SEPERATOR = '<SEPERATOR>'

PROXY_3_PORT = 5004
PROXY_3_IP = '127.0.0.5'

flag = True
lock = Lock()
def proxy_1():
    # Create a TCP socket
    proxy_socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy_socket_tcp.bind(('0.0.0.0', PROXY_1_PORT))
    proxy_socket_tcp.listen(1)
    print('Proxy is ready listening to Send')

    # Create a UDP socket
    proxy_socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    proxy_socket_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('UDP socket was created')

    # Create connection to Proxy3 with TCP socket
    proxy_3_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_3_socket.connect((PROXY_3_IP, PROXY_3_PORT))
    print('Connect to Proxy3')
    list = []

    while True:
        global flag, lock
        send_socket, address = proxy_socket_tcp.accept()
        # Connection succeeded with Send
        with send_socket:

            if flag: # Prints once
                print(f"Connection established with {address}")
                flag = False

            receive_data(send_socket,list)
            send_data(proxy_socket_udp, proxy_3_socket, list)
            list.clear()

        send_socket.close()

    proxy_socket_udp.close()
    proxy_socket_tcp.close()


def send_data(proxy_socket_udp, proxy_3_socket, list):
    if list:
        i = 0
        while i < len(list):
            data = list[i] + SEPERATOR.encode() + str(i).encode()
            proxy_socket_udp.sendto(data, (PROXY_2_IP, PROXY_2_PORT))
            print(f'Packet was sent to Diode, length: {len(data)}')
            time.sleep(0.3)
            proxy_3_socket.send(str(i).encode())
            time.sleep(0.3)
            ack = proxy_3_socket.recv(BUFFER_SIZE) # Receives ack from Proxy3
            if ack:
                ack = ack.decode()
                if ack == 'ack':
                    i = i + 1
                    print("Packet arrived to Proxy2")
                else:
                   print("Trying to send the packet again")
            else:
                print("Error occurred with sending ack")
                return
        print("All packets were sent")
    else:
        print('No packets in list')


def receive_data(send_socket, list):

    data = send_socket.recv(BUFFER_SIZE)
    while data:
        print(f'Packet was received from Send, length: {len(data)}')
        list.append(data)
        data = send_socket.recv(BUFFER_SIZE)
    print('Packet was not received')



if __name__ == '__main__':
    proxy_1()

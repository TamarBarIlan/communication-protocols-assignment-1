import socket
import time

PROXY_1_IP = '127.0.0.1'
PROXY_2_PORT_UDP = 5002

PROXY_2_IP = '127.0.0.3'
PROXY_2_PORT_TCP = 5003

END_USER_IP = '127.0.0.4'

BUFFER_SIZE = 10000

PROXY_3_IP = '127.0.0.5'
PROXY_3_PORT = 5005

flag = True
SEPERATOR = '<SEPERATOR>'

def proxy_2():
    # Create a UDP socket
    proxy_socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    proxy_socket_udp.bind(('0.0.0.0', PROXY_2_PORT_UDP))
    proxy_socket_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy_socket_udp.settimeout(5)
    print('UDP socket is ready')

    # Create a TCP socket
    proxy_socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy_socket_tcp.bind(('0.0.0.0', PROXY_2_PORT_TCP))
    proxy_socket_tcp.listen(1)
    print('TCP socket is ready')

    # Create connection to Proxy3 with TCP socket
    proxy_3_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_3_socket.connect((PROXY_3_IP, PROXY_3_PORT))
    print('Connect to Proxy3')

    while True:
        global flag
        end_user_socket, end_user_address = proxy_socket_tcp.accept()

        if flag:
            print(f'Connection established with {end_user_address}')
            flag = False

        to_close = receive_and_send(proxy_socket_udp, proxy_3_socket, end_user_socket)

        if to_close == 'yes':
            end_user_socket.close()


    proxy_socket_udp.close()
    proxy_socket_tcp.close()

def receive_and_send(proxy_socket_udp, proxy_3_socket, end_user_socket):
    received = 'not'
    while received == 'not':
        try:
            print('Waiting for receiving packets')
            data, address = proxy_socket_udp.recvfrom(BUFFER_SIZE)
            while data:
                received = 'yes'
                print(f'Packet was received from Diode, length: {len(data)}')
                time.sleep(0.3)
                data, num = data.split(SEPERATOR.encode())
                proxy_3_socket.send(num) # sends to Proxy3 the packet number
                ack = proxy_3_socket.recv(BUFFER_SIZE) # Receives ack from Proxy3
                ack = ack.decode()
                if ack == 'ack':
                    end_user_socket.send(data)
                    print(f'Packet was sent to EndUser, length: {len(data)}')
                    time.sleep(0.3)
                else:
                    print('Packet was not sent to EndUser')
                data, address = proxy_socket_udp.recvfrom(BUFFER_SIZE)

        except socket.timeout:
            print('Timeout')
            pass

    return received


if __name__ == '__main__':
    proxy_2()
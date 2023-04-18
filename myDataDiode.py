import socket
import time

DIODE_PORT = 5001

PROXY_2_IP = '127.0.0.3'
PROXY_2_PORT = 5002

BUFFER_SIZE = 10000
def mydiode(allowed_addrs):

    # Create a UDP socket
    diode_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    diode_socket.bind(('0.0.0.0', DIODE_PORT))
    diode_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('UDP socket is ready')

    while True:

        data, address = diode_socket.recvfrom(BUFFER_SIZE)
        print(f'Packet was received from Proxy1, length: {len(data)}')
        time.sleep(0.3)
        if data and address[0] in allowed_addrs:
            diode_socket.sendto(data,(PROXY_2_IP,PROXY_2_PORT))
            print(f'Packet was sent to Proxy2, length: {len(data)}')
            time.sleep(0.3)
        else:
            print(f'Dropping packet from {address}')

    diode_socket.close()

if __name__ == '__main__':
    allowed_addrs = ['127.0.0.1']
    mydiode(allowed_addrs)
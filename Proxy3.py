import socket
import time

PROXY_1_PORT = 5004

PROXY_2_PORT = 5005

BUFFER_SIZE = 1024

# This proxy is only for control
def proxy_3():
    # Create a TCP socket
    proxy_1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_1_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy_1_socket.bind(('0.0.0.0', PROXY_1_PORT))
    proxy_1_socket.listen(1)
    print('Proxy 3 is ready listening to Proxy1')

    # Create a TCP socket
    proxy_2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_2_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy_2_socket.bind(('0.0.0.0', PROXY_2_PORT))
    proxy_2_socket.listen(1)
    print('Proxy 3 is ready listening to Proxy2')

    while True:
        receive_socket_proxy1, address_proxy1 = proxy_1_socket.accept()
        receive_socket_proxy2, address_proxy2 = proxy_2_socket.accept()

        with receive_socket_proxy1 and receive_socket_proxy2:
            print(f'Connection established with {address_proxy1}')
            print(f'Connection established with {address_proxy2}')
            while True:
                data1 = receive_socket_proxy1.recv(BUFFER_SIZE)
                data2 = receive_socket_proxy2.recv(BUFFER_SIZE)
                # Checks if packets were received
                if data1 and data2:
                    print('Packets were received from both proxies')

                    # Converts from bits
                    data1 = int(data1)
                    data2 = int(data2)

                    if data1 != data2:
                        ack = 'nack'.encode()
                        receive_socket_proxy1.send(ack)
                        receive_socket_proxy2.send(ack)
                        print('nack was sent')

                    else:
                        ack = 'ack'.encode()
                        receive_socket_proxy1.send(ack)
                        receive_socket_proxy2.send(ack)
                        print('ack was sent')


    proxy_1_socket.close()
    proxy_2_socket.close()

if __name__ == '__main__':
    proxy_3()
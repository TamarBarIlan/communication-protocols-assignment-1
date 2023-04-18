import socket
import time
import hashlib

END_USER_IP = '127.0.0.4'

PROXY_2_IP = '127.0.0.3'
PROXY_2_PORT = 5003

BUFFER_SIZE = 8192
def receive_from_proxy():
    # Create connection to Proxy2
    receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receive_socket.connect((PROXY_2_IP, PROXY_2_PORT))
    print('Connect to Proxy2')


    # Receives packets from Proxy2
    received_hash, filename = receive_data(receive_socket)

    # Checksum
    check_hash(received_hash, filename)

    receive_socket.close()

def check_hash(received_hash, filename):

    hash_md5 = hashlib.md5()
    with open(filename, "rb") as file:
        for chunk in iter(lambda: file.read(BUFFER_SIZE), b""):
            hash_md5.update(chunk)

    if hash_md5.hexdigest() == received_hash:
        print('File received and its hash matched')
    else:
        print('File received but its hash did not match')

    file.close()

def receive_data(receive_socket):
    print('Start receiving packets')

    received_hash = receive_socket.recv(BUFFER_SIZE).decode()
    print(f'Packet was received, length: {len(received_hash)}')

    with open('file_from_send.txt', 'wb') as file:
        # Gets data in chunks
        data = receive_socket.recv(BUFFER_SIZE)

        while data:
            print(f'Packet received, length: {len(data)}')
            file.write(data)
            time.sleep(0.3)
            data = receive_socket.recv(BUFFER_SIZE)

    print('All packets received')
    file.close()
    return received_hash, 'file_from_send.txt'


if __name__ == '__main__':
    receive_from_proxy()
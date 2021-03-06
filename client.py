# Based on https://www.bogotobogo.com/python/python_network_programming_tcp_server_client_chat_server_chat_client_select.php

import sys
import socket
import select

def chat_client():
    if(len(sys.argv) < 3) :
        print('Usage : python chat_client.py hostname port')
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print('Unable to connect')
        sys.exit()

    print('Connected to remote host. You can start sending messages')
    sys.stdout.write('[Me] '); sys.stdout.flush()

    while 1:
        socket_list = [sys.stdin, s]

        # Get the list sockets which are readable
        ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])

        for sock in ready_to_read:
            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(4096).decode()
                if not data :
                    print('\nDisconnected from chat server')
                    sys.exit()
                if data[0] == "\r":
                    #print data
                    sys.stdout.write(data)
                    sys.stdout.write('[Me] '); sys.stdout.flush()
                else:
                    print("\rSystem message\n[Me] ")

            else :
                # user entered a message
                msg = sys.stdin.readline()
                s.send(str.encode(msg))
                sys.stdout.write('[Me] '); sys.stdout.flush()

if __name__ == "__main__":
    try:
        sys.exit(chat_client())
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)

#!/usr/bin/env python
#!/usr/bin/python

import socket
import sys
import argparse

HOST = ''
PORT = 27995
NUID = '001475954'
isSSLset = False

def send_Hello_message(s):
    str = 'cs5700spring2019 HELLO ' + NUID + '\n'
    s.sendall(str.encode())


def solveExpression(data):
    split_expression = data.decode("utf-8").split()
    res = eval(split_expression[2] + split_expression[3] + split_expression[4])
    res = round(res)
    return ('cs5700spring2019 ' + str(res) + '\n').encode()

def run():
    if isSSLset is True:
        print('SSL is set')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        #print('Connected')
        send_Hello_message(s)
        while True:
            data = s.recv(1024)
            data = data.decode("utf-8")
            print("Recd:: " + data + ".")
            if not data:
                #print('This is it: ' +data+ ".")
                #continue
                return

            if "STATUS" in data:
                print('Received message: ' + data)
                res = solveExpression(data.encode())
                print('Result message: ' + res.decode("utf-8"))
                s.sendall(res)

            # print('Recv: ' + data.decode("utf-8"))
            # res = solveExpression(data)
            # print('Result: ' + res.decode("utf-8"))
            # s.sendall(res)

            if "BYE" in data:
                print(data)
                return

        print('Connection Terminated')

def gatherArguments():

    global NUID
    global PORT
    global HOST
    global isSSLset

    parser = argparse.ArgumentParser(description = 'Refer proper syntax')
    parser.add_argument('hostname', help = 'Enter the hostname.')
    parser.add_argument('nuid', help = 'Enter the NUID')
    parser.add_argument('--port','-p', help = 'Enter port number (default: 27995)', default = 27995)
    parser.add_argument('--setSSL','-s', help = 'Add this option if SSL connection is required', action = 'store_true')
    args = parser.parse_args()

    if len(sys.argv) < 3:
        print('Not enough arguments')

    if args.port is not None:
        PORT = args.port

    if args.setSSL is True:
        isSSLset = True

    HOST = args.hostname

    NUID = args.nuid

if __name__ == '__main__':
    gatherArguments()
    run()

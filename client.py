#!/usr/bin/env python
#!/usr/bin/python

import socket
import sys
import argparse
import ssl
import logging

HOST = ''
PORT = 27995
NUID = '001475954'
isSSLset = False
isDebug = False
isInfo = False

def send_Hello_message(s):
    str = 'cs5700spring2019 HELLO ' + NUID + '\n'
    logging.debug('Sent Hello Message: ' + str + 'EOD')
    s.sendall(str.encode())


def solveExpression(data):
    split_expression = data.decode("utf-8").split()
    res = eval(split_expression[2] + split_expression[3] + split_expression[4])
    res = round(res)
    return ('cs5700spring2019 ' + str(res) + '\n').encode()

def run():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        global PORT
        if isSSLset is True:
            logger.info('SSL is Set')
            PORT = 27996
            s = ssl.wrap_socket(s, ssl_version=3)
        else:
            logger.info('SSL is not set')

        s.connect((HOST, PORT))
        logger.info('Connected to %s %s' % (HOST, PORT))

        send_Hello_message(s)

        while True:
            data = s.recv(1024)
            data = data.decode("utf-8")
            logger.debug('Data Received: ' + data + 'EOD')

            if not data:
                logger.debug('Empty string! Received message: '+ data + 'EOD')
                #continue
                return

            if "STATUS" in data:
                logger.debug('Status Message: ' + data + 'EOD')
                res = solveExpression(data.encode())
                logger.debug('Result Status message: ' + res.decode("utf-8") + 'EOD')
                s.sendall(res)

            # print('Recv: ' + data.decode("utf-8"))
            # res = solveExpression(data)
            # print('Result: ' + res.decode("utf-8"))
            # s.sendall(res)

            if "BYE" in data:
                logger.debug('Bye Message: ' + data + 'EOD')
                print(data)
                return

        logger.info('Connection Terminated')

def gatherArguments():

    global NUID
    global PORT
    global HOST
    global isSSLset
    global isDebug
    global isInfo

    parser = argparse.ArgumentParser(description = 'Refer proper syntax')
    parser.add_argument('hostname', help = 'Enter the hostname.')
    parser.add_argument('nuid', help = 'Enter the NUID')
    parser.add_argument('--port','-p', help = 'Enter port number (default: 27995)', default = 27995)
    parser.add_argument('--setSSL','-s', help = 'Add this option if SSL connection is required', action = 'store_true')
    parser.add_argument('--debug', '-d', help = 'Add this option if you want to see debug messages', action = 'store_true')
    parser.add_argument('--info', '-i', help = 'Add this option if you want to see info messages', action = 'store_true')
    args = parser.parse_args()

    if len(sys.argv) < 3:
        print('Not enough arguments')

    if args.port is not None:
        PORT = args.port

    if args.setSSL is True:
        isSSLset = True

    if args.debug is True:
        isDebug = True
    elif args.info is True:
        isInfo = True

    HOST = args.hostname

    NUID = args.nuid

if __name__ == '__main__':


    gatherArguments()

    if isDebug is True:
        logging.basicConfig(format='%(message)s',level = logging.DEBUG)
    elif isInfo is True:
        logging.basicConfig(format='%(message)s',level = logging.INFO)
    else:
        logging.basicConfig(format='%(message)s',level = logging.ERROR)

    logger = logging.getLogger(__name__)

    run()

#!/usr/bin/python
import socket
import sys
import argparse
import ssl
import logging

"""

This is a simple client for Project 1 of CS5700.
It has 2 positional arguments - hostname and NUID.
There are 2 optional arguments - SSL <-s> and PORT <-p port_number>.
The format of running the program are as follows:
./client <-p port> <-s> [hostname] [NEU ID]

It uses the inbuilt python libraries to connect to a specified server by sending a 'HELLO' message and solves the equations sent by the server in the 'STATUS' format as required.
It then sends the 'SOLUTION' message to the server.
It prints the secret key supplied in the 'BYE' message on the screen. Any other format would result in display of error message and  the termination of program.
The format of the messages are as follows:

STATUS:
cs5700spring2019 STATUS [a number] [a math operator] [another number]\n

SOLUTION:
cs5700spring2019 [the solution]\n

BYE:
cs5700spring2019 [a 64 byte secret flag] BYE\n

"""

HOST = ''
PORT = 27995
NUID = '001475954'
isSSLset = False
isDebug = False
isInfo = False
portSet = False

def send_Hello_message(s):
    """
	Sends the 'HELLO' message to the server in the format specified.
    """
    str = 'cs5700spring2019 HELLO ' + NUID + '\n'
    logging.debug('Sent Hello Message: ' + str + 'EOD')
    s.sendall(str.encode())


def solveExpression(data):
    """
	Solves the expression as spcified in the 'STATUS' message and sends the solution in the 'SOLUTION' format.
    """
    split_expression = data.decode("utf-8").split()
    res = eval(split_expression[2] + split_expression[3] + split_expression[4])
    return ('cs5700spring2019 ' + str(res) + '\n').encode()

def run():
    """
	Runs the control for the program. It creates a TCP socket using the socket library. If the SSL option is selected, it wraps the socket in an SSL wrapper ( and uses suitable port).
	A connection is then established to the server using the provided HOST and PORT.
	It runs an infinite loop that reads the messages from the server and takes the necessary actions:
		- First it logs the data received from the server.
		- Matches the message (data received from the server) to the known and accepted format of message (Either 'STATUS' or 'BYE')
		- Performs the required action based on the message sent by the server.
		- If the format is not followed, it prints an error message and returns the control.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    global PORT

    if isSSLset is True:
        logger.info('SSL is Set')
        logger.debug('portSet: %s' % portSet)
        if portSet == False:
            	PORT = 27996
        s = ssl.wrap_socket(s, ssl_version=3)
    else:
        logger.info('SSL is not set')

    logger.info('Request connection to %s %s' % (HOST, PORT))
    s.connect((HOST, PORT))
    logger.info('Connected to %s %s' % (HOST, PORT))

    send_Hello_message(s)

    while True:
        data = s.recv(1024)
        data = data.decode("utf-8")
        logger.debug('Data Received: ' + data + 'EOD')

        if not data:
            logger.debug('Empty string! Received message: '+ data + 'EOD')
            s.close()
            logger.info('Connection Closed after receiving empty string.')
            return

        if "STATUS" in data:
            logger.debug('Status Message: ' + data + 'EOD')
            res = solveExpression(data.encode())
            logger.debug('Result Status message: ' + res.decode("utf-8") + 'EOD')
            s.sendall(res)
            continue

        if "BYE" in data:
            logger.debug('Bye Message: ' + data + 'EOD')
            key = data.split()
            key = key[1]
            print(key)
            s.close()
            logger.info('Connection closed after BYE')
            return

        else:
            logger.debug('Unknown format - ' + data + 'EOD')
            logger.info('Connection closed after unknown format')
            s.close()
            return

    logger.info('Run completed.')

def gatherArguments():
    """
	This method is used to gather the arguments given by the user and set the required variables.
	It uses an inbuilt python library called argparse.
	To lnow more about this library, kindly go through the documentation on argparse.
    """
    global NUID
    global PORT
    global HOST
    global isSSLset
    global isDebug
    global isInfo
    global portSet

    parser = argparse.ArgumentParser(description = 'This is simple client program for project-1 for cs5700\n')
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
	if args.port == 27995:
        	portSet = False
	else:
		portSet = True

        PORT = int(args.port)

    if args.setSSL is True:
        isSSLset = True

    if args.debug is True:
        isDebug = True
    elif args.info is True:
        isInfo = True

    HOST = args.hostname

    NUID = args.nuid


if __name__ == '__main__':

   """
	This is the main method of the program. It gathers the arguments and then initializes a logger using the in-built logging library. It then gives the control to the run() method.
	If the run() method catches an exception, it is printed on the screen and the program exits.
   """

   gatherArguments()

   if isDebug is True:
       logging.basicConfig(filename = 'log', filemode ='w', format='%(message)s',level = logging.DEBUG)
   elif isInfo is True:
       logging.basicConfig(format='%(message)s',level = logging.INFO)
   else:
       logging.basicConfig(format='%(message)s',level = logging.ERROR)

   logger = logging.getLogger(__name__)

   try:
       run()
   except Exception as e:
       print(str(e))
       print('Exception found. Exiting the program.')

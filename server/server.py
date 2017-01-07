#!/usr/bin/env python

import socket
import os
import threading
import sys

host = '127.0.0.1'
port = int(sys.argv[1])

def file_handler(name, s, filename=''):
	if filename == '':
		filename = s.recv(1024)
	
	if os.path.isfile(filename):
		filesize = os.path.getsize(filename)
		s.send('EXISTS {}'.format(filesize))
		user_response = s.recv(1024)
		if user_response[:2] == 'OK':
			with open(filename, 'rb') as f:
				bytes_to_send = f.read(filesize)
				s.send(bytes_to_send)
				while bytes_to_send != '':
					bytes_to_send = f.read(filesize)
					s.send(bytes_to_send)
	else:
		s.send('ERROR')


def chat_handler(name, s):
	flag = True
	while flag:
		message = s.recv(1024)
		user, message = message.split('@#$@')
		if message == 'exit':
			flag = False
		elif message[:5] == 'file ':
			file_handler('rt', s, message.split(' ')[1])
		elif message == '':
			exit()
		else:
			print('{}>> {}'.format(user, message))
			# print('Message "{}" received from {}.'.format(message, s.getpeername()))



def main():
	s = socket.socket()
	s.bind((host, port))
	s.listen(5)
	print('Server Start Listening !!!')
	try:
		while True:
			conn, addr = s.accept()
			print('Client connected of ip <{}>'.format(addr))
			
			file_chat = conn.recv(1024)
	
			if file_chat == 'F':
				t1 = threading.Thread(target=file_handler, args=('rt', conn))
				t1.start()
			else:
				t2 = threading.Thread(target=chat_handler, args=('rt', conn))
				t2.start()
	
	except KeyboardInterrupt:
		s.close()


if __name__ == '__main__':
	main()
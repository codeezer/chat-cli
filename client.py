#!/usr/bin/env python

import socket
import sys

host = '127.0.0.1'
port = int(sys.argv[1])
user = sys.argv[2]

def file_handler(s, filename=''):
	if filename == '':
		flag = 1
		filename = raw_input('Press "q" to quit \nEnter Filename: ')
	else:
		flag = 0

	if filename != 'q':
		if flag == 1:
			s.send(filename)
		data = s.recv(1024)
		if data[:6] == 'EXISTS':
			filesize = long(data[6:])
			message = raw_input('File Exists, {} Bytes \
				\nDo You Want to Download (Y/N)?: '.format(filesize))
			if message == 'Y':
				s.send('OK')
				f = open('new_{}'.format(filename), 'wb')
				data = s.recv(filesize)
				total_receive = len(data)
				f.write(data)
				print('{} Bytes of data has been received.'.format(total_receive))
			else:
				pass
		else:
			print('File {} not found in server.'.format(filename))


def chat_handler(s):
	flag = True
	while flag:
		message = raw_input('{}>> '.format(user))
		s.send('{}@#$@{}'.format(user, message))
		if message == 'exit':
			print('Bye...')
			flag = False
		
		elif message[:5] == 'file ':
			file, filename = message.split(' ')
			file_handler(s, filename)


def main():
	s = socket.socket()
	s.connect((host, port))
	
	chat_file = raw_input('Chat or File (C/F): ')
	s.send(chat_file)

	if chat_file == 'F':
		file_handler(s)

	elif chat_file == 'C':
		chat_handler(s)
	
	else:
		print('No service available...')
		exit()


if __name__ == '__main__':
	main()
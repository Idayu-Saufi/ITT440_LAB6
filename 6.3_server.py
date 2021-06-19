import socket
import sys
import time
import errno
import math
from multiprocessing import Process

ok_message = '\nHTTP/1.0 200 OK\n\n'
nok_message = '\nHTTP/1.0 404 NotFound\n\n'

def process_start(s_sock):
	s_sock.send(str.encode("**************Online Calculator using Python*************** \n Function : LOG, SQUARE ROOT, EXPONENTIAL \n How to use: log/sqrt/exp <number>\n Example: log 20\n\tType 'exit' to close\n-----------------------------------------------------------"))

	while True:
		data = s_sock.recv(2048)
		data = data.decode('utf-8')
		print(data)

		try:
			operation, value = data.split()
			op = str(operation)
			num = int(value)

			if op[0] == 'l':
				op = 'Log'
				answer = math.log10(num)
			elif op[0] == 's':
				op = 'Square root'
				answer = math.sqrt(num)
			elif op[0] == 'e':
				op = 'Exponential'
				answer = math.exp(num)
			else:
				answer = ('Error!')

			Reply = (str(op) + '(' + str(num) + ') = ' + str(answer))
			print ('Calculation is Done!!!')
		except:
			print ('Invalid input')
			Reply = ('Invalid input')

		if not data:
			break

		s_sock.send(str.encode(Reply))

	s_sock.close()

if __name__ == '__main__':
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(("",8888))
	print("Listening...")
	s.listen(5)

	try:
		while True:
			try:
				s_sock, s_addr = s.accept()
				p = Process(target=process_start, args=(s_sock,))
				p.start()

			except socket.error:

				print('socket error')

			except Exception as e:
				print("Exception Occured!!")
				print(e)
				sys.exit(1)
	finally:
		s.close()

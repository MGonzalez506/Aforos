import os
import sys
import csv
import time

import threading
import mysql.connector
from mysql.connector import errorcode
from time import sleep
from datetime import datetime, timedelta




start = time.perf_counter()

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
output_file_addr = str(THIS_FOLDER + ("/Resultado.csv"))

try:
	cnx = mysql.connector.connect(user='Username',
								password='Password',
								host='Localhost',
								database='DatabaseName')
except mysql.connector.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print("El usuario o contraseña no son correctos")
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print("La base de datos no existe")
	else:
		print(err)
else:
	cursor = cnx.cursor()
	beggining = datetime.now() - timedelta(hours=24)
	end = datetime.now()
	print(f'Beggining time: {beggining}, finish time: {end}')
	add_event = "SELECT * FROM historial_aforos WHERE timestamp BETWEEN '" + str(beggining) + "' AND '" + str(end) + "'"
	cursor.execute(add_event)
	result = cursor.fetchall()
	cnx.commit()
	cursor.close()
	cnx.close()
	cont = 0
	with open(output_file_addr, 'w', newline='') as f:
		thewriter = csv.writer(f)
		for x in result:
			cont+=1
			thewriter.writerow(x)

finish = time.perf_counter()

print(f'Finish document in {round(finish-start, 2)} seconds and {cont} entries...')

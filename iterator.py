#!/usr/bin/python3

import gspread
from oauth2client.service_account import ServiceAccountCredentials
# import mysql.connector
import os
import main
import time
import subprocess

scope = ['https://spreadsheets.google.com/feeds' + ' ' +'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open("LIDRE").sheet1
list_of_hashes = sheet.get_all_records()

# connection=mysql.connector.connect(host='localhost',database='users',user='mukul',password='mukul')
# cursor=connection.cursor()

# sql_query= "INSERT IGNORE INTO users (ROLL,NAME,EMAIL) VALUES (%(Roll Number)s,%(Name)s, %(Email)s)"
# cursor.executemany(sql_query,list_of_hashes)
# connection.commit()

# cursor.execute('SELECT * FROM users')
os.environ['SENDGRID_API_KEY']='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'
subprocess.run('./api_key.sh')

for row in list_of_hashes:
	print("Starting for {}".format(row['Roll Number']))
	try:
		main.date_check(row['Roll Number'],row['Email'])
	except Exception as e:
		print("An error occured! Skipping this person")
		print(e)
		pass
	print("Process completed for {}".format(row['Roll Number']))
	time.sleep(1)



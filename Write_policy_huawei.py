#!/usr/bin/python3

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sys

reload(sys)
sys.setdefaultencoding('utf8')


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a spreadsheet.
SPREADSHEET_ID = '1q6j10Q8CHmH7bLRvdg0EmckFsiSK-he7IHSWcI97zFC'
RANGE_NAME = 'BGP!A2:F'

def main():
	creds = None
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				'credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	service = build('sheets', 'v4', credentials=creds)

	# Call the Sheets API
	sheet = service.spreadsheets()
	result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
	values = result.get('values', [])

	if not values:
		print('No data found.')
	else:

	# EMPRESA
	# ASN
	# Prefixos IPv4
	# Prefixos IPv6
	# PREFIX-LIST
	# ASPATH

		# Create new file
		file = open("Prefix_List.txt","w+")
		for row in values:
			# Criando os campos da planilha
			EMPRESA  = row[0]
			ASN      = row[1]
			PREFV4   = row[2].split(';')
			PREFV6   = row[3].split(';')
			PREFLIST = row[4]
			ASPATH   = row[5]
			
			# Separando os prefixos por ; e verificando se nao estao em branco
			for PREFV4 in PREFV4:
				if PREFV4 != '':
					PREFV4 = PREFV4.split('/')
					file.write('ip ip-prefix PREFIXv4_AS%s-IN permit %s %s greater-equal %s less-equal 24\n' % (ASN, PREFV4[0], PREFV4[1], PREFV4[1]))
					
			for PREFV6 in PREFV6:
				if PREFV6 != '':
					PREFV6 = PREFV6.split('/')
					file.write('ip ip-prefix PREFIXv6_AS%s-IN permit %s %s greater-equal %s less-equal 48\n' % (ASN, PREFV6[0], PREFV6[1], PREFV6[1]))
			
		
		EMPRESA  = row[0]
		ASN      = row[1]
		PREFV4   = row[2].split(';')
		PREFV6   = row[3].split(';')
		PREFLIST = row[4]
		ASPATH   = row[5]
			
		file = open("Prefix_List.txt","a+")
		for row in values:
			ASN   = ASPATH.split(' ')
			AS = ''
			ASPATH = '^'
			for ASN in ASN:
				AS += '(_'+ASN+')+'
				ASPATH = ASPATH+AS+'$'
				print ('ip as-path-filter ASPATH_AS%s_IN permit %s' % (ASN, ASPATH))
				#file.write('ip as-path-filter ASPATH_AS%s_IN permit %s' % (ASN, ASPATH))
			
			
	file.close()		

if __name__ == '__main__':
	main()

#!/usr/bin/env python3
import csv
import sys
import os
import getopt
import requests

def main(argv):
	print('Requires python-requests. Install with "pip install requests"')
	# get args
	inputfile = ''
	outputfile = ''
	helpstring = 'webfruit.py -i <inputfile.csv> -o <outputfile.csv>\nInput file required\nOutput file optional and defaults to output.csv'
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["infile=","outfile="])
	except getopt.GetoptError:
		print(helpstring)
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print(helpstring)
			sys.exit()
		elif opt in ("-i", "--infile"):
			inputfile = arg
		elif opt in ("-o", "--outfile"):
			outputfile = arg
	if not inputfile.strip():
		print(helpstring)
		sys.exit(2)
	if not outputfile.strip():
		outputfile = 'output.csv'
		
	print('Working... ', end='\r')
	
	# open input file and load into variable
	with open(inputfile, 'r') as f:
		reader = csv.reader(f)
		url_list = list(reader)
	
	# open output file for writing
	outfile = open(outputfile, 'w', encoding='utf-8')
	
	# scan each url
	counter = 0
	total = len(url_list)
	for url in url_list:
		# Nikto 003496
		try:
			r = requests.get(url[0]+'/status?full=true', verify=False, timeout=6.1)
			if 'Tomcat Status' in r.text: 
				outbuf = url[0]+',/status?full=true\n'
				outfile.write(outbuf)
		except:
			pass

		# Nikto 000165
		try:
			r = requests.get(url[0]+'/web-console/ServerInfo.jsp%00', verify=False, timeout=6.1)
			if '<\%=' in r.text: 
				outbuf = url[0]+',/web-console/ServerInfo.jsp%00\n'
				outfile.write(outbuf)
		except:
			pass

		# Nikto 003263
		try:
			r = requests.get(url[0]+'/isapi/tstisapi.dll', verify=False, timeout=6.1)
			if 'Pi3web' in r.text: 
				outbuf = url[0]+',/isapi/tstisapi.dll\n'
				outfile.write(outbuf)
		except:
			pass
		
		counter += 1
		print('Working... ' + str(counter) + ' / ' + str(total) + ' URLs done!', end='\r')
	# done
	print('\nDone! Requested ' + str(counter) + ' URLs!')

if __name__ == "__main__":
	main(sys.argv[1:])

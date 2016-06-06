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
	helpstring = 'geolocate.py -i <inputfile.csv> -o <outputfile.csv>\nInput file required\nOutput file optional and defaults to output.csv'
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
		ip_list = list(reader)
	
	# open output file for writing
	outfile = open(outputfile, 'w', encoding='utf-8')
	
	# scan each ip/port combo
	counter = 0
	total = len(ip_list)
	for combo in ip_list:
		r = requests.get('http://199.116.235.115:8080/csv/' + combo[0])
		if r.status_code is not 200:
			print('It looks like the daily limit of 10000 is exceeded. Exiting...')
			print('\nDone! Located ' + str(counter) + ' IPs!')
			sys.exit(1)
		outbuf = r.text.strip() + '\n'
		outfile.write(outbuf)
		counter += 1
		print('Working... ' + str(counter) + ' / ' + str(total) + ' IPs located!', end='\r')
	# done
	print('\nDone! Located ' + str(counter) + ' IPs!')

if __name__ == "__main__":
	main(sys.argv[1:])

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
	helpstring = 'statuscodes.py -i <inputfile.csv> -o <outputfile.csv>\nInput file required\nOutput file optional and defaults to output.csv'
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
		try:
			r = requests.get(url[0], verify=False, timeout=6.1)
			outbuf = url[0]+','+str(r.status_code) + '\n'
		except:
			outbuf = url[0]+',0\n'
		outfile.write(outbuf)
		counter += 1
		print('Working... ' + str(counter) + ' / ' + str(total) + ' URLs done!', end='\r')
	# done
	print('\nDone! Requested ' + str(counter) + ' URLs!')

if __name__ == "__main__":
	main(sys.argv[1:])

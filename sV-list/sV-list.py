#!/usr/bin/env python3
import csv
import sys
import os
import nmap
import getopt

def main(argv):
	# get args
	inputfile = ''
	outputfile = ''
	helpstring = 'sV-list.py -i <inputfile.csv> -o <outputfile.csv>\nInput file required\nOutput file optional and defaults to output.csv'
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
	
	# load nmap module
	try:
		nm = nmap.PortScanner()
	except nmap.PortScannerError:
		print('Nmap not found', sys.exc_info()[0])
		sys.exit(1)
	except:
		print('Unexpected error:', sys.exc_info()[0])
		sys.exit(1)
	
	# open input file and load into variable
	with open(inputfile, 'r') as f:
		reader = csv.reader(f)
		toscan_list = list(reader)
	
	# open output file for writing
	outfile = open(outputfile, 'w')
	
	# scan each ip/port combo
	counter = 0
	for combo in toscan_list:
		nm = nmap.PortScanner()
		nm.scan(hosts=combo[0], arguments='-sV -Pn -p ' + combo[1])
		svcname = nm[combo[0]]['tcp'][int(combo[1])]['name']
		if not svcname:
			svcname = 'N/A'
		nmop = '"' + combo[0] + '","' + combo[1] + '","tcp","' + nm[combo[0]]['tcp'][int(combo[1])]['state'] + '","' + svcname + '"\n'
		outfile.write(nmop)
		print('.',end="",flush=True)
		counter += 1
	# done
	print('\nDone! Scanned ' + str(counter) + ' ip/port combos!')

if __name__ == "__main__":
	main(sys.argv[1:])

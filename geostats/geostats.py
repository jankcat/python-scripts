#!/usr/bin/env python3
import csv
import sys
import os
import getopt

def main(argv):
	# get args
	inputfile = ''
	outputfile = ''
	helpstring = 'geostats.py -i <inputfile.csv> -o <output_prefix>\nInput file required\nOutput prefix optional and defaults to output'
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
		outputfile = 'output'

	print('Working... ', end='\r')
	
	# open input file and load into variable
	with open(inputfile, 'r', encoding='utf-8') as f:
		reader = csv.reader(f)
		csv_list = list(reader)
	# Input File:
	# csv_line[0]	csv_line[1]		csv_line[2]		csv_line[3]
	# Source IP, 	Dest IP, 		Dest Port, 		Source IP Country

	# open output file for writing
	outfile_c = open(outputfile+'_countries.csv', 'w', encoding='utf-8')
	outfile_p = open(outputfile+'_ports.csv', 'w', encoding='utf-8')

	# keep a counter so the user is not worried it hung
	counter = 0
	total = len(csv_list)
	countries = {}
	ports = {}

	for csv_line in csv_list:
		counter += 1
		if csv_line[3] in countries:
			countries[csv_line[3]]['count'] += 1
			if csv_line[2] in countries[csv_line[3]]['ports']: 
				countries[csv_line[3]]['ports'][csv_line[2]] += 1
			else:
				countries[csv_line[3]]['ports'][csv_line[2]] = 1
		else:
			countries[csv_line[3]] = {'count': 1, 'name': csv_line[3], 'ports': {csv_line[2]: 1}}

		if csv_line[2] in ports:
			ports[csv_line[2]] += 1
		else:
			ports[csv_line[2]] = 1
		print('Working... ' + str(counter) + ' / ' + str(total) + ' rows parsed!', end='\r')
	print('\nDone parsing! Parsed ' + str(counter) + ' rows!')

	# get countries and thier top 5 ports
	print('Sorting countries...')
	topCountries = sorted(countries, key=lambda x: (countries[x]['count'], countries[x]['name']), reverse = True)
	for country in topCountries: 
		outbuf = '"'+country.strip()+'","'+ str(countries[country]['count'])+'"'
		topPortsForCountry = sorted(countries[country]['ports'], key=lambda x: (countries[country]['ports'][x]), reverse = True)
		for port in topPortsForCountry[:5]:
			outbuf += ',"'+port+'","'+str(countries[country]['ports'][port])+'"'
		outbuf += '\n'
		outfile_c.write(outbuf)

	print('Sorting ports...')
	topPorts = sorted(ports, key=ports.get, reverse = True)
	for port in topPorts:
		outbuf = '"'+port+'","'+ str(ports[port])+'"\n'
		outfile_p.write(outbuf)

	print('Done!')

if __name__ == "__main__":
	main(sys.argv[1:])

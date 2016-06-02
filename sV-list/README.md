# ./sV-list.py
This script takes a list of IP Address/TCP Port combinations from a CSV file, runs them through nmap with -sV and -Pn arguments, and outputs the results to a CSV file.

## Requirements
* python-nmap is required, and instructions can be found here: http://xael.org/pages/python-nmap-en.html
* Python 3 is required, it has not been tested on Python 2.

## Execution
* `sV-list.py -i <inputfile.csv> -o <outputfile.csv>`
* Input file required
* Output file optional and defaults to output.csv

## Input format
The input file should be a csv file, formatted as such: IPAddr,TCPPort
````
127.0.0.1,3389
127.0.0.1,25
127.0.0.2,445
127.0.0.3,8443
````
Please only include one IP and one Port per line, as that is all this script is designed to support... unless you feel like sending a pull request my way...

## Output File
The output file will look similar to the below file:
````
"127.0.0.1","3389","tcp","filtered","N/A"
"127.0.0.1","25","tcp","open","smtp"
"127.0.0.2","445","tcp","closed","N/A"
"127.0.0.3","8443","tcp","closed","N/A"
````

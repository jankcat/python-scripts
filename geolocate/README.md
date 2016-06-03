# ./geolocate.py
This script takes a list of IP Addresses from a CSV file, runs them through a geolocater, and outputs the results to a CSV file.

## Requirements
* python-requests is required, and instructions can be found here: http://docs.python-requests.org/en/latest/user/install/#install
* Python 3 is required, it has not been tested on Python 2.

## Execution
* `geolocate.py -i <inputfile.csv> -o <outputfile.csv>`
* Input file required
* Output file optional and defaults to output.csv

## Input format
The input file should be a csv file or text file, formatted as such: IPAddr
````
127.0.0.1
127.0.0.1
127.0.0.2
127.0.0.3
````
Please only include one IP per line.

## Output File
The output file will look similar to the below file:
````
8.8.8.8,US,United States,CA,California,Mountain View,94035,America/Los_Angeles,37.39,-122.08,807
8.8.4.4,US,United States,,,,,,37.75,-97.82,0
12.23.34.45,US,United States,LA,Louisiana,Metairie,70001,America/Chicago,29.98,-90.17,622
````

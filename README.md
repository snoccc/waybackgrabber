# waybackgrabber

A Python tool that lets you access The Wayback Machine in a terminal and creates a webpage to quickly search through the results.

# Setup
1. Navigate to the Python directory.

To install the required packages, run
```
pip3 install -r requirements.txt
```
### Usage
```
python3 waybackgrabber.py -t TARGET [-l LIMIT]
```
### Examples
```
python3 waybackgrabber.py -t example.com
python3 waybackgrabber.py -t example.com -l 10000
```
You can limit the amount of results by adding `-l <RESULTS>`

# Results
Results are stored in a folder called `./Grabs/<target>/`, in there you will find the webpage and a json file containing the results.

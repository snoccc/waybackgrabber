# waybackgrabber

A Python tool that lets you access The Wayback Machine in a terminal and creates a webpage to quickly search through the results.

# Setup
First, navigate to the Python directory.

To install the required packages, run
```
pip3 install -r requirements.txt
```
### Usage
```
python3 waybackgrabber.py [-h] -t TARGET [-l LIMIT]
```
### Examples
```
python3 waybackgrabber.py -t example.com
python3 waybackgrabber.py -t example.com -l 10000
```
You can limit the amount of results by adding `-l <RESULTS>`

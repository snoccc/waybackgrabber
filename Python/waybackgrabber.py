import validators
import webbrowser
import argparse
import requests
import pandas
import sys
import json
import os
import time

def getUrls():
	# get every url except "original", the column name
	for row in jsonObject:
		if str(row[0]) != 'original':
			print(row[0])

def getTimespan():
	timespan = f"{str(jsonObject[1][2])[0:4]} - {str(jsonObject[1][3])[0:4]}"
	return timespan

def makeDirectory(dirName):
	try:
		os.makedirs(f'../Grabs/{dirName}', exist_ok=True)
	except OSError:
		print (f'Error: Creation of the directory {dirName} failed')

robotlist = []
def getRobots():
	# grab data for <target>/robots.txt urls with statuscode 200
	url = f'https://web.archive.org/cdx/search/cdx\
		?url={args.target}/robots.txt&output=json&fl=timestamp,original&filter=statuscode:200&collapse=digest'

	response = requests.get(url)
	results = response.json()

	# store all snapshot IDs in a list
	for row in results:
		if row != None:
			robotlist.append(row[0])

# every js file goes in a set to get rid of duplicates
jsFiles = set()
def getJavascript():
	valid = ['application/javascript', 'application/x-javascript']

	# get everything before the '.js', we don't want parameters
	for row in jsonObject:
		if any(i in row[1] for i in valid):
			jsFiles.add(str(row[0].split('.js')[0]) + '.js')


def df_html():
	getRobots()
	getJavascript()

	# javascript
	df2 = pandas.DataFrame(jsFiles, columns =['url'])
	df2.index = df2.index + 1

	# robots
	df3 = pandas.DataFrame(robotlist, columns =['snapshot'])
	df3 = df3[df3.snapshot != 'timestamp']
	
	# make the urls clickable in each dataframe
	df['url'] = '<span id="pos"><a href=https://web.archive.org/web/*/' + df['url'] +' target="_blank">' + df['url'] + '</a></span>'
	df2['url'] = '<span id="pos"><a href=https://web.archive.org/web/*/' + df2['url'] + ' target="_blank">' + df2['url'] + '</a></span>'
	df3['snapshot'] = '<span id="pos"><a href=https://web.archive.org/web/' + df3['snapshot'] + '/' + 'http://' + args.target + '/robots.txt' + ' target="_blank">' + df3['snapshot'] + '</a></span>'

	del df['from']
	del df['to']

	# HTML page content
	base_html = """
	<!DOCTYPE html>
	<html>
		<head>
			<meta http-equiv="Content-type" content="text/html; charset=utf-8">
			<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.2/jquery.min.js"></script>
			<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.16/css/jquery.dataTables.css">
			<script type="text/javascript" src="https://cdn.datatables.net/1.10.16/js/jquery.dataTables.js"></script>
			<link rel="stylesheet" type="text/css" href="../../style/stylesheet.css">
		</head>
		<body>
			<div id="wrapper">
				<ul>
					<li> <a href="#" onclick="showAll()">All</a> </li>
					<li> <a href="#" onclick="switchToJS()">JavaScript</a> </li>
					<li> <a href="#" onclick="switchToRobots()">robots.txt</a> </li>
				</ul>
				<div id="spinner"></div>
				<div id="all">
					%s
				</div>
				<div id="js">
					%s
				</div>
				<div id="robots">
					%s
				</div>
			</div>
			<script type="text/javascript">
				$(document).ready(function(){
					$('table').DataTable({
						"pageLength": 50
					});
					$('table').show();
					$('#spinner').hide();
					$('#js').hide();
					$('#robots').hide();
				});
				function showAll() {
					$('#js').hide();
					$('#robots').hide();
					$('#all').show();
				}
				function switchToJS() {
					$('#all').hide();
					$('#robots').hide();
					$('#js').show();
				}
				function switchToRobots() {
					$('#js').hide();
					$('#all').hide();
					$('#robots').show();
				}
			</script> 
		</body>
	</html>
	"""

	dfAll = df.to_html(escape=False).replace('border="1"','border="0"')
	dfJS = df2.to_html(escape=False).replace('border="1"','border="0"')
	dfRobots = df3.to_html(escape=False).replace('border="1"','border="0"')

	return base_html % (dfAll, dfJS, dfRobots)

if __name__ == '__main__':
	is_windows = sys.platform.startswith('win')
	if is_windows:
		G = '\033[92m'  # green
		Y = '\033[93m'  # yellow
		B = '\033[36m'  # blue
		R = '\033[91m'  # red
		W = '\033[0m'   # white
		try:
			import colorama
			colorama.init()
		except:
			print('Error: Coloring libraries not installed')
			G = Y = B = R = W = G = Y = B = R = W = ''
	else:
		G = '\033[92m'  # green
		Y = '\033[93m'  # yellow
		B = '\033[94m'  # blue
		R = '\033[91m'  # red
		W = '\033[0m'   # white

	parser = argparse.ArgumentParser()

	# add target (-t) flag
	parser.add_argument('-t', action='store', dest='target', help='Target', required=True)

	# add limit (-l) flag
	parser.add_argument('-l', action='store', dest='limit', type=int, default=0,help='Limit')

	args = parser.parse_args()

	if validators.domain(args.target):
		pass
	else:
		print(f'{R}Error: please enter valid target!\n{Y}Example: example.com{W}')
		sys.exit()

	print(f"""{G}
                      _                _                   _     _               
                     | |              | |                 | |   | |              
 __      ____ _ _   _| |__   __ _  ___| | ____ _ _ __ __ _| |__ | |__   ___ _ __ 
 \ \ /\ / / _` | | | | '_ \ / _` |/ __| |/ / _` | '__/ _` | '_ \| '_ \ / _ \ '__|
  \ V  V / (_| | |_| | |_) | (_| | (__|   < (_| | | | (_| | |_) | |_) |  __/ |   
   \_/\_/ \__,_|\__, |_.__/ \__,_|\___|_|\_\__, |_|  \__,_|_.__/|_.__/ \___|_|   {W}v1.0{G}
                 __/ |                      __/ |                                
                |___/                      |___/                                  
	{W}""")

	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
	mainUrl = f'https://web.archive.org/cdx/search?url={args.target}%2F&matchType=prefix&collapse=urlkey&output=json&fl=original%2Cmimetype%2Ctimestamp%2Cendtimestamp%2Cgroupcount%2Cuniqcount'

	# if limit specified, add limit to url
	if args.limit != 0:
		mainUrl += f'&limit={args.limit}'

	response = requests.get(mainUrl,headers=headers)
	jsonObject = json.loads(response.text)

	# standard directory name for targets
	dirName = args.target

	makeDirectory(dirName)

	# save snapshots to json file
	with open(f'../Grabs/{dirName}/snapshots.json', 'w', encoding='utf-8') as f:
		json.dump(jsonObject, f, ensure_ascii=False, indent=4)

	df = pandas.read_json(path_or_buf=f'../Grabs/{dirName}/snapshots.json', orient='records')

	# rename the colums
	new_header = df.iloc[0]
	df = df[1:]
	df.columns = ['url', 'mimetype', 'from', 'to', 'groupcount', 'uniqcount']

	with open(f'../Grabs/{dirName}/snapshots.html', 'w', encoding='utf-8') as f:
		f.write(df_html())

	print((
	f'{G}==============================================================================================\n\n'
	f'{Y} Host:{W} {args.target}\n'
	f'{Y} Results:{W} {len(df.index)}\n'
	f'{Y} Timespan:{W} {getTimespan()}\n'
	f'{Y} JavaScript files:{W} {len(jsFiles)}\n\n'
	f'{G}==============================================================================================\n\n'
	f'{Y}[+] {G}The results are saved in {Y}../Grabs/{dirName}/{G}.{W}'))

	print(f'{Y}[+] {G}Would you like to open the web interface? [y/n]{W} ')

	inp = input()

	if inp.lower() == 'y':
		print(f"{B}Note: consider adding a limit with '-l' if the page won't load{W}")
		webbrowser.open(os.path.realpath(f.name))

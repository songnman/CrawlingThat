# from dc_inside import extract_dc_contents
from datetime import datetime, timezone
from flask import Flask, render_template, request, redirect, send_file
from arca import extract_arca_list, extract_arca_single, email_alert
from save import save_to_file
from threading import Thread
import time, os.path

app = Flask("WebScrapper")

db = {}

@app.route("/")
def home():
	return render_template("Search.html")

@app.route("/repeat")
def repeat():
	# word = request.args.get('word')
	interval = request.args.get('interval', type=int)

	t = Thread(target=threaded, args=[interval])
	t.daemon = True
	t.start()
	return render_template("Search.html", repeat_interval=interval)

def threaded(interval):
	
	#*[2021-08-29 22:00:03] 서치리스트 생성
	search_List = []
	list_file = "Search_List.csv"
	if os.path.exists(list_file):
		import csv
		with open(list_file,'r', encoding='utf-8-sig', newline='') as csvfile:
			rdr = csv.reader(csvfile)
			for line in rdr:
				search_List.append(line[0])

	global is_end; is_end = False
	count = 0

	while True:
		if is_end: break
		#*[2021-08-29 22:00:03] 서치리스트를 통해서 서칭
		print(f"Searching List: {search_List}")
		for search in search_List:
			if is_end: break
			extract_arca_list(1, 2, search)
			time.sleep(5)
			pass
		count += 1
		print(f'[{count}]Times Repeated.')
		if(count%10 == 0) : email_alert(f"{count}Times Scrap Repeated.","", "songnman@gmail.com" )
		spend_minute(interval)
	print("Stoped!")

def spend_minute(interval):
	for i in range(1, interval * 60):
		if is_end: break
		time.sleep(1)

@app.route("/stop_repeat")
def stop_repeat():
	global is_end; is_end = True
	return render_template("Search.html")

@app.route("/report")
def report():
	word = request.args.get('word')
	start = request.args.get('start', type=int)
	pages = request.args.get('pages', type=int)
	contents = extract_arca_list(start, pages, word)
	# save_to_file(contents,word) #필요없나?
	# db[word] = contents
	return render_template(
		"Search.html",
		searchingBy=word,
		resultNumber=len(contents),
		contents=contents)
		
@app.route("/report_single")
def report_single():
	index = request.args.get('index')
	contents = extract_arca_single(index)
	# db[word] = contents
	return render_template(
		"Result.html",
		searchingBy=None,
		resultNumber=1,
		contents=contents)

@app.route("/export")
def export():
	try:
		word = request.args.get('word')
		if not word:
			raise Exception()
		contents = db.get(word)
		if not contents:
			raise Exception()
		save_to_file(contents,word)
		return send_file(
			"contents.csv",
			mimetype='text/csv',
			attachment_filename= f'result_{datetime.now(timezone.utc)}{word}.csv',
			as_attachment=True)

	except:
		return redirect("/")

# Temp 페이지 생성
# @app.route("/<username>")
# def contact(username):
#	 return f"this is {username}"

app.run("0.0.0.0")
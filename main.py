# from dc_inside import extract_dc_contents
from datetime import datetime, timezone
from flask import Flask, render_template, request, redirect, send_file
from arca import extract_arca_list
from save import save_to_file
from threading import Thread
import time

app = Flask("WebScrapper")

db = {}

@app.route("/")
def home():
    return render_template("Search.html")

@app.route("/repeat")
def repeat():
    word = request.args.get('word')
    interval = request.args.get('interval', type=int)

    t = Thread(target=threaded, args=(interval,word))
    t.daemon = True
    t.start()
    return render_template("Repeat.html", repeat_interval=interval)

def threaded(interval,word):
    global is_end
    is_end = False
    count = 0
    while True:
        if is_end == True:
            print("Stoped!")
            break
        else:
            contents = extract_arca_list(1, 1, word)
            save_to_file(contents,word)
            count += 1
            print(f'[{count}]Times Repeated.')
            for i in range(1, interval * 60):
                if is_end == True:
                    break
                else :
                    time.sleep(1)

@app.route("/stop_repeat")
def stop_repeat():
    global is_end
    is_end = True
    return render_template("Repeat.html")

@app.route("/report")
def report():
    word = request.args.get('word')
    start = request.args.get('start', type=int)
    pages = request.args.get('pages', type=int)
    contents = extract_arca_list(start, pages, word)
    save_to_file(contents,word) #필요없나?
    # db[word] = contents
    return render_template(
        "Result.html",
        searchingBy=word,
        resultNumber=len(contents),
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
#     return f"this is {username}"

app.run("0.0.0.0")
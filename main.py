from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
from exporter import save_to_file
# template 불러오기 위해서 이거 import해야함

app = Flask("FirstScrapper")

db = {} # 가짜db

# repl.it에서 공개하는 웹사이트가 만들어짐
@app.route("/")
def home():
  return render_template("potato.html")

@app.route("/report")
def report():
  word = request.args.get('word') # 검색단어를 받기
  # report?args=21&args=33 이런식으로 전달되는게 argument
  if word: # 검색단어가 있으면 
    word = word.lower() # 대문자로 쓸수도있으니 소문자로 바꿔주기
    existingjobs = db.get(word)
    if existingjobs: #db에 검색단어가 있으면
      jobs = existingjobs
    else:
      jobs = get_jobs(word)
      db[word] = jobs
  else: # 검색단어가 없을 경우
    return redirect("/") #home으로 보내주기
  return render_template(
    "report.html", 
    searchingBy=word,
    resultsNumber=len(jobs),
    jobs=jobs
  )
  #이런식으로 써주면 html file에서 값을 가져올수있음


# 결과를 csv로 다운받는 function
@app.route("/export")
def export():
  try:
    word = request.args.get('word')
    if not word: #만약에 word가 존재하지않으면
      raise Exception() #다시홈화면으로
    word = word.lower()
    jobs = db.get(word)
    if not jobs:        #fake DB에 word가 데이터없으면
      raise Exception() #다시홈화면으로
    save_to_file(jobs)
    return send_file("jobs.csv", mimetype='application/x-csv', attachment_filename="jobs.csv", as_attachment=True) 
  except:
    return redirect("/")




######################################################
@app.route("/contact")
# 위에 이거를 decorator라고 부르고 route으ㅣ경로로 들어갔을때 아래의 function을 실행해줌 (변수 ㄴㄴ)) 
def potato():
  return "Contact Me"


# dynamic urls 사용
@app.route("/<username>")
def tomato(username):
  return f"Hello your name is {username}"
######################################################
app.run(host="0.0.0.0")
#repl에서 작업해서 0.0.0.0 넣어준것

from flask import Flask, redirect, render_template, url_for, request
from DB_handler import DBmodule

app = Flask(__name__)
DB=DBmodule()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/list")         #게시글 목록
def post_list():
    pass

@app.route("/post/<int:pid>")         #목록 내의 각 포스트의 세부내용
def post(pid):
    pass

@app.route("/write")            #게시글 작성
def write():
    pass

@app.route("/write_done", methods = ["GET"])    #작성한 게시글을 get으로 받고 입력완료 페이지
def write_done():
    pass 

@app.route("/login")           #로그인
def login():
    pass

@app.route("/login_done")      #실제로 보이는 부분x
def login_done():
    pass

@app.route("/signin")          #회원가입
def signin():
    return render_template("signin.html")

@app.route("/signin_done", methods = ["get"])   #실제로 보이는 부분x      
def signin_done():
    email = request.args.get("email")
    name = request.args.get("name")
    uid = request.args.get("id")
    pwd = request.args.get("pwd")
    if DB.signin(uid,pwd,email,name):
        return redirect(url_for("index"))
    else:
        return redirect(url_for("signin"))
@app.route("/user/<uid>")       #각 회원의 개인정보
def user(uid):
    pass

if __name__ == "__main__":
    app.run(host = "0.0.0.0" , debug = True)
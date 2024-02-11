from flask import Flask, redirect, render_template, url_for, request, flash, session
from DB_handler import DBmodule
import uuid
import face_model

app = Flask(__name__)
app.secret_key = "dasggasdgasd"
DB=DBmodule()

@app.route("/")
def index():
    if "uid" in session:
        user = session["uid"]
    else:
        user = "login"
    return render_template("index.html", user = user)

@app.route("/list")         #게시글 목록
def post_list():
    post_list = DB.post_list()
    if post_list == None:
        length = 0
    else:
        length = len(post_list)
    return render_template("post_list.html", post_list = post_list.items(), length = length)

@app.route("/post/<string:pid>")         #목록 내의 각 포스트의 세부내용
def post(pid):
    post = DB.post_detail(pid)
    photourl = DB.get_photo_url(post["photo"],session["uid"])
    return render_template("post_detail.html", post = post, photourl = photourl)

@app.route("/write")            #게시글 작성
def write():
    if "uid" in session:
        return render_template("write_post.html")
    else:
        return redirect(url_for("login")) 

@app.route("/write_done", methods = ["get"])    #작성한 게시글을 get으로 받고 입력완료 페이지
def write_done():
    title = request.args.get("title")
    contents = request.args.get("contents")
    uid = session.get("uid")
    DB.write_post(title, contents, uid)
    return render_template("applyphoto.html")

@app.route("/photoupload_done", methods = ["post"])    #작성한 게시글을 get으로 받고 입력완료 페이지
def photoupload_done():
    f = request.files["file"]
    uid = session.get("uid")
    photoid = str(uuid.uuid4())[:12]
    f.save("static/img/{}.jpeg".format(photoid))
    Dimage = face_model.detect_face("static/img/{}.jpeg".format(photoid))
    if Dimage == None:
        DB.upload_photo("static/img/{}.jpeg".format(photoid),uid)
        return render_template("viewphoto.html", uid = uid, img="img/{}.jpeg".format(photoid), detect = False)
    else: 
        DB.upload_photo("static/img/{}.jpeg".format(Dimage),uid)
        return render_template("viewphoto.html", uid = uid, img="img/{}.jpeg".format(Dimage), detect = True)

@app.route("/login")           #로그인
def login():
    if "uid" in session:
        return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/logout")           #로그인
def logout():
    if "uid" in session:
        session.pop("uid")
        return redirect(url_for("index"))
    else:
        return redirect(url_for("login"))

@app.route("/login_done", methods = ["GET"])      #실제로 보이는 부분x
def login_done():
    uid = request.args.get("id")
    pwd = request.args.get("pwd")
    if DB.login(uid,pwd):
        session["uid"] = uid
        return redirect(url_for("index"))
    else:
        flash("아이디가 없거나 비밀번호가 틀립니다")
        return redirect(url_for("login"))

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
        flash("이미 존재하는 아이디입니다.")
        return redirect(url_for("signin"))
    
@app.route("/users_post/<string:uid>")       
def users_post(uid):
    u_post = DB.get_user(uid)
    if u_post == None:
        length = 0
    else:
        length = len(u_post)
    return render_template("user_detail.html", post_list = u_post, length = length, uid = uid)

if __name__ == "__main__":
    app.run(host = "0.0.0.0" , debug = True)
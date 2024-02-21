from flask import Flask, redirect, render_template, url_for, request, flash, session, jsonify
from DB_handler import DBmodule
import uuid
import face_model
import datetime

app = Flask(__name__)
app.secret_key = "dasggasdgasd"
DB=DBmodule()

@app.route("/")                     #홈화면 버튼에 대한 처리(로그인o : 업로드 화면, 로그인x : 로그인 화면으로)
def index():
    if "uid" in session:
        user = session["uid"]
    else:
        user = "login"
    return jsonify({"user" : user}) 

@app.route("/api/login", methods = ["POST"])      #실제로 보이는 부분x
def login():
    users = request.get_json()
    uid = users['id']
    pwd = users['pwd']
    if DB.login(uid,pwd):
        session["uid"] = uid
        return jsonify(True)             #로그인 성공   ->업로드 화면
    else:
        return jsonify(False)            #로그인 실패   ->다시 로그인 화면
    
@app.route("/api/signin", methods = ["POST"])   #회원가입 처리
def signin():
    users = request.get_json()
    uid = users['id']
    pwd = users['pwd']
    email = users['email']
    if DB.signin(uid,pwd,email):
        return jsonify(True)        #회원가입 성공 -> 로그인 화면
    else:
        return jsonify(False)       #회원가입 실패 -> 다시 회원가입 화면(무슨 이유로 실패인지 전달 1. 비밀번호 재입력 오류, 이미 쓰는)
    
@app.route("/api/upload", methods = ["POST"])    #사진 업로드
def upload():
    file = request.get_json()
    f = file['url']
    photoid = str(uuid.uuid4())[:12]                   #서버에는 임의의 이름으로 받은 사진 저장
    f.save("static/img/{}.jpeg".format(photoid))
    return jsonify({"photo_url" : photoid})            #저장한 사진의 url을 프론트에 전달

@app.route("/invert", methods = ["GET"])
def invert():
    id = request.get_json()                      #저장한 사진의 url을 프론트에서 다시 받기
    photoid = id['photo_url']
    uid = session.get("uid")
    Dimage = face_model.detect_face("static/img/{}.jpeg".format(photoid))
    if Dimage == None:                          #인식이 안된 경우 
        DB.upload_photo("static/img/{}.jpeg".format(photoid),uid)   #안된 경우도 DB에 올려야할까? , 인식안된 경우 다시 업로드 페이지로?
        return jsonify({"imgsrc" : "static/img/{}.jpeg".format(photoid) , "detect" : False})
    else: 
        DB.upload_photo("static/img/{}.jpeg".format(Dimage),uid)    #감지된 경우 DB에 업로드 처리하기 / 파일 넘길때 아예 사이트 통으로 넘기기?
        return jsonify({"imgsrc" : "static/img/{}.jpeg".format(Dimage), "detect" : True})

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



@app.route("/signin")          #회원가입
def signin():
    return render_template("signin.html")
    
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
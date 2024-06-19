from flask import Flask, request, session, jsonify
from DB_handler import DBmodule
import uuid
import face_model
import datetime
from flask_cors import CORS



app = Flask(__name__)
CORS(app)
CORS(app,resource={r'*':{'origins':'*'}})
app.config["SECRET_KEY"] = "dasggasdgasd"

CORS(app, supports_credentials=True)

#app.config["SESSION_COOKIE_SAMESITE"] = "None"
#app.config["SESSION_COOKIE_SECURE"] = True

DB=DBmodule()

@app.route("/")                     #홈화면 버튼에 대한 처리(로그인o : 업로드 화면, 로그인x : 로그인 화면으로)
def index():
    if "uid" in session:
        print("Home True")
        return jsonify(True)
    else:
        print("Home False")
        return jsonify(False)

@app.route("/login", methods = ["POST"])      #실제로 보이는 부분x
def login():
    users = request.get_json()
    uid = users['id']
    pwd = users['pw']

    if DB.login(uid,pwd):
        session["uid"] = uid

        print(session["uid"])   #test
        print("True")

        response = jsonify(True)
        return response             #로그인 성공   ->업로드 화면
    else:
        print("False")
        return jsonify(False)            #로그인 실패   ->다시 로그인 화면
    
@app.route("/logout")           #로그아웃
def logout():
    if "uid" in session:
        session.pop("uid")
        return None         #홈 화면으로 이동?

@app.route("/dup" , methods = ["POST"])           
def dup():
    users = request.get_json()
    uid = users['id']
    print(uid)   #for test
    if DB.signin_verification(uid):
        print(False)
        return jsonify(False)
    else :
        print(True)
        return jsonify(True)
    
@app.route("/signin", methods = ["POST"])   #회원가입 처리
def signin():
    users = request.get_json()
    uid = users['id']
    pwd = users['pwd']
    if DB.signin(uid,pwd):
        return jsonify(True)        #회원가입 성공 -> 로그인 화면
    else:
        return jsonify(False)       #회원가입 실패 -> 다시 회원가입 화면(무슨 이유로 실패인지 전달 1. 비밀번호 재입력 오류, 이미 쓰는)
    
@app.route("/upload", methods = ["POST"])    #사진 업로드
def upload():
    f = request.files.get('file')

    print("checkupload")   #테스팅
    print(session["uid"])  #테스트

    print(f)
    photoid = str(uuid.uuid4())[:12]                   #서버에는 임의의 이름으로 받은 사진 저장
    f.save("static/img/{}.jpeg".format(photoid))   
    return jsonify({"photo_id" : photoid})            #저장한 사진의 url을 프론트에 전달

@app.route("/invert", methods = ["POST"])
def invert():
    id = request.get_json()                      #저장한 사진의 url을 프론트에서 다시 받기
    photoid = id['photo_id']

    uid = session.get("uid")       #일단
    print("invert")
    print(uid)                     #일단

    Dimage = face_model.detect_face("static/img/{}.jpeg".format(photoid))
    if Dimage == None:                          #인식이 안된 경우 
        DB.upload_photo("static/img/{}.jpeg".format(photoid),uid)   #일단 #안된 경우도 DB에 올려야할까? , 인식안된 경우 다시 업로드 페이지로?
        return jsonify({"imgsrc" : "static/img/{}.jpeg".format(photoid) , "detect" : False})
    else: 
        title = str(datetime.datetime.now())        #제목을 날짜로 저장

        DB.write_post(title, uid)               #일단
        DB.upload_photo("static/img/{}.jpeg".format(Dimage),uid)    #일단#감지된 경우 DB에 업로드 처리하기 / 파일 넘길때 아예 사이트 통으로 넘기기?
        print("invert2")
        return jsonify({"imgsrc" : "static/img/{}.jpeg".format(Dimage), "detect" : True})
    
@app.route("/users_list/<string:uid>")       #react로 어캐 받을지 고민
def users_list(uid):
    u_post = DB.get_user(uid)
    return jsonify({"post_list" :u_post, "uid" : uid})     #none이면 아직 목록이 없는 상태, uid를 통해 누구의 리스트인지표기

@app.route("/post/<string:pid>")         #목록 내의 각 포스트의 세부내용(post_list의 각 인덱스별 0번이 pid 이중배열)
def post(pid):              #pid는 post제목 즉 입력날짜를 의미한다. 위의 제목 list에서 받아오면됨
    post = DB.post_detail(pid)
    photourl = DB.get_photo_url(post["photo"],session["uid"])      #사진url을 받아오기
    return jsonify({"post" : post, "imgsrc" : photourl})


if __name__ == "__main__":
    app.run(host = "0.0.0.0")
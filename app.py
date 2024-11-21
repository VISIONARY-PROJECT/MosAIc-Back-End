from flask import Flask, request, session, jsonify
from DB_handler import DBmodule
import text_model
import uuid
import datetime
from flask_cors import CORS

app = Flask(__name__)
app.config["SECRET_KEY"] = "dasggasdgasd"
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = True


CORS(app, supports_credentials=True)



DB=DBmodule()

@app.route("/")                     #홈화면 버튼에 대한 처리(로그인o : 업로드 화면, 로그인x : 로그인 화면으로)
def index():
    return True

@app.route("/model", methods = ["POST"])    #사진 업로드
def upload():
    f = request.files.get('file')
    print("프론트 통과!")
    
    print("checkupload")   #테스팅
    print(f)
    photoid = str(uuid.uuid4())[:12]                   #서버에는 임의의 이름으로 받은 사진 저장
    f.save("static/img/{}.jpeg".format(photoid))   

    print("백엔드 통과!")
    Dtext = text_model.text_out("static/img/{}.jpeg".format(photoid))
    print("AI 통과!")

    
    if Dtext == None:                         #인식이 안된 경우 
        print("no text")
        return jsonify({"photo_id": photoid, "detect" : False, "text" : Dtext})
    else: 
        print("yes text")
        DB.write_post(photoid, Dtext)  
        return jsonify({"photo_id": photoid, "detect" : True, "text": Dtext})
    
@app.route("/category", methods = ["POST"])
def category():
    info = request.get_json()                      #저장한 사진의 url을 프론트에서 다시 받기
    photoid = info['photo_id']
    category_name = info['category']

    DB.update_category(photoid, category_name)

@app.route("/text_list", methods = ["POST"])       #사용자의 해당 카테고리를 가지는 사진 목록을 보여줌.
def text_list():
    info = request.get_json()       #카테고리 정보를 받을 것
    category_name = info['category']
        
    c_post = DB.get_category(category_name)       #해당 카테고리의 이미지 소스들

    return jsonify({"post_list" :c_post, "category" : category_name})     #none이면 아직 목록이 없는 상태, category를 통해 어떤 카테고리의 리스트인지표기

@app.route("/detail",methods = ["POST"])
def detail():
    info = request.get_json()
    photoid = info['photoid']

    detail_info = DB.get_detail(photoid)
    print(detail_info)

    return jsonify({"text" : detail_info["Dtext"]})

if __name__ == "__main__":
    app.run(host = "0.0.0.0")
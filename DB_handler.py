import pyrebase
import json
import uuid

class DBmodule:
    def __init__(self):
        with open("./auth/firebaseAuth.json") as f:
            config = json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
        self.storage = firebase.storage()

    def login(self, uid, pwd):
        users = self.db.child("users").get().val()
        try:
            userinfo = users[uid]
            if userinfo["pwd"] == pwd:
                return True
            else:
                return False
        except:
            return False

    def signin_verification(self, uid):
        users = self.db.child("users").get().val()
        for i in users:
            if uid == i:
                return False
        return True    

    def signin(self, id, pwd, email, name):
        information={
            "pwd":pwd,
            "uname":name,
            "email":email
        }
        if self.signin_verification(id):
            self.db.child("users").child(id).set(information)
            return True
        else:
            return False

    
    def write_post(self, title, contents, uid):
        pid = str(uuid.uuid4())[:12]             #post의 아이디
        information ={
            "title":title,
            "contents":contents,
            "uid":uid
        }
        self.db.child("posts").child(pid).set(information)

    def upload_photo(self, photo_url, userid):
        spid = str(uuid.uuid4())[:12]
        self.storage.child("images/{}.jpg" .format(spid)).put(photo_url, userid)
        ad = {"photo" : "images/{}.jpg" .format(spid)}
        users_post =self.db.child("posts").get().val()
        for post in users_post.items():
            if post[1]["uid"]==userid:
                self.db.child("posts").child(post[0]).update(ad)

    
    def post_list(self):
        post_lists = self.db.child("posts").get().val()
        return post_lists
    
    def post_detail(self, pid):
        post = self.db.child("posts").get().val()[pid]
        return post

    def get_user(self, uid):
        post_list =[]
        users_post =self.db.child("posts").get().val()
        try:
            for post in users_post.items():
                if post[1]["uid"]==uid:
                    post_list.append(post)
            return post_list
        except:
            return post_list
    def get_photo_url(self, purl, uid):
        print(self.storage.child(purl).get_url(uid))
        return self.storage.child(purl).get_url(uid)

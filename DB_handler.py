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

    def signin(self, id, pwd):
        information={
            "pwd":pwd
        }
        if self.signin_verification(id):
            self.db.child("users").child(id).set(information)
            return True
        else:
            return False
        
    def write_post(self, photoid, Dtext):
        information ={
            "photo":"static/img/{}.jpeg".format(photoid),
            "text":Dtext,
            "category" : None
        }
        self.db.child("posts").child(photoid).set(information)

    def update_category(self, photoid, category):
        self.db.child("posts").child(photoid).update({"category":category})

    def get_category(self, category):
        post_list =[]
        users_post =self.db.child("posts").get().val()
        try:
            for post in users_post.items():
                if post[1]["category"]==category:
                    print(post[0])  #post[0]가 photoid?
                    post_list.append(post[0])
            return post_list
        except:
            return post_list
        
    def get_detail(self, photoid):
        posts =self.db.child("posts").get().val()
        try: 
            for post in posts.items():
                if post[0] == photoid:
                    print(post[0])
                    return(post[1])
        except:
            return None
                    
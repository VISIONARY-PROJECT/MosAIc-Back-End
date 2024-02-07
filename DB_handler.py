import pyrebase
import json

class DBmodule:
    def __init__(self):
        with open("./auth/firebaseAuth.json") as f:
            config = json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()

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

    
    def write_post(self, user, contents):
        pass
    
    def post_list(self):
        pass
    
    def post_detail(self, pid):
        pass

    def get_user(self, uid):
        pass
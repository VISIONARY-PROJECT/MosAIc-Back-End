import pyrebase
import json

class DBmodule:
    def __init__(self):
        with open("./auth/firebaseAuth.json") as f:
            config = json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()

    def login(self, id, pwd):
        pass

    def signin(self, id, pwd, email, name):
        information={
            "pwd":pwd,
            "uname":name,
            "email":email
        }
        self.db.child("users").child(id).set(information)

    
    def write_post(self, user, contents):
        pass
    
    def post_list(self):
        pass
    
    def post_detail(self, pid):
        pass

    def get_user(self, uid):
        pass
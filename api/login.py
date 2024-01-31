# Old code:

# from flask import Blueprint, request
# from flask_restful import Api, Resource, reqparse
# from __init__ import db
# # from .. import db # Error 3: ImportError: attempted relative import beyond top-level package
# from ..model.login import User # This is the class, you can find it in login.py model (in this case it is "User")

# loginBp = Blueprint("login", __name__)
# loginAPI = Api(loginBp)

# class loginAPI(Resource): # REST API to add/delete INDIVIDUAL user data
#     def get(self):
#         id = request.args.get("id")
#         login = db.session.query(User).get(id)
#         if login:
#             return login.to_dict()
#         return {"message": "not found"}, 404

#     def post(self):
#         parser = reqparse.RequestParser()
        
#         parser.add_argument("username", required=True, type=str)
#         parser.add_argument("password", required=True, type=str)
#         args = parser.parse_args()
#         login = User(args["username"], args["password"])

#         try:
#             db.session.add(login)
#             db.session.commit()
#             return login.to_dict(), 201
#         except Exception as exception:
#             db.session.rollback()
#             return {"message":f"error {exception}"}, 500

#     def put(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument("id", required=True, type=int)
#         parser.add_argument("username")
#         parser.add_argument("password")
#         args = parser.parse_args()
        
#         try:
#             login = db.session.query(User).get(args["id"])
#             if login:
#                 if args["username"] is not None:
#                     login.username = args["username"]
#                 if args["password"] is not None:
#                     login.password = args["password"]
#                 db.session.commit()
#                 return login.to_dict(), 200
#             else:
#                 return {"message": "not found"}, 404
#         except Exception as exception:
#             db.session.rollback()
#             return {"message": f"error {exception}"}, 500
    
#     def delete(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument("id", required=True, type=int)
#         args = parser.parse_args()

#         try:
#             login = db.session.query(User).get(args["id"])
#             if login:
#                 db.session.delete(login)
#                 db.session.commit()
#                 return login.to_dict()
#             else:
#                 return {"message": "not found"}, 404
#         except Exception as exception:
#             db.session.rollback()
#             return {"message": f"error {exception}"}, 500

# class ListLoginAPI(Resource): # EXTRA: List API to clear out entire databse/edit entire database (essentially anything to do with entire databse)
#     def get(self):
#         scholarSearch = db.session.query(User).all()
#         return [scholarSearch.to_dict() for scholar in scholarSearch]
    
#     def delete(self):
#         try:
#             db.session.query(User).delete()
#             db.session.commit()
#             return
#         except Exception as exception:
#             db.session.rollback()
#             return {"message": f"error {exception}"}

# loginAPI.add_resource(loginAPI, "/scholarSearch")
# loginAPI.add_resource(ListLoginAPI, "/scholarSearchList")

# New code:

from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse
from __init__ import db
from model.login import Login

loginBp = Blueprint("login", __name__)
loginApi = Api(loginBp)

class LoginAPI(Resource):
    def get(self):
        id = request.args.get("id")
        login = Login.query.get(id)
        if login:
            return login.to_dict()
        return {"message": "not found"}, 404
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True, type=str)
        parser.add_argument("password", required=True, type=str)
        args = parser.parse_args()
        login = Login.query.filter_by(_username=args["username"], _password=args["password"]).first()
        if login:
            return login.to_dict()
        return {"message": "not found"}, 404

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id", required=True, type=int)
        parser.add_argument("username")
        parser.add_argument("password")
        args = parser.parse_args()
        
        try:
            login = Login.query.get(args["id"])
            if login:
                if args["username"] is not None:
                    login.username = args["username"]
                if args["password"] is not None:
                    login.password = args["password"]
                db.session.commit()
                return login.to_dict(), 200
            else:
                return {"message": "not found"}, 404
        except Exception as exception:
            db.session.rollback()
            return {"message": f"error {exception}"}, 500
    
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id", required=True, type=int)
        args = parser.parse_args()

        try:
            login = Login.query.get(args["id"])
            if login:
                db.session.delete(login)
                db.session.commit()
                return login.to_dict()
            else:
                return {"message": "not found"}, 404
        except Exception as exception:
            db.session.rollback()
            return {"message": f"error {exception}"}, 500

class CreateAccAPI(Resource):
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True, type=str)
        parser.add_argument("password", required=True, type=str)
        args = parser.parse_args()
        login = Login(args["username"], args["password"])

        try:
            db.session.add(login)
            db.session.commit()
            return login.to_dict(), 201
        except Exception as exception:
            db.session.rollback()
            return {"message":f"error {exception}"}, 500
        
class AuthorizeAPI(Resource):
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id", required=True, type=int)
        parser.add_argument("username")
        parser.add_argument("password")
        args = parser.parse_args()
        
        try:
            login = Login.query.get(args["id"])
            if login:
                if args["username"] is not None:
                    login.username = args["username"]
                if args["password"] is not None:
                    login.password = args["password"]
                db.session.commit()
                return login.to_dict(), 200
            else:
                return {"message": "not found"}, 404
        except Exception as exception:
            db.session.rollback()
            return {"message": f"error {exception}"}, 500
        
class LoginListAPI(Resource):
    def get(self):
        login = Login.query.all()
        return [login.to_dict() for login in login]
    
    def delete(self):
        try:
            db.session.query(Login).delete()
            db.session.commit()
            return
        except Exception as exception:
            db.session.rollback()
            return {"message": f"error {exception}"}

loginApi.add_resource(LoginAPI, "/login")
loginApi.add_resource(CreateAccAPI, "/signUp")
loginApi.add_resource(AuthorizeAPI, "/authorize")
loginApi.add_resource(LoginListAPI, "/loginList")


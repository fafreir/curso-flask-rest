from flask_sqlalchemy import Resource, reqparse 
from models.usuario import UserModel

class User(Resource):

    # Visualizar
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message':'User not found.'}, 404
    
    # deletar
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            user.delete_user()
            return {'message':'User deleted.'}
        return {'message':'User not found.'}
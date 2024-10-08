from flask_restful import Resource, reqparse
from blacklist import BLACKLIST
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, create_refresh_token
import hmac

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True,
                       help="The field 'login' cannot left be")
atributos.add_argument('senha', type=str, required=True,
                       help="The field 'senha' cannot left be")


class User(Resource):

    # Visualizar
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            user.delete_user()
            return {'message': 'User deleted.'}
        return {'message': 'User not found.'}


class UserRegister(Resource):
    # /cadastro
    def post(self):

        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            # return {"message": "The login '{}' already exists.".format{dados['login']}}
            return {"message": f'The login {dados["login"]} already exists'}

        user = UserModel(**dados)
        user.save_user()
        return {'message': 'User created sucessfully'}, 201


class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()
        user = UserModel.find_by_login(dados['login'])

        if user and hmac.compare_digest(user.senha, dados['senha']):
            access_token = create_access_token(identity="example_user")
            refresh_token = create_refresh_token(identity=user.user_id)
            token_de_acesso = create_access_token(identity=user.user_id)
            return {'acess_token': token_de_acesso, "refresh_token": refresh_token}, 200
        return {'message': 'The username or password is incorrect'}, 401


class UserLogout(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti']  # JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out sucessfully'}

from flask_restful import Resource, reqparse
from models.usuario import UserModel


class User(Resource):

    # Visualizar
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404

    # deletar
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            user.delete_user()
            return {'message': 'User deleted.'}
        return {'message': 'User not found.'}


class UserRegister(Resource):
    # /cadastro
    def post(self):
        atributos = reqparse.RequestParser()
        atributos.add_argument('login', type=str, required=True,
                               help="The field 'login' cannot left be")
        atributos.add_argument('senha', type=str, required=True,
                               help="The field 'senha' cannot left be")
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            # return {"message": "The login '{}' already exists.".format{dados['login']}}
            return {"message": f'The login {dados["login"]} already exists'}

        user = UserModel(**dados)
        user.save_user()
        return {'message': 'User create sucessfully'}, 201

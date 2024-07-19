from sql_alchemy import banco 

class UserModel(banco.Model):
    __table__ = 'usuarios'

    user_id = banco.Column(banco.Integer, primary_key = True)
    login = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))

    def __init__(self, login, senha):
        self.login = login
        self.senha = senha 
    
    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login
        }
    
    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id = user_id).first() 
        if user:
            return user 
        return None 
    
    # Cadastrar usuario
    def save_user(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_hotel(self):
        banco.session.delete(self)
        banco.session.commit()
    
    
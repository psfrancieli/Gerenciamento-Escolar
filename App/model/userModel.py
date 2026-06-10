from __future__ import annotations
from App.config.database import Database

class Usuario:
    id = None
    name = ""
    email = ""
    password = ""
    type = ""
    active = True

    def __init__(self , id=None , name="" , email="" , password="" , type="" , active=True):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.type = type 
        self.active = bool(active)

    @classmethod
    def createUser(cls , user:"Usuario"):
        try:
            DB = Database()
            sql = "INSERT INTO usuarios (nome, email , senha , tipo_user) VALUES(%s , %s , %s , %s)"
            params = (user.name , user.email , user.password , user.type)
            result = DB.execute(sql  , params)
            return result
        except Exception as e:
            print(f'Erro na criação do usuario {e}')
            raise RuntimeError

    @classmethod
    def updateUser(cls ,user:"Usuario"):
        try:
            DB = Database()
            sql = "UPDATE usuarios SET nome = %s , email = %s , senha = %s WHERE id = %s"
            params = (user.name , user.email , user.password , user.id)
            result = DB.execute(sql , params)
            return result
        except Exception as e:
            print(f'Não foi possivel atualizar os dados do usuario {e}')
            raise RuntimeError
        
    @classmethod
    def deactiveUser(cls, id):
        try:
            DB = Database()
            sql = "UPDATE usuarios SET ativo = 0 WHERE id = %s"
            params = (id , )
            result = DB.execute(sql, params)
            return result
        except Exception as e:
            print(f'Erro ao tentar desativar o usuario {e}')
            raise RuntimeError
        
    @classmethod
    def findById(cls, id):
        try:
            DB = Database()
            sql = "SELECT * FROM usuarios WHERE id = %s"
            params = (id,)
            result = DB.fetchOne(sql , params)
            if not result:
                return None
            return cls(*result.values())
            
        except Exception as e:
            print(f'Erro ao encontrar usuario por id {e}')
            raise RuntimeError

    @classmethod
    def findByEmail(cls , email):
        try:
            DB = Database()
            sql = "SELECT * FROM usuarios WHERE email = %s"
            params = (email , )
            result = DB.fetchOne(sql , params)
            if not result:
                return None
            return cls(*result.values()) 
        except Exception as e:
            print(f'Erro ao buscar o usuario por email {e}')
            raise RuntimeError
        

    @classmethod
    def findAll(cls):
        try:
            DB = Database()
            sql = "SELECT * FROM usuarios"
            result = DB.fetchAll(sql , )
            user = [cls(*row.values()) for row in result]
            return user
        except Exception as e:
            print(f'Erro ao buscar todos os usuarios {e}')
            raise RuntimeError
            

    @classmethod
    def findUserActive(cls):
        try:
            DB = Database()
            sql = "SELECT * FROM usuarios WHERE ativo = 1"
            result = DB.fetchAll(sql)
            user = [cls(*row.values()) for row in result]
            return user
        except Exception as e:
            print(f'Erro ao listar usuarios ativos {e}')
            raise RuntimeError

    # @classmethod
    # def findByEmail(cls):
    #     try:
    #         DB = Database()
    #         sql = "SELECT nome , email FROM usuarios WHERE email= %s"
    #         result = DB.fetchOne()


    @classmethod
    def login(cls , email):
        try:
            DB = Database()
            sql = "SELECT * FROM usuarios WHERE email = %s AND ativo = 1"
            params = (email,)
            result = DB.fetchOne(sql, params)
            if not result: return None
            return cls(*result.values())
        except Exception as e:
            print(f"Não foi possivel fazer login! {e}")
            raise ValueError
        
    def showInfo(self):
        print(f"""
            ID : {self.id}
            Name : {self.name}
            Email: {self.email}
            Password: {self.password}
            Type: {self.type}
            Active: {self.active}
        """)

if __name__ == "__main__":
    user = Usuario(id= 5 , name="Chico" , email="caique22@gmail.com" , password="123567")
    criar = Usuario.login("caique22@gmail.com")
    print(criar.showInfo())
    #print(criar)
    #print(criar.showInfo())
    # for u in todosUsuarios:
    #     print(u.showInfo())
    resultado = Usuario.findById(100)
    print (resultado.id, resultado.name, resultado.email)

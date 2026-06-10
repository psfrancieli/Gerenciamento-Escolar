from App.config.database import Database

class Student:
    id = None
    nome = ""
    nome_social = None
    CPF = ""
    data_nasc = ""
    RA = ""
    RM = ""
    obs = None
    status = True
    data_registro = ""
    data_status = None


    def __init__(self, id = None, nome = "", nome_social = None, CPF = "", data_nasc = "", RA = "", RM = "", obs = None, status = True, data_registro = "", data_status = None):
        self.id = id
        self.nome = nome
        self.nome_social = nome_social
        self.CPF = CPF
        self.data_nasc = data_nasc
        self.RA = RA
        self.RM = RM
        self.obs = obs
        self.status = status
        self.data_registro = data_registro
        self.data_status = data_status


    @classmethod
    def Create(cls, student:"Student"):
        try:
            DB = Database()
        
            sql = """INSERT INTO alunos (nome, nome_social, CPF, data_nasc, RA, RM, Observacao)
                     VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                 
            params = (student.nome, student.nome_social, student.CPF, student.data_nasc, student.RA, student.RM, student.obs)

            novo_id = DB.insert(sql, params) 
        
            print(f"Aluno inserido com sucesso! ID gerado: {novo_id}")
            return novo_id
        except Exception as erro:
            print(f'nao foi possível inserir novo aluno: {erro}')

    @classmethod
    def Update(cls, student: "Student"):
        try:
            DB = Database()
            sql = """UPDATE alunos SET nome = %s, nome_social = %s, CPF = %s, 
                    data_nasc = %s, RA = %s, RM = %s, Observacao = %s, status = %s 
                    WHERE id = %s"""
        
            
            params = (student.nome, student.nome_social, student.CPF, student.data_nasc, 
                     student.RA, student.RM, student.obs, student.status, student.id)
                  
            DB.execute(sql, params)
            print(f"Aluno atualizado con sucesso, RA: {student.RA}, ID: {student.id}")
            return student.RA, student.id
        except Exception as erro:
            print(f'Não foi possível atualizar os dados do aluno: {erro}')
        raise RuntimeError
        
    @classmethod
    def delete(cls, id):
        try:
            DB = Database()
            sql = "UPDATE alunos SET status = 0 WHERE id = %s"
            params = (id , )
            result = DB.execute(sql, params)
            print('aluno desativado com sucesso!')
            return result
        except Exception as erro:
            print(f'Erro ao tentar desativar o aluno {erro}')
            raise RuntimeError
    @classmethod
    def activate(cls, id):
        try:
            DB = Database()
            sql = "UPDATE alunos SET status = 1 WHERE id = %s"
            params = (id , )
            result = DB.execute(sql, params)
            print('aluno ativado com sucesso!')
            return result
        except Exception as erro:
            print(f'Erro ao tentar desativar o aluno {erro}')
            raise RuntimeError
        
    @classmethod
    def linkStudentInClassroom(cls, student_id, room_id):

        try:
            DB = Database()
            sql = """INSERT INTO sala_alunos (id_aluno, id_sala) VALUES (%s, %s)"""

            params = (student_id, room_id)
            result = DB.insert(sql, params)
            print(f"Aluno inserido na sala {result}")

        except Exception as erro:
            print(f'Erro ao tentar inserir aluno na sala {erro}')
            raise RuntimeError
        
    @classmethod
    def findById(cls, id):
        try:
            DB = Database()
            sql = "SELECT * FROM alunos WHERE id = %s"
            params = (id,)
            result = DB.fetchOne(sql , params)
            if not result:
                return None
            return cls(*result.values())
        except Exception as erro:
            print(f'Erro ao encontrar aluno por id {erro}')
            raise RuntimeError

    @classmethod
    def _getObjectList(cls, lista):
        return [cls(*user.values())for user in lista]

    @classmethod
    def findAll(cls):
        try:
            DB = Database()
            sql = "SELECT * FROM alunos"
            result = DB.fetchAll(sql)
            return cls._getObjectList(result)
        except Exception as erro:
            print(f'Erro lsitagem de alunos: {erro}')
            raise RuntimeError
    
    @classmethod
    def findActive(cls):
        try:
            DB = Database()
            sql = "SELECT * FROM alunos WHERE status = 1"
            result = DB.fetchAll(sql)
            student = [cls(*row.values()) for row in result]
            return student
        except Exception as erro:
            print(f'Erro lista de alunos ativos {erro}')
            raise RuntimeError
    
    def showInfo(self):
        print(f"""
            ID : {self.id}
            Nome : {self.nome}
            Nome Social: {self.nome_social}
            CPF: {self.CPF}
            Data Nascimento: {self.data_nasc}
            RA: {self.RA}
            RM: {self.RM}
            STATUS: {self.status}
            Data Registro: {self.data_registro}
            Observações: {self.obs}
        """)

    @classmethod
    def findByRoomID(cls, roomID):
        try:
            DB = Database()
            sql = """
            SELECT a.id, a.nome, a.nome_social, a.CPF, a.data_nasc, a.RA, a.RM, a.Observacao, a.status, a.data_registro
            FROM alunos AS a JOIN sala_alunos AS sa ON a.id = sa.id_aluno
            WHERE sa.id_sala = %s
            AND sa.id = (SELECT MAX(sa2.id) FROM sala_alunos sa2 WHERE sa2.id_aluno = a.id) AND a.status = 1;
            """
            params = (roomID,)
            result = DB.fetchAll(sql, params)
            if result: 
                return cls._getObjectList(result)
            return cls()
        except Exception as e:
            print(f'Erro ao buscar alunos')
            raise RuntimeError
        

    @classmethod
    def searchStudent(cls, search):
        try:
            DB = Database()
            sql = """
                SELECT * FROM alunos 
                WHERE 
                    RA = %s 
                    OR nome LIKE CONCAT('%', %s, '%') 
                    OR nome_social LIKE CONCAT('%', %s, '%')
            """
            params = (search, search, search)
            result = DB.fetchAll(sql, params)
            return cls._getObjectList(result)
        except Exception as e:
            print(f'Erro ao buscar alunos {e}')
            raise RuntimeError

    @classmethod
    def AllStudentsWithoutClassroom(cls):
        try:
            DB = Database()
            sql = "SELECT a.id , a.nome,a.nome_social, a.CPF , a.data_nasc , a.RA , a.RM ,a.Observacao , a.status, a.data_registro FROM alunos a LEFT JOIN sala_alunos sa ON a.id = sa.id_aluno WHERE sa.id_aluno IS NULL;"
            result =  DB.fetchAll(sql)
            return cls._getObjectList(result)
        except Exception as e:
            print(f'Erro ao tentar buscar alunos que não possuem sala {e}')
            raise RuntimeError
        
if __name__ == "__main__":
    # Student.Update(2)

    # listaEstudantes = Student.findByRoomID(10)
    # for i in listaEstudantes:
    #     i.showInfo()
    # print(s)
    # a = Student.searchStudent("Lucas Crispim")
    # print(a)
    # pass
    estudanteSemClasse = Student.AllStudentsWithoutClassroom()
    for i in estudanteSemClasse:
        i.showInfo()
    


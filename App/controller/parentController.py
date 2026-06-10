from App.model.parentModel import Parent 
from App.controller.AddressController import AddressController
from App.controller.telephoneController import TelephoneController
import re

class ParentController:
    
    @classmethod
    def validCpf(cls, cpf):
        pass


    @classmethod
    def create(cls, parent:any):
        try:
            newParent:Parent = Parent(nome=parent["nome"], cpf=parent["cpf"])
            if not newParent.name.strip() or not newParent.cpf:
                print(f'E necessario preencher todos os dados')
                return False
            parentID = Parent.create(newParent.name, newParent.cpf)
            if parentID:
                address = parent.get('address')
                resp = AddressController.create(parentID, address)
                print(resp)

                telephone = parent.get('telephone')
                resp = TelephoneController.create(parentID, telephone)
                print(resp)
        except Exception as e:
            print(f'Erro ao tentar a criação de usuario {e}')
            raise RuntimeError
        
    @classmethod
    def update(cls, parent: any):
        try:
            updatedParent: Parent = Parent(nome=parent["nome"], cpf=parent["cpf"], id=parent["id"])
            if not updatedParent.name.strip() or not updatedParent.cpf:
                print(f'E necessario preencher todos os dados')
                return False
            updated = Parent.update(updatedParent)
            if updated is not None:
                address = parent.get('address')
                if address:
                    resp = AddressController.update(address)
                    print(resp)

                telephone = parent.get('telephone')
                if telephone:
                    resp = TelephoneController.update(telephone["id"], telephone["telephone"])
                    print(resp)
        except Exception as e:
            print(f'Erro ao tentar a atualização de usuario {e}')
            raise RuntimeError
    
    @classmethod
    def findParentForStudent(cls, studentID):
        try:
            studentID = ParentController.validateID(studentID)
            lista = Parent.findParentForStudent(studentID)
            return lista
        except Exception as e:
            raise e
        
    @classmethod
    def findParentId(cls, parentId):
        try:
            parId = Parent.getUnique(parentId)
            return parId
        except Exception as e:
            raise e
    
    @classmethod
    def validateID(cls, value):
        if not isinstance(value, int): raise TypeError(f"ID incorreto")
        if value <= 0: raise ValueError("Id invalido")
        return value
    
    @classmethod
    def deleteParent(cls, responsavel_id, aluno_id):

        try:

            if not responsavel_id or not aluno_id:
                return {"Parente não foi passado "}
            
            Parent.deleteParent(responsavel_id, aluno_id)

        except Exception as e:
            return {"Erro ao excluir parente"}
    

if __name__ == "__main__":
    # testParent = {
    #     "name" : "cavalo",
    #     "cpf" : "1234567233",
    #     "address" : {"city" : "Sorocaba" , "neighborhood" : "Paineras" , "street" : "Vitor Gomes", "complement" : "Scrum-Master", "cep" : "1909192"}
    # }
    # ParentController.create(testParent)

    a= ParentController.findParentForStudent(5)

    print(a)

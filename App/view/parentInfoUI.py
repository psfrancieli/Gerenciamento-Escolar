from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5.uic import loadUi
from App.utils.qthread import Trabalhador
from App.controller.telephoneController import TelephoneController
from App.controller.parentController import ParentController
from App.controller.AddressController import AddressController
from App.view.registerParentUI import RegisterParentUI




class ParentInfoUI(QDialog):
    
    def __init__(self, studentID, **kwargs):
        super().__init__(**kwargs)
        loadUi("App/view/ui/parentInfo.ui", self)
        self.studentID = studentID
        self.listParents = ParentController.findParentForStudent(self.studentID)
        self.btnEditar.clicked.connect(self.enableEditing)
        self.cep.editingFinished.connect(self.buscarCEP)
        self.populateComboBox()
        self.comboBox.currentIndexChanged.connect(self.getInfo)
        self.btnRemover.clicked.connect(self.removeParent)
        self.getInfo()
        self.show()
        
        
    def getInfo(self):
        if self.comboBox.count() == 0:
                return
        indexResp = self.comboBox.currentIndex()
        parent = self.listParents[indexResp]

        self.nome.setText(parent.name)
        self.cpf.setText(parent.cpf)
        self.respLegal.setChecked(parent.legal_guardian)
        self.lockFields(True)

        listTelephone = TelephoneController.findTelephoneByParentId(parent.id)
        self.telefone.setText(listTelephone[0].telephone)

        listAddress = AddressController.findAddressByParentId(parent.id)
        self.cidade.setText(listAddress[0].city)
        self.complemento.setText(listAddress[0].complement)
        self.rua.setText(listAddress[0].street)
        self.bairro.setText(listAddress[0].neighborhood)
        self.cep.setText(listAddress[0].cep)
        self.numero.setText(listAddress[0].number)

        self.nome.setReadOnly(True)
        self.cpf.setReadOnly(True)

    def lockFields(self, state:bool):
        self.cidade.setReadOnly(state)
        self.complemento.setReadOnly(state)
        self.rua.setReadOnly(state)
        self.bairro.setReadOnly(state)
        self.cep.setReadOnly(state)
        self.numero.setReadOnly(state)
        self.telefone.setReadOnly(state)
        self.respLegal.setEnabled(not state)

    def enableEditing(self):
        self.lockFields(False)
        self.btnEditar.setText("Salvar")
        self.btnEditar.clicked.disconnect(self.enableEditing)
        self.btnEditar.clicked.connect(self.saveParent)

    def saveParent(self):
        print(self.telefone.text())
        print(self.cidade.text())
        print(self.complemento.text())
        print(self.rua.text())
        print(self.bairro.text())
        print(self.cep.text())
        print(self.numero.text())

        self.lockFields(True)
        self.btnEditar.setText("Editar")
        self.btnEditar.clicked.disconnect(self.saveParent)
        self.btnEditar.clicked.connect(self.enableEditing)
       
    def buscarCEP(self):
        cep = self.cep.text()
        self.validarCEP =Trabalhador(AddressController.requestCep, cep=cep)
        self.validarCEP.signal_CEP.connect(self.popularCEP)
        self.validarCEP.finished.connect(self.validarCEP.deleteLater)
        self.validarCEP.start()

    def popularCEP(self, dadosCEP):
        self.cidade.setText(dadosCEP.get("city"))
        self.bairro.setText(dadosCEP.get("neighborhood"))
        self.rua.setText(dadosCEP.get("street"))

    def populateComboBox(self):
        try:
            for parent in self.listParents:
                self.comboBox.addItem(parent.name)
        except Exception as e:
            print(f"{e}")

    def removeParent(self):
        try:
            indexResp = self.comboBox.currentIndex()
            parent = self.listParents[indexResp]
            ParentController.deleteParent(parent.id, self.studentID)
            self.listParents.pop(indexResp)
            self.comboBox.removeItem(indexResp)
        except Exception as e:
            print(f"Erro ao remover parente: {e}")

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    from App.controller.studentController import StudentController
    aluno = StudentController.getById(10)
    app = QApplication([])
    login = ParentInfoUI(aluno.id)
    app.exec_()
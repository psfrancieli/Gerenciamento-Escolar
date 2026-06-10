from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QPushButton, QApplication, QTableWidget
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtCore import Qt
from App.controller.userController import UserController

class adminUI(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("App/view/ui/adminScreen.ui", self)

        dados = UserController.findUserActive()
        self.setValuesOnTable(dados)

        self.tableWidget.itemClicked.connect(self.ao_clicar_item)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.timer = QTimer()

        self.selectedId = None

        self.cancelar.setEnabled(False)

        self.show()


    def setValuesOnTable(self, values):
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(len(values))

        for i, v in enumerate(values):

            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(v.name)))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(v.email)))

            btn = QPushButton("Excluir") 
            btn.setCursor(Qt.PointingHandCursor) 
            btn.clicked.connect(lambda _, id=v.id: self.btn_act(id))
            self.tableWidget.setCellWidget(i, 2, btn)

            
    def btn_act(self, id):
        resp = UserController.deactiveUser(id)

        print(resp)

        dados = UserController.findUserActive()
        self.setValuesOnTable(dados)

    def clearText(self):
        self.label1.setText("")

    @pyqtSlot()
    def on_salvar_clicked(self):
        name = self.name.text()
        email = self.email.text()
        password = self.senha.text()
        confirmarSenha = self.confirmarSenha.text()
        type = self.typeUser.currentText()

        if not name or not email:
            self.label1.setText("Preencha corretamente as Informações!")
            self.timer.singleShot(2300, self.clearText)
            return
        
        if not password or not confirmarSenha:
            self.label1.setText("Preencha corretamente as Informações!")
            self.timer.singleShot(2300, self.clearText)
            return

        if not UserController.isValidPassword(password):
            self.label1.setText("Senha fraca! Mínimo 8 caracteres e 1 maiúscula.")
            self.timer.singleShot(2300, self.clearText)
            return
        
        if password != confirmarSenha :
                self.label1.setText("As senhas não Coicidem!")
                self.timer.singleShot(2300, self.clearText)
                return  

        resp = UserController.createUser({
                "name": name,
                "email": email,
                "password": password,
                "type": type
            })
        

        if resp:
            self.label1.setText("Usuário criado com sucesso!")
            self.timer.singleShot(2300, self.clearText)
            

            self.name.setText("")
            self.email.setText("")
            self.senha.setText("")
            self.confirmarSenha.setText("")

            dados = UserController.findUserActive()
            self.setValuesOnTable(dados)

        else: 
            self.label1.setText("Preencha os Dados Corretamente!")
            self.timer.singleShot(2300, self.clearText)
        
    def ao_clicar_item(self, item):
        row = item.row()  

        nome  = self.tableWidget.item(row, 0)
        email = self.tableWidget.item(row, 1)
        tipo = self.tableWidget.item(row, 2)

        dados = UserController.findUserActive()
        self.selectedId = dados[row].id

        self.name.setText(nome.text())
        self.email.setText(email.text())
        self.confirmarSenha.setText("")
        self.senha.setText("")  
        self.cancelar.setEnabled(True) 

        self.salvar.setText("Atualizar")

        if tipo:
            self.typeUser.setCurrentText(tipo.text().upper())

            

    def on_cancelar_clicked(self):
        self.name.setText("")
        self.email.setText("")
        self.cancelar.setEnabled(False)
        self.salvar.setText("Salvar") 

          

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication([])
    admin = adminUI()
    app.exec_()
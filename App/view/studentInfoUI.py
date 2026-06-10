from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5.uic import loadUi
from App.controller.studentController import StudentController
from App.view.reportUI import ReportUI

class StudentInfoUI(QDialog):
    def __init__(self, student, **kwargs):
        super().__init__(**kwargs)
        loadUi("App/view/ui/studentInfo.ui", self)
        self.student = student
        self.getInfo()
        self.show()
    
        self.btnOcorrencias.clicked.connect(self.openOcorrencias)
        


    def getInfo(self):
        self.nome_4.setText(self.student.nome)
        self.nomeSocial.setText(self.student.nome_social)
        self.data_6.setDate(self.student.data_nasc)
        self.cpf_3.setText(self.student.CPF)
        self.ra.setText(self.student.RA)
        self.rm.setText(self.student.RM)
        self.obs.setText(self.student.obs)
        
        self.cpf_3.setReadOnly(True)
        self.ra.setReadOnly(True)
        self.rm.setReadOnly(True)

    def openOcorrencias(self):
            self.report = ReportUI(self.student.id)
            self.report.show()

    @pyqtSlot()
    def on_btnEdit_clicked(self):
        if self.btnEdit.text() == "Editar":
            self.btnEdit.setText("Salvar") 
            self.btnEdit.setStyleSheet("background-color: #4CAF50")
            self.nomeSocial.setEnabled(True)
            self.obs.setEnabled(True)
            
            print(self.student.id)
            

        else:
            self.btnEdit.setText("Editar")
            self.btnEdit.setStyleSheet("")
            self.nomeSocial.setEnabled(False)
            self.obs.setEnabled(False)
            
        nomeSocial =  self.nomeSocial.text()
        obs = self.obs.toPlainText()
        
        self.student.nome_social = nomeSocial
        self.student.obs = obs
        
        StudentController.update(self.student)
        print(self.student.obs, self.student.nome_social)

    

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    aluno = StudentController.getById(7)
    app = QApplication([])
    login = StudentInfoUI(aluno)
    app.exec_()
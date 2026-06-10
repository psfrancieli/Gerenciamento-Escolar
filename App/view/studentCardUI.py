from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot
from PyQt5.uic import loadUi
from App.view.newReportUI import NewReportUI
from App.view.parentInfoUI import ParentInfoUI
from App.view.studentInfoUI import StudentInfoUI
from App.controller.userController import getCurrentUser

class StudentCardUI(QWidget):
    def __init__(self, student, **kwargs):
        super().__init__(**kwargs)
        loadUi("App/view/ui/studentCard.ui", self)
        

        self.student = student
        self.person = self.student.nome_social or self.student.nome
        self.studentName.setText(self.person)
        
        if getCurrentUser()['tipo'] != 'agente':
            self.studentName.clicked.connect(self.openScreen)
            self.parentInfo.clicked.connect(self.openScreen)
        self.newReport.clicked.connect(self.openScreen)

        
    def openScreen(self):
        sender = self.sender()
        if sender == self.studentName:
            self.studentInfo = StudentInfoUI(self.student)
            self.studentInfo.show()

        elif sender == self.newReport:
            self.freshReport = NewReportUI(self.student.id)
            self.freshReport.show()

        elif sender == self.parentInfo:
            self.parentData = ParentInfoUI(self.student.id)
            self.parentData.show()


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    from App.controller.studentController import Student
    student = Student.findById(13)
    app = QApplication([])
    login = StudentCardUI(student)
    login.show()
    app.exec_()
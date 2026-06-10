from PyQt5 import QtCore
from PyQt5.QtWidgets import QMenu, QPushButton, QPushButton, QWidget, QVBoxLayout, QLabel, QMainWindow, QAction, QScrollArea
from PyQt5.QtCore import Qt, pyqtSlot, QPoint, pyqtSignal
from PyQt5.uic import loadUi
from App.controller.roomController import RoomController
from App.view.adminUI import adminUI
from App.view.classCardUI import ClassCardUI
from App.view.registerClassUI import RegisterClassUI
from App.controller.loginController import logout
from App.view.registerStudentUI import RegisterStudentUI
from App.view.registerEmployeeUI import RegisterEmployeeUI
from App.controller.studentController import StudentController
from App.view.studentCardUI import StudentCardUI
from App.controller.userController import getCurrentUser
from App.view.transferRoomUI import transferRoomUI

class HomeUI(QMainWindow):

    signal_desmarcarTurma = pyqtSignal(object)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        loadUi("App/view/ui/home.ui", self)
        self.show()

        self.currentUser = getCurrentUser()
        print(self.currentUser["tipo"])
        
        self.menuOpt = QMenu(self)

        if self.currentUser["tipo"] != "agente":
            self.createMenu()

        self.btnOptions.clicked.connect(self.showMenu)
        self.btnPesquisa.clicked.connect(self.searchStudentByName)
        self.barPesquisa.textChanged.connect(self.searchStudentByName)
        
        
        self.consultarTurmas()
        self.show()
 
    def createMenu(self):
        # can't click on other screens when menu is open, being necessary to click on the menu to close it before clicking on the screen
        self.menuOpt.setStyleSheet("""
            QMenu {
                background-color: #fff;
                color: #4A5DD6;
                border: 1.5px solid #D6DCF5;
                border-radius: 5px;
                margin: 2px;
                font-size: 14px;
                font-family: 'Segoe UI', 'SF Pro Text', sans-serif;
            }
            QMenu::item {
                background-color: transparent;
                padding: 5px 25px 5px 20px;
            }
            QMenu::item:selected {
                background-color: #5B6EE9;
                color: white;
            }
            QMenu::separator {
                height: 1px;
                background: #555;
                margin: 5px 10px;
            }""")
        action = [
            ("Nova turma", lambda : self.callEvent(RegisterClassUI, parent=self)),
            ("Cadastrar aluno", lambda : self.callEvent(RegisterStudentUI, parent=self)),
            ("Novo ano letivo", lambda : self.callEvent(transferRoomUI, parent=self)), # mudar para transferenciaUI
            ("Relatórios", lambda : self.callEvent(RegisterStudentUI, parent=self)), # mudar para relatoriosUI
            ("Cadastrar funcionário", lambda : self.callEvent(adminUI, parent=self)),
        ]

        if self.currentUser["tipo"] == "secretaria":
            action.pop()
        
        for texto, funcao in action:
            event = QAction(texto, self)
            event.triggered.connect(funcao)
            self.menuOpt.addAction(event)
            
    def callEvent(self, event, **kwargs):
        self.evento = event(**kwargs)
        if hasattr(self.evento, 'signal_IdRoom'):
            self.evento.signal_IdRoom.connect(self.consultarTurmas)
        self.evento.exec_()
            
    def showMenu(self):
        self.menuOpt.exec_(self.btnOptions.mapToGlobal(QPoint(0, self.btnOptions.height())))
        self.menuOpt.show()

        
    def consultarTurmas(self):
        self.clearStackCards(self.scrollAreaWidgetContents_2)
        todas_turmas = RoomController.getRoomByYear(2026)
        for turma in todas_turmas:
            card = ClassCardUI(turma, parent=self)
            card.signal_idDaTurma.connect(self.consultarAlunos)
            card.signal_idDaTurma.connect(self.desmarcarTurma)
            self.addCardInStackTurmas(card)

    def desmarcarTurma(self, idTurma):
        self.signal_desmarcarTurma.emit(idTurma)
    
    def consultarAlunos(self, idTurma):
        alunos = StudentController.getByRoomID(idTurma)
        
        self.populaStackAlunos(alunos)        

    def searchStudentByName(self):
        name = self.barPesquisa.text()
        alunos = StudentController.searchStudent(name)
        self.populaStackAlunos(alunos)
        
    
    def populaStackAlunos(self, alunos):
        self.clearStackCards(self.scrollAreaWidgetContentAlunos)
        
        try:
            for aluno in alunos:
                card = StudentCardUI(aluno)
                self.addCardInStackStudents(card)
        except Exception as e:
            self.scrollAreaWidgetContentAlunos.layout().addWidget(QLabel("Nenhum aluno encontrado nessa turma.", alignment=Qt.AlignCenter))
                    
    def addCardInStackTurmas(self, interface):
        self.scrollAreaWidgetContents_2.layout().addWidget(interface, alignment=Qt.AlignCenter)
    
    def addCardInStackStudents(self, interface):
        self.scrollAreaWidgetContentAlunos.layout().addWidget(interface)
    
    def clearStackCards(self, scrollArea):
        layout = scrollArea.layout()
        for i in range(layout.count()):
            layout.itemAt(i).widget().deleteLater()
    
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication([])
    home = HomeUI()
    app.exec_()
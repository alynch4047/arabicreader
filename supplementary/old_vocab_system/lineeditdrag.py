from qt import *
from constants import *

class lineeditdrag(QLineEdit):
    def __init__(self,a, name):
        QLineEdit.__init__(self,a,name)
        self.setAcceptDrops(True)
        self.setMouseTracking(False)
        self.name = name

    def mouseMoveEvent(self,e):
        global dragEvent
        text = self.text()
        self.emit(PYSIGNAL("startdrag"),(text,self.name))

    def dragEnterEvent(self,e):
        if str(self.text()) == '' or self.text() == None:
            e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self,e):
        #print repr(self.text()), str(self.text())
        if str(self.text()) == '' or self.text() == None:
            e.accept()
        else:
            e.ignore()
        
    def dropEvent(self,e):
        self.emit(PYSIGNAL("enddrag"),(e,self.name))
        

def main():
    import sys
    myApp = QApplication(sys.argv)

    myForm = lineeditdrag(None, "My data")
    myApp.setMainWidget(myForm)
    myForm.show()
    myApp.exec_loop()

if __name__ == '__main__':
    main()

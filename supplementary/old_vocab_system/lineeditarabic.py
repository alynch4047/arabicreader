from qt import *
from constants import *
import os


class lineeditarabic(QLineEdit):
    def __init__(self,a, name):
        QLineEdit.__init__(self,a,name)
        self.name = name

    def focusInEvent(self,e):
        QLineEdit.focusInEvent(self,e)
        os.system("dcop kxkb kxkb setLayout 'ar'")

    def focusOutEvent(self,e):
        QLineEdit.focusOutEvent(self,e)
        os.system("dcop kxkb kxkb setLayout 'us'")
        

def main():
    import sys
    myApp = QApplication(sys.argv)

    myForm = lineeditfocus(None, "My data")
    myApp.setMainWidget(myForm)
    myForm.show()
    myApp.exec_loop()

if __name__ == '__main__':
    main()

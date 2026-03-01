#! /usr/bin/env python
from qt import *
import sys
from mainentrysub import *

myApp = QApplication(sys.argv)

myForm = MainEntrySub(None, "My data")
myApp.setMainWidget(myForm)
myForm.show()
myApp.exec_loop()

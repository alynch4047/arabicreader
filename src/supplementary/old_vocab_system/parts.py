from kdecore import KCmdLineArgs, KURL, KApplication, i18n, KAboutData, BarIcon, KLibLoader, KShortcut

from kdeui import KMainWindow, KMessageBox, KAction, KStdAction, KKeyDialog, KEditToolbar

from qt import  QString, QStringList

from kio import KTrader

import kfile 

# Importing the KParts namespace gets us all of the KParts:: classes
from kparts import KParts, createReadOnlyPart, createReadWritePart

import sys, os

FALSE = 0
TRUE  = not FALSE

TOOLBAR_EXIT = 0
TOOLBAR_OPEN = 1

# Note that we use KParts.MainWindow, not KMainWindow as the superclass
# (KParts.MainWindow subclasses KMainWindow). Also, be sure the 'apply'
# clause references KParts.MainWindow - it's a hard bug to track down
# if it doesn't.

class pyPartsMW (KParts.MainWindow):
    def __init__ (self, *args):
        apply (KParts.MainWindow.__init__, (self,) + args)

        # Create the actions for our menu/toolbar to use
        # Keep in mind that the part loaded will provide its
        # own menu/toolbar entries

        # check out KParts.MainWindow's ancestry to see where
        # some of this and later stuff (like self.actionCollection () )
        # comes from

        quitAction = KStdAction.quit (self.close, self.actionCollection ())

        self.m_toolbarAction = KStdAction.showToolbar(self.optionsShowToolbar, self.actionCollection());
        self.m_statusbarAction = KStdAction.showStatusbar(self.optionsShowStatusbar, self.actionCollection());
        self.m_openFileAction = KStdAction.open(self.openFile, self.actionCollection())

        KStdAction.keyBindings(self.optionsConfigureKeys, self.actionCollection());
        KStdAction.configureToolbars(self.optionsConfigureToolbars, self.actionCollection());

        self.path = os.getcwd () + '/'
        self.setGeometry (0, 0, 600, 600)

        # point to our XML file
        self.setXMLFile (self.path + "parts.rc", FALSE)

        self.partArgs = QStringList()
        self.partArgs.append(QString("Browser/View"))

        print repr(self.partArgs)

        self.part = createReadOnlyPart ("libkghostviewpart", self,"gvpart","KParts::ReadOnlyPart",self.partArgs )

        # set the part as the main widget (you can use it in other
        # ways too)
        self.setCentralWidget (self.part.widget())

        # merge the menus/toolbars and display them
        # (comment this out to see what happens)
        self.createGUI (self.part)
        self.dynamicActions ()

        # load a file to view - this calls the part's openURL or openFile
        # This should be network transparent, so any URL for an image
        # should work here
        #self.myURL = KURL("file:/home/alynch/postscript/arabic-present-A.pdf")

        self.myURL = KURL("file:" + self.path + "psout.pdf")
        print str(self.myURL.fileName())
        self.part.openURL(self.myURL)
        print self.part.url()
        print self.part.url().path()
        

    def openFile(self):
        self.myFile = kfile.KFileDialog.getOpenFileName()
        self.myURL = KURL("file:" + str(self.myFile))
        print self.myURL.fileName()
        if self.part.openURL(self.myURL) == TRUE:
            print "opened"
        else:
            print "failed"


    # slots for our actions
    def optionsShowToolbar (self):
        if self.m_toolbarAction.isChecked():
                self.toolBar().show()
        else:
                self.toolBar().hide()

    def optionsShowStatusbar (self):
        if self.m_statusbarAction.isChecked ():
                self.statusBar().show()
        else:
                self.statusBar().hide()


    def optionsConfigureKeys (self):
        KKeyDialog.configureActionKeys (self.actionCollection(), self.xmlFile ())


    def optionsConfigureToolbars (self):
        dlg = KEditToolbar (self.actionCollection(), self.xmlFile ())
        if dlg.exec_loop ():
                self.createGUI(self);


    # some boilerplate left over from pyKLess/KLess
    def queryClose(self):
        return TRUE


    def queryExit(self):
            #// this slot is invoked in addition when the *last* window is going
            #// to be closed. We could do some final cleanup here.
        return TRUE #// accept

    # I'm not sure the session mgmt stuff here works

    # Session management: save data
    def saveProperties(self, config):
    # This is provided just as an example.
    # It is generally not so good to save the raw contents of an application
    # in its configuration file (as this example does).
    # It is preferable to save the contents in a file on the application's
    # data zone and save an URL to it in the configuration resource.
        config.writeEntry("text", self.edit.text())


    # Session management: read data again
    def readProperties(self, config):
    # See above
        self.edit.setText(config.readEntry("text"))

    def dynamicActions (self):
        fakeFiles = ["kaction.sip", "kxmlguiclient.sip"]
        self.unplugActionList("recent");
        self.dynamicActionsList = []
        for i in range (len (fakeFiles)):
            act = KAction (i18n (fakeFiles [i]), KShortcut.null (), None, fakeFiles [i][:-4] + "open")
            self.dynamicActionsList.append(act);

        for a in self.dynamicActionsList:
            print a.name ()
        print

        self.plugActionList("recent", self.dynamicActionsList);

    def slotFake (self, id = -1):
        pass



#------------- main ----------------------------

# A Human readable description of your program
description = "KParts - simple example"
# The version
version = "0.1"

# stuff for the "About" menu
aboutData = KAboutData ("pyParts", "pyParts",\
    version, description, KAboutData.License_GPL,\
    "(c) 2002, Jim Bublitz")

aboutData.addAuthor ("Jim Bublitz", "Example for PyKDE", "jbublitz@nwinternet.com")

# This MUST go here (before KApplication () is called)
KCmdLineArgs.init (sys.argv, aboutData)

app = KApplication ()

if (app.isRestored()):
        RESTORE(KLess)
else:
        # no session management: just create one window
        # this is our KParts::MainWindow derived class
        parts = pyPartsMW (None, "pyParts")
        if len(sys.argv) > 1:
        # read kcmdlineargs.h for the full unabridged instructions
        # on using KCmdLineArgs, it's pretty confusing at first, but it works
        # This is pretty useless in this program - you might want to
        # expand this in your app (to load a file, etc)
                args = KCmdLineArgs.parsedArgs()

parts.show()
app.exec_loop()

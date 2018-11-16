from PyQt5.QtCore import QFile, QRegExp, Qt, pyqtSignal
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QPalette, QColor 
from PyQt5.QtWidgets import (QApplication, QFileDialog, QMainWindow, QMenu,
							 QMessageBox, QTextEdit, QVBoxLayout, QWidget,
							 QStatusBar, QAction, QTabWidget)

from libs.Highlighter import Highlighter
from libs.Tabber import Tabber, Tab
from libs.CodeInput import CodeInput
import os

class MainWindow(QMainWindow):
	resized = pyqtSignal()
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)

		self.window = None
		self.toolBar = None
		self.tabber = None
		self.statusBar = None

		self.initUI()

	def initUI(self):
		self.window = QWidget()
		self.setCentralWidget(self.window)
		vBox = QVBoxLayout()
		self.setupTabber(self.window)
		self.setupFileMenu()
		self.setupRunMenu()
		self.setupHelpMenu()
		self.setupToolbar()
		self.setupStatusbar()
		self.updateWindowTitle()
		self.window.setLayout(vBox)
		self.tabber.currentChanged.connect(self.tabber.on_activeTab_changed)
		self.resized.connect(self.tabber.on_owner_resized)

	def resizeEvent(self, event):
		self.resized.emit()
		#return super(MainWindow, self).resizeEvent(event)

	def setupFileMenu(self):
		fileMenu = QMenu("&File", self)
		self.menuBar().addMenu(fileMenu)

		fileMenu.addAction("&New...", self.on_btnNew_pressed, "Ctrl+N")
		fileMenu.addAction("&Open...", self.on_btnOpen_pressed, "Ctrl+O")
		fileMenu.addAction("&Save...", self.on_btnSave_pressed, "Ctrl+S")
		fileMenu.addAction("&Save As...", self.on_btnSaveAs_pressed, "Ctrl+Shift+S")
		fileMenu.addAction("E&xit", QApplication.instance().quit, "Ctrl+Q")

	def setupRunMenu(self):
		runMenu = QMenu("&Run", self)
		self.menuBar().addMenu(runMenu)

		runMenu.addAction("&Run...", self.on_btnRun_pressed, "Ctrl+Shift+A")
		runMenu.addAction("&Compile...", self.on_btnCompile_pressed, "Ctrl+Shift+C")
		runMenu.addAction("&Compile and Run...", self.on_btnCompileRun_pressed, "Ctrl+X")

	def setupHelpMenu(self):
		helpMenu = QMenu("&Help", self)
		self.menuBar().addMenu(helpMenu)

		helpMenu.addAction("&About", self.on_btnAbout_pressed)
		helpMenu.addAction("About &Qt", QApplication.instance().aboutQt)

	def setupToolbar(self):
		self.toolBar = self.addToolBar("File")
		new = QAction("New", self)
		self.toolBar.addAction(new)
		new = QAction("Open", self)
		self.toolBar.addAction(new)
		new = QAction("Save", self)
		self.toolBar.addAction(new)
		new = QAction("Save As", self)
		self.toolBar.addAction(new)
		new = QAction("Compile", self)
		self.toolBar.addAction(new)
		new = QAction("Run", self)
		self.toolBar.addAction(new)
		self.toolBar.actionTriggered[QAction].connect(self.onToolBtnPressed)

	def setupStatusbar(self):
		self.statusBar = QStatusBar()
		self.setStatusBar(self.statusBar)

	def setupTabber(self, owner):
		self.tabber = Tabber(owner)

	def setupEditor(self, owner):
		self.editor = CodeInput(owner)

	def onToolBtnPressed(self, sender):
		toolBtn = sender.text()
		if toolBtn == "New":
			self.on_btnNew_pressed()
		elif toolBtn == "Open":
			self.on_btnOpen_pressed()
		elif toolBtn == "Save":
			self.on_btnSave_pressed()
		elif toolBtn == "Save As":
			self.on_btnSaveAs_pressed()
		elif toolBtn == "Compile":
			self.on_btnCompile_pressed()
		elif toolBtn == "Run":
			self.on_btnRun_pressed()

	def on_btnNew_pressed(self, name="*new*"):
		if not self.tabber.tabNameExistsByName(name):
			tab = self.tabber.addNewTab(name, QVBoxLayout())
			codeInput = CodeInput(tab.layout)
			self.tabber.setActiveTabByTab(tab)
		else:
			self.tabber.setActiveTabByName(name)

	def on_btnOpen_pressed(self):
		tab = self.tabber.addNewTab("", QVBoxLayout())
		codeInput = CodeInput(tab.layout)
		filePath = codeInput.openFile()
		if not filePath:
			self.tabber.on_tab_close(self.tabber.count()-1)
		else:
			fileName = os.path.basename(filePath)
			filePath = filePath.replace(fileName, "")
			if self.tabber.tabNameExistsByName(fileName):
				self.tabber.on_tab_close(self.tabber.count()-1)
				self.tabber.setActiveTabByName(fileName)
			else:
				self.tabber.setTabName(self.tabber.count()-1, fileName)
				self.tabber.setActiveTabByTab(tab)

	def on_btnSave_pressed(self):
		activeTab = self.tabber.activeTab()
		if activeTab:
			editor = activeTab.layout.itemAt(0).widget()
			if editor:
				filePath = editor.saveFile()# <------------
				if filePath:
					fileName = os.path.basename(filePath)
					filePath = filePath.replace(fileName, "")
					self.tabber.changeTabNameByTab(activeTab, fileName)

	def on_btnSaveAs_pressed(self):
		activeTab = self.tabber.activeTab()
		if activeTab:
			editor = activeTab.layout.itemAt(0).widget()
			if editor:
				filePath = editor.saveFileAs()# <------------
				if filePath:
					fileName = os.path.basename(filePath)
					filePath = filePath.replace(fileName, "")
					self.tabber.changeTabNameByTab(activeTab, fileName)
				


	def on_btnCompile_pressed(self):
		pass

	def on_btnRun_pressed(self):
		self.tabber.debugTabNames()
		pass

	def on_btnCompileRun_pressed(self):
		pass

	def on_btnAbout_pressed(self):
		pass


	def updateWindowTitle(self, addString=""):
		pass
		#self.setWindowTitle("VisualFASM     FILE:"+addString+"[ "+os.path.basename(self.openedFile)+" ]"+addString)


	def about(self):
		QMessageBox.about(self, "About VisualFASM",
				"<p> <b>VisualFASM</b> \nis a simple Editor " \
				"for the Flat Assembler assembly language. \n" \
				"Copyright (c) by Michael Binder</p>")

	# not used 
	def runShellCommand(self, command):
		process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
		while True:
			line = process.stdout.readline().rstrip()
			if not line:
				break
			yield line



if __name__ == "__main__":

	import sys

	app = QApplication(sys.argv)
	app.setStyle('Fusion')
	palette = QPalette()
	palette.setColor(QPalette.Window, QColor(53,53,53))
	palette.setColor(QPalette.WindowText, Qt.white)
	palette.setColor(QPalette.Base, QColor(40,42,40))
	palette.setColor(QPalette.AlternateBase, QColor(53,53,53))
	palette.setColor(QPalette.ToolTipBase, Qt.white)
	palette.setColor(QPalette.ToolTipText, Qt.white)
	palette.setColor(QPalette.Text, QColor(216,216,216))
	palette.setColor(QPalette.Button, QColor(53,53,53))
	palette.setColor(QPalette.ButtonText, Qt.white)
	palette.setColor(QPalette.BrightText, Qt.red)
		 
	palette.setColor(QPalette.Highlight, QColor(40,120,100).lighter())
	palette.setColor(QPalette.HighlightedText, Qt.black)
	app.setPalette(palette)
	window = MainWindow()
	window.resize(640, 512)
	window.show()
	sys.exit(app.exec_())

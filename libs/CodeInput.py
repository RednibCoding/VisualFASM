from PyQt5.QtCore import QFile, QRegExp, Qt, pyqtSignal
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QPalette, QColor 
from PyQt5.QtWidgets import (QApplication, QFileDialog, QMainWindow, QMenu,
							 QMessageBox, QTextEdit, QVBoxLayout, QWidget,
							 QStatusBar, QAction, QTabWidget)

from libs.Highlighter import Highlighter
import os

class CodeInput(QTextEdit):
	def __init__(self, owner, ratio=5):
		super(CodeInput, self).__init__()
		font = QFont()
		font.setFamily("Consolas")
		font.setFixedPitch(True)
		font.setPointSize(11)
		self.owner = owner

		self.myFile = ""

		self.setLineWrapMode(0) # no wrap
		self.setFont(font)
		self.textChanged.connect(self.onTextChanged)
		self.mouseReleaseEvent = self.onMouseReleaseEvent

		self.highlighter = Highlighter(parent=self.document())

		owner.addWidget(self, ratio)

	def onTextChanged(self):
		cursor = self.textCursor()
		self.cursorX = cursor.columnNumber()+1;
		self.cursorY = cursor.blockNumber()+1;
		print("Line: "+str(self.cursorY) + ", Column " + str(self.cursorX))
		#self.owner.statusBar.showMessage("Line: "+str(self.cursorY) + ", Column " + str(self.cursorX))

	def onMouseReleaseEvent(self, event):
		pos = event.pos()
		cursor = self.cursorForPosition(pos)
		self.cursorX = cursor.columnNumber()+1;
		self.cursorY = cursor.blockNumber()+1;
		print("Line: "+str(self.cursorY) + ", Column " + str(self.cursorX))
		#self.owner.statusBar.showMessage("Line: "+str(self.cursorY) + ", Column " + str(self.cursorX))

	def newFile(self):
		#newTab = self.tabber.addNewTab("New", QVBoxLayout())
		#self.setupEditor(newTab.layout, 4)
		pass

	def openFile(self, path=None):
		if not path:
			path, _ = QFileDialog.getOpenFileName(self, "Open File", '',
					"ASM Files (*.asm *.inc)")
			if not path:
				return ""
		if path:
			inFile = QFile(path)
			if inFile.open(QFile.ReadOnly | QFile.Text):
				text = inFile.readAll()

				try:
					# Python v3.
					text = str(text, encoding='ascii')
				except TypeError:
					# Python v2.
					text = str(text)

				self.setPlainText(text)
				self.myFile = path
				return self.myFile

	def saveFile(self):
		if self.myFile != "":
			with open(self.myFile, "w") as asmFile:
				text = self.toPlainText()
				asmFile.write(text)
			return ""
		else:
			self.saveFileAs()
			return self.myFile

	def saveFileAs(self):
		path, _ = QFileDialog.getSaveFileName(self, "Save File", '',
				"ASM Files (*.asm)")
		if path:
			with open(path, "w") as asmFile:
				text = self.toPlainText()
				asmFile.write(text)
			self.myFile = path
			return self.myFile
		else:
			return ""

	def compileFile(self):
		if self.myFile:
			os.system("fasm "+self.myFile+ " "+ self.myFile + ".exe")

	def runFile(self):
		if self.myFile:
			os.system(self.myFile+".exe")

	def compileAndRun(self):
		self.compileFile()
		self.runFile()
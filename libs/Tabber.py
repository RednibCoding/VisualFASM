from PyQt5.QtCore import QFile, QRegExp, Qt
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QPalette, QColor 
from PyQt5.QtWidgets import (QApplication, QFileDialog, QMainWindow, QMenu,
							 QMessageBox, QTextEdit, QVBoxLayout, QWidget,
							 QStatusBar, QAction, QTabWidget)

class Tabber(QTabWidget):
	def __init__(self, owner):
		super(Tabber, self).__init__(owner)
		self.owner = owner
		self.resize(owner.frameGeometry().width(), owner.frameGeometry().height()-50)
		self.setMovable(True)
		self.setTabsClosable(True)
		self.setTabShape(0) # 0 Rounded / 1 Triangular
		self.tabs = []
		self.tabCloseRequested.connect(self.on_tab_close)


	def on_activeTab_changed(self, index):
		self.resize(self.owner.frameGeometry().width(), self.owner.frameGeometry().height())

	def on_owner_resized(self):
		self.resize(self.owner.frameGeometry().width(), self.owner.frameGeometry().height())

	def on_tab_close(self, widgetIndex):
		tab = self.getTabByWidgetIndex(widgetIndex)
		self.closeTabByTab(tab)

	def closeTabByTab(self, tab):
		widgetIndex = self.getWidgetIndexByTab(tab)
		self.delTabByName(tab.name)
		self.removeTab(widgetIndex)

	def closeTabByName(self, name):
		tab = self.getTabByName(name)
		widgetIndex = self.getWidgetIndexByTab(tab)
		self.delTabByName(tab.name)
		self.removeTab(widgetIndex)

	def addNewTab(self, name, tabLayout):
		self.tabs.append(Tab(name, tabLayout))
		self.evaluateTabName(self.last())
		self.addTab(self.last(), self.last().name)
		return self.last()

	def last(self):
		if self.tabs:
			return self.tabs[-1]

	def evaluateTabName(self, tab):
		while self.tabNameExistsByTab(tab):
			self.appendNamePrefix(tab, "_")

	def tabNameExistsByTab(self, tab):
		for tmpTab in self.tabs:
			if not tmpTab == tab:
				if tmpTab.name == tab.name:
					return True
		return False

	def tabNameExistsByName(self, name):
		for tmpTab in self.tabs:
			if tmpTab.name == name:
				return True
		return False

	def appendNamePrefix(self, tab, prefix):
		tab.name = prefix + tab.name

	def getTabByName(self, name):
		for tab in self.tabs:
			if tab.name == name:
				return tab

	def getTabByWidgetIndex(self, index):
		tabWidget = self.widget(index)
		for tab in self.tabs:
			if tab == tabWidget:
				return tab

	def delTabByName(self, name):
		self.tabs = [tab for tab in self.tabs if tab.name != name]

	def setTabName(self, index, name):
		tab = self.getTabByWidgetIndex(index)
		tab.setName(name)
		self.evaluateTabName(tab)
		self.setTabText(index, tab.name)

	def changeTabNameByTab(self, tab, newName):
		if tab.name == newName:
			return
		if self.tabNameExistsByName(newName):
			oldTab = self.getTabByName(newName)
			self.closeTabByTab(oldTab)
			widgetIndex = self.getWidgetIndexByTab(tab)
			print(widgetIndex, newName)
			self.setTabName(widgetIndex, newName)
		else:
			widgetIndex = self.getWidgetIndexByTab(tab)
			self.setTabName(widgetIndex, newName)


	def getWidgetIndexByTab(self, tab):
		for i in range(0, self.count()):
			tabWidgetText = self.tabText(i)
			if tabWidgetText == tab.name:
				return i

	def getWidgetIndexByName(self, name):
		for i in range(0, self.count()):
			tabWidgetText = self.tabText(i)
			if tabWidgetText == name:
				return i

	def setActiveTabByTab(self, tab):
		widgetIndex = self.getWidgetIndexByTab(tab)
		self.setCurrentIndex(widgetIndex)

	def setActiveTabByName(self, name):
		widgetIndex = self.getWidgetIndexByName(name)
		self.setCurrentIndex(widgetIndex)

	def activeTab(self):
		current = self.currentIndex()
		tab = self.getTabByWidgetIndex(current)
		return tab

	def activeTabIndex(self):
		return self.currentIndex()

	def debugTabNames(self):
		print("---- Debug Tab Names: ----")
		for tab in self.tabs:
			print(tab.name)
		print("--------------------------")


class Tab(QWidget):
	def __init__(self, name, tabLayout):
		super(Tab, self).__init__()
		self.name = name
		self.layout = tabLayout
		self.setLayout(self.layout)

	def setName(self, name):
		self.name = name

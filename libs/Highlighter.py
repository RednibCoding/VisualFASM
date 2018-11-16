
# Class for Highlighting source code
#
# "parent" must be a QTextEdit().document()


from PyQt5.QtCore import QFile, QRegExp, Qt
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QColor
from PyQt5.QtWidgets import (QApplication, QFileDialog, QMainWindow, QMenu,
							 QMessageBox, QTextEdit)


class Highlighter(QSyntaxHighlighter):

	def __init__(self, parent=None):
		super(Highlighter, self).__init__(parent)

		self.useMultilineComments = False

		keywordPatterns = self.readKeywords("cfg/keywords.ini")
		commentPatterns = self.readCommentSymbols("cfg/commentSymbols.ini")

		if len(commentPatterns) > 1 and len(commentPatterns) <= 3:
			self.useMultilineComments = True

		# Keywords
		keywordsFormat = QTextCharFormat()
		keywordsFormat.setFontWeight(QFont.Bold)
		keywordsFormat.setForeground(QColor(60,180,160))
		self.highlightingRules = [(QRegExp(pattern), keywordsFormat)
								  for pattern in keywordPatterns]
		self.highlightingRules.append((QRegExp("\\bQ[A-Za-z]+\\b"), keywordsFormat))

		# Singleline Comments
		singleLineCommentFormat = QTextCharFormat()
		singleLineCommentFormat.setForeground(QColor(120,120,120))
		self.highlightingRules.append((QRegExp(commentPatterns[0]+"[^\n]*"), singleLineCommentFormat))
		# Multiline Comments
		if self.useMultilineComments:
			self.multiLineCommentFormat = QTextCharFormat()
			self.multiLineCommentFormat.setForeground(Qt.red)
			self.commentStartExpression = QRegExp(commentPatterns[1])
			self.commentEndExpression = QRegExp(commentPatterns[2])
		# Strings
		quotationFormat = QTextCharFormat()
		quotationFormat.setForeground(QColor(240,160,0))
		self.highlightingRules.append((QRegExp("\".*\""), quotationFormat))
		self.highlightingRules.append((QRegExp("\'.*\'"), quotationFormat))

	def readKeywords(self, file):
		if file:
			inFile = QFile(file)
			with open(file, "r") as keywordFile:
				text = keywordFile.read()
				kwList = text.split("\n")
				# remove empties
				kwList = [val for val in kwList if val != ""]
				# format keywords for QHighlighter
				kwList = [self.formatTokens(kw) for kw in kwList]
				return kwList

	def readCommentSymbols(self, file):
		if file:
			inFile = QFile(file)
			with open(file, "r") as commentFile:
				text = commentFile.read()
				commentList = text.split("\n")
				# remove empties
				commentList = [val for val in commentList if val != ""]
				return commentList

	def formatTokens(self, keyword):
		keyword = "\\b" + keyword + "\\b"
		return keyword

	def highlightBlock(self, text):
		for pattern, format in self.highlightingRules:
			expression = QRegExp(pattern)
			index = expression.indexIn(text)
			while index >= 0:
				length = expression.matchedLength()
				self.setFormat(index, length, format)
				index = expression.indexIn(text, index + length)

		self.setCurrentBlockState(0)
		if self.useMultilineComments:
			startIndex = 0
			if self.previousBlockState() != 1:
				startIndex = self.commentStartExpression.indexIn(text)

			while startIndex >= 0:
				endIndex = self.commentEndExpression.indexIn(text, startIndex)

				if endIndex == -1:
					self.setCurrentBlockState(1)
					commentLength = len(text) - startIndex
				else:
					commentLength = endIndex - startIndex + self.commentEndExpression.matchedLength()

				self.setFormat(startIndex, commentLength,
						self.multiLineCommentFormat)
				startIndex = self.commentStartExpression.indexIn(text,
						startIndex + commentLength);

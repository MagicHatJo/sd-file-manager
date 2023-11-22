import logging
import logging.handlers

from PyQt5.QtWidgets import QWidget, QDialog, QVBoxLayout, QTextBrowser

class LogWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Log")
		self.resize(400, 400)
		
		# GUI
		self.text_browser = QTextBrowser(self)
		self.text_browser.setReadOnly(True)

		layout = QVBoxLayout(self)
		layout.addWidget(self.text_browser)

		self.setLayout(layout)

		# Logging
		logging.root.addFilter(self.handler)

	def handler(self, record):
		'''
		Handles displaying the message logged
		'''
		self.text_browser.append(record.levelname + ":" + record.getMessage())
		return True

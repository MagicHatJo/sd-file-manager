import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMenuBar, QAction
from PyQt5.QtCore import Qt

from app.gui.widgets import DropboxWidget, FileDetailsWidget
from app.gui.config import ConfigWindow

class FileManager(QMainWindow):
	'''
	Main window manager.
	Event handler.
	'''
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Stable Diffusion File Manager")
		self.resize(500, 600)
		self.setAcceptDrops(True)

		# Menu Bar
		self.menu = self.menuBar()

		action_config = QAction("Config", self)
		action_config.triggered.connect(self.action_config)
		self.menu.addAction(action_config)

		# Content
		self.widget_dropbox = DropboxWidget()
		self.widget_details = FileDetailsWidget()
		self.setCentralWidget(self.widget_dropbox)

	# Event Handler
	def dragEnterEvent(self, event):
		if event.mimeData().hasUrls():
			event.accept()
		else:
			event.ignore()

	def dragMoveEvent(self, event):
		if event.mimeData().hasUrls():
			event.accept()
		else:
			event.ignore()

	def dropEvent(self, event):
		if event.mimeData().hasUrls():
			event.setDropAction(Qt.CopyAction)
			try:
				# TODO file validation
				print("Loading in a file")
				self.widget_details.load_file(event.mimeData().urls()[0].toLocalFile())
				self.setCentralWidget(self.widget_details)
			except:
				print("Failed to load file")
				self.setCentralWidget(self.widget_dropbox)
			event.accept()
		else:
			event.ignore()
	
	# Menu Bar

	# Config
	def action_config(self):
		config_window = ConfigWindow()
		result = config_window.exec_()
		if result == QDialog.Accepted:
			print("Save successfull")
		else:
			print("Did not save")
import os
import logging

from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMenuBar, QAction
from PyQt5.QtCore    import Qt

from app.gui.widgets import DropboxWidget, FileDetailsWidget
from app.gui.windows import LogWindow
from app.gui.config  import ConfigWindow

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

		# Windows
		self.log_window = LogWindow()

		# Menu Bar
		self.menu = self.menuBar()

		action_config = QAction("Config", self)
		action_config.triggered.connect(self.action_config)
		self.menu.addAction(action_config)

		action_log = QAction("Log", self)
		action_log.triggered.connect(self.action_log)
		self.menu.addAction(action_log)

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
				self.widget_details.load_file(event.mimeData().urls()[0].toLocalFile())
				self.setCentralWidget(self.widget_details)
				logging.info(f"Loaded {event.mimeData().urls()[0].toLocalFile()}")
			except:
				self.setCentralWidget(self.widget_dropbox)
				logging.error(f"Failed to load {event.mimeData().urls()[0].toLocalFile()}")
			event.accept()
		else:
			event.ignore()
	
	########## Menu Bar ##########
	def action_config(self):
		config_window = ConfigWindow()
		result = config_window.exec_()
		if result == QDialog.Accepted:
			logging.info("Saved configuration")
		else:
			logging.error("Could not save configuration")
	
	def action_log(self):
		self.log_window.show()
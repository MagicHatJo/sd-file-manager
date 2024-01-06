import os
import logging

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QMenuBar, QAction, QVBoxLayout
from PyQt5.QtCore    import Qt

from app.gui.widgets import DropboxWidget, FileDetailsWidget
from app.gui.windows import LogWindow, ConfigWindow

class FileManager(QMainWindow):
	'''
	Main window manager.
	Event handler.
	'''
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Stable Diffusion File Manager")
		self.resize(500, 600)

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

		self.widget_dropbox.load = self.widget_details.load_file
		
		self.layout = QVBoxLayout()
		self.layout.addWidget(self.widget_dropbox)
		self.layout.addWidget(self.widget_details)

		self.central_widget = QWidget(self)
		self.central_widget.setLayout(self.layout)
		self.setCentralWidget(self.central_widget)
	
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
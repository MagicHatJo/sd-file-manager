import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QAction
from PyQt5.QtCore import Qt

from app.gui.widgets import EmptyWidget, FileDetailsWidget

class FileManager(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Stable Diffusion File Manager")
		self.resize(400, 600)
		self.setAcceptDrops(True)

		# Content
		self.widget_empty   = EmptyWidget()
		self.widget_details = FileDetailsWidget()
		self.setCentralWidget(self.widget_empty)

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
			self.widget_details.load_file(event.mimeData().urls()[0].toLocalFile())
			self.setCentralWidget(self.widget_details)
			event.accept()
		else:
			event.ignore()
import logging

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class DropboxWidget(QWidget):
	# TODO have this display associated files (image moving, json?)
	'''
	Widget that recieves drag and drop files.
	self.load should be initialized to a function that connects the file path.
	'''
	def __init__(self):
		super().__init__()
		self.setAcceptDrops(True)
		self.layout = QVBoxLayout()
		self.label  = QLabel(self)
		self.load   = None
		self._init_layout()

	def load_file(self, file_name):
		self.load(file_name)
		self.label.setText(f"\n\n {file_name} \n\n")

	def _init_layout(self):
		self.label.setAlignment(Qt.AlignCenter)
		self.label.setText('\n\n Drop File Here \n\n')
		self.label.setStyleSheet(
			'''
			QLabel{
				border: 4px dashed #aaa
			}
			'''
		)

		self.layout.addWidget(self.label)
		self.setLayout(self.layout)
	
	########## Event Handler ##########
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
				self.load_file(event.mimeData().urls()[0].toLocalFile())
				logging.info(f"Loaded {event.mimeData().urls()[0].toLocalFile()}")
			except:
				logging.error(f"Failed to load {event.mimeData().urls()[0].toLocalFile()}")
			event.accept()
		else:
			event.ignore()
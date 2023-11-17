
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class DropboxWidget(QWidget):
	# TODO make this a dedicated spot for dropping data.
	# have this display the original file path
	# have this display asdsociated files (image moving, json?)
	'''
	Placeholder widget for no file loaded.
	Should not interact with data.
	'''
	def __init__(self):
		super().__init__()
		self.layout = QVBoxLayout()

		self.label = QLabel(self)
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
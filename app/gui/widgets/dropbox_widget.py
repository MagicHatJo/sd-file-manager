
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class DropboxWidget(QWidget):
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
		self.label.setStyleSheet('''
			QLabel{
				border: 4px dashed #aaa
			}
		''')

		self.layout.addWidget(self.label)
		self.setLayout(self.layout)
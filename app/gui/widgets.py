import os

from PyQt5.QtWidgets import (
	QWidget,
	QVBoxLayout, QHBoxLayout,
	QLabel, QPushButton,
	QLineEdit, QTextEdit
)
from PyQt5.QtCore import Qt

from app.util.widget_helpers import new_widget, new_button, get_edit_text, clear_layout
from app.util import config

class EmptyWidget(QWidget):
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

class FileDetailsWidget(QWidget):
	'''
	Widget handling file data.
	'''
	def __init__(self):
		super().__init__()

		self.config = config.load()
		
		self.file_path = None
		self.file_name = None

		self.data = self._init_data()
		self.layout = self._init_layout()

		self.setLayout(self.layout)

	def load_file(self, file_path):
		def set_text(key, value=""):
			if value != "" or key not in self.config:
				self.data[key].setText(value)
			elif not self.config[key].get("remember_last", False):
				self.data[key].setText(self.config[key].get("default", value))
					
		self.file_path = file_path
		self.file_name = os.path.basename(self.file_path)
		
		for key in self.data:
			# Future proofing
			match key:
				case "Model Name":
					set_text("Model Name", self.file_name)
				case _:
					set_text(key)
	
	def button_save(self):
		# TODO customize save path
		destination_path = os.path.join(
			self.config["default_path"],
			get_edit_text(self.data["Model Type"], QLineEdit),
			get_edit_text(self.data["SD Version"], QLineEdit),
			get_edit_text(self.data["Category"], QLineEdit)
		)
		destination_file = get_edit_text(self.data["Model Name"], QLineEdit) + os.path.splitext(self.file_path)[1]

		if not os.path.exists(destination_path):
			os.makedirs(destination_path)

		os.rename(self.file_path, os.path.join(destination_path, destination_file))

		data = {
			"original name"    : self.file_name,
			"id"               : get_edit_text(self.data["Model ID"], QLineEdit),
			"description"      : get_edit_text(self.data["Description"], QTextEdit),
			"sd version"       : get_edit_text(self.data["SD Version"], QLineEdit),
			"activation text"  : get_edit_text(self.data["Activation"], QLineEdit),
			"preferred weight" : get_edit_text(self.data["Weight"], QLineEdit),
			"notes"            : get_edit_text(self.data["Notes"], QTextEdit)
		}

		with open(os.path.join(destination_path, os.path.splitext(destination_file)[0] + ".json"), 'w') as f:
			json.dump(data, f, indent=4)

	def _init_data(self):
		return {
			"Model Name"  : QLineEdit(),
			"Model Type"  : QLineEdit(),
			"Category"    : QLineEdit(),
			"Model ID"    : QLineEdit(),
			"Description" : QTextEdit(),
			"SD Version"  : QLineEdit(),
			"Activation"  : QLineEdit(),
			"Weight"      : QLineEdit(),
			"Notes"       : QTextEdit()
		}

	def _init_layout(self):
		layout = QVBoxLayout()
		
		for label, data in self.data.items():
			layout.addWidget(new_widget(label, data))

		layout.addWidget(new_button("Save", self.button_save))

		return layout
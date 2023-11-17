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
	def __init__(self):
		super().__init__()

		self.config = config.load()
		
		self.file_path = None
		self.file_name = None
		self.layout = QVBoxLayout()
		self.setLayout(self.layout)

		self.previous_data = {}

	def load_file(self, file_path):
		self.file_path = file_path
		self.file_name = os.path.basename(self.file_path)
		
		clear_layout(self.layout)
		self._setup_layout()
	
	def button_save(self):
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

		# Previous data used for "remember last" setting
		self.previous_data = {
			"model type": get_edit_text(self.data["Model Type"], QLineEdit),
			"category"  : get_edit_text(self.data["Category"], QLineEdit),
			"sd_version": get_edit_text(self.data["SD Version"], QLineEdit),
			"preferred_weight": get_edit_text(self.data["Weight"], QLineEdit)
		}

		with open(os.path.join(destination_path, os.path.splitext(destination_file)[0] + ".json"), 'w') as f:
			json.dump(data, f, indent=4)
	
	def _setup_layout(self):

		self.data = {
			"Model Name"  : new_widget("Model Name", QLineEdit, os.path.splitext(self.file_name)[0]),
			"Model Type"  : new_widget("Model Type", QLineEdit, "Lora"),
			"Category"    : new_widget("Category", QLineEdit),
			"Model ID"    : new_widget("Model ID", QLineEdit),
			"Description" : new_widget("Description", QTextEdit),
			"SD Version"  : new_widget("SD Version", QLineEdit, "1.5"),
			"Activation"  : new_widget("Activation Text", QLineEdit),
			"Weight"      : new_widget("Preferred Weight", QLineEdit, "1"),
			"Notes"       : new_widget("Notes", QTextEdit)
		}

		# Category
		self.layout.addWidget(self.data["Model Name"])
		self.layout.addWidget(self.data["Model Type"])
		self.layout.addWidget(self.data["Category"])

		# Data
		self.layout.addWidget(self.data["Model ID"])
		self.layout.addWidget(self.data["Description"])
		self.layout.addWidget(self.data["SD Version"])
		self.layout.addWidget(self.data["Activation"])
		self.layout.addWidget(self.data["Weight"])
		self.layout.addWidget(self.data["Notes"])

		# Finish
		self.layout.addWidget(new_button("Save", self.button_save))
import os
import json

from PyQt5.QtWidgets import (
	QWidget,
	QVBoxLayout, QHBoxLayout,
	QLabel, QPushButton,
	QLineEdit, QTextEdit
)
from PyQt5.QtCore import Qt

from app.util.widget_helpers import new_widget, new_button, get_text, clear_layout
from app.util import config

class FileDetailsWidget(QWidget):
	'''
	Widget handling file data.
	'''
	def __init__(self):
		super().__init__()

		self.config = config.load()
		
		self.file_path = ""
		self.file_name = ""
		self.origin_path_display = QLabel()

		self.destination_path    = ""
		self.destination_display = QLineEdit()

		self.data   = self._init_data()
		self.layout = self._init_layout()

		self.setLayout(self.layout)

	########## File Handlers ##########
	def load_file(self, file_path):
		'''
		Connects to new file event.
		Manages population of default values in data.
		'''
		# TODO Open loaded file
		# Read auto fill info

		self.file_path = file_path
		self.origin_path_display.setText(self.file_path)
		self.file_name, self.file_extension = os.path.splitext(os.path.basename(file_path))
		print(f"File Name: {self.file_name}")
		
		for key in self.data:
			# Future proofing
			match key:
				case "Model Name":
					self._set_text("Model Name", self.file_name)
				case _:
					self._set_text(key)
	
	def save_file(self):
		'''
		Connects to Save button.
		Manages file saving.
		'''
		if not os.path.exists(self.destination_path):
			os.makedirs(self.destination_path)

		os.rename(self.file_path, get_text(self.destination_display))

		# Create output format
		data = {
			"original name"    : self.file_name,
			"id"               : get_text(self.data["Model ID"]),
			"description"      : get_text(self.data["Description"]),
			"sd version"       : get_text(self.data["SD Version"]),
			"activation text"  : get_text(self.data["Activation"]),
			"preferred weight" : get_text(self.data["Weight"]),
			"notes"            : get_text(self.data["Notes"])
		}

		# Save to destination
		with open(get_text(self.destination_display).replace(self.file_extension, ".json"), 'w') as f:
			json.dump(data, f, indent=4)

	########## Constructors ##########
	def _init_data(self):
		'''
		Helper function to initialize GUI data.
		Should only be used once on construction.
		'''
		data = {
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

		# TODO make this dynamic based on configuration path options
		data["Model Name"].textChanged.connect(self._update_destination_path)
		data["Model Type"].textChanged.connect(self._update_destination_path)
		data["Category"  ].textChanged.connect(self._update_destination_path)
		data["Model ID"  ].textChanged.connect(self._update_destination_path)
		data["SD Version"].textChanged.connect(self._update_destination_path)

		return data

	def _init_layout(self):
		'''
		Helper function to initialize GUI Layout.
		Should only be used once on construction.
		'''
		layout = QVBoxLayout()

		layout.addWidget(new_widget("From: ", self.origin_path_display))
		layout.addWidget(new_widget("To: "  , self.destination_display))

		for label, data in self.data.items():
			layout.addWidget(new_widget(label, data))

		layout.addWidget(new_button("Save", self.save_file))

		return layout
	
	########## Data Managers ##########
	def _set_text(self, key, value=""):
		'''
		Sets text on load.
		'''
		if value != "" or key not in self.config:
			self.data[key].setText(value)
		elif not self.config[key].get("remember_last", False):
			self.data[key].setText(self.config[key].get("default", value))
	
	def _update_destination_path(self):
		'''
		Connects to data.
		Event handler for changes to data relevant to destination path.
		Updates destination display.
		'''
		# TODO make this not hardcoded.
		self.destination_path = os.path.join(
			self.config["default_path"],
			get_text(self.data["Model Type"]),
			get_text(self.data["SD Version"]),
			get_text(self.data["Category"])
		)

		self.destination_display.setText(os.path.join(
			self.destination_path,
			get_text(self.data["Model Name"]) + self.file_extension
		))
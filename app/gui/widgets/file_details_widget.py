import os
import json
import shutil

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt

from app.util.widget_helpers import QGeneric, new_button
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
		self.file_extension = ""

		self.data   = {}
		self.layout = QVBoxLayout()
		self._init_data()

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
		self.file_name, self.file_extension = os.path.splitext(os.path.basename(file_path))
		
		for key in self.data:
			self._set_text(key)
		self.data["Model Name"].text = self.file_name

		self._update_destination_path()
	
	def save_file(self):
		'''
		Connects to Save button.
		Manages file saving.
		'''
		# Create output format
		data = {
			"original name"    : self.file_name,
			"id"               : self.data["Model ID"].text,
			"description"      : self.data["Description"].text,
			"sd version"       : self.data["SD Version"].text,
			"activation text"  : self.data["Activation"].text,
			"preferred weight" : self.data["Weight"].text,
			"notes"            : self.data["Notes"].text
		}
		# TODO error handle this part
		# TODO add image moving here
		# Ensure destination path
		dir = os.path.dirname(self.data["Path"].text)
		if not os.path.exists(dir):
			os.makedirs(dir)

		# Move file
		shutil.move(self.file_path, self.data["Path"].text)

		# Create json
		with open(self.data["Path"].text.replace(self.file_extension, ".json"), 'w') as f:
			json.dump(data, f, indent=4)

	########## Constructors ##########
	def _init_data(self):
		'''
		Helper function to initialize GUI data.
		Should only be used once on construction.
		'''
		self._load_parameters()
		self._load_defaults()
		self._connect_destination_paths(self.data)

	def _load_parameters(self):
		'''
		Initializes GUI data and layout.
		These must be done concurrently due to limitations with accessing
		different QObjects.
		data   - contains QObjects
		layout - contains wrapped objects
		'''
		
		for label, table in self.config["layout"].items():
			self.data[label] = QGeneric(label, table)
			self.layout.addWidget(self.data[label].widget)
		
		self.layout.addWidget(new_button("Save", self.save_file))
	
	def _load_defaults(self):
		'''
		Loads default data into GUI.
		'''
		for label, q in self.data.items():
			q.text = self.config["layout"][label].get("default", "")
			
	def _connect_destination_paths(self, data):
		# TODO make this dynamic based on configuration path options
		data["Model Name"].connect(self._update_destination_path)
		data["Model Type"].connect(self._update_destination_path)
		data["Category"  ].connect(self._update_destination_path)
		data["Model ID"  ].connect(self._update_destination_path)
		data["SD Version"].connect(self._update_destination_path)
	
	########## Data Managers ##########
	def _set_text(self, key, value=""):
		'''
		Sets text on load.
		'''
		if value != "" or key not in self.config["layout"]:
			self.data[key].text = value
		elif not self.config["layout"][key].get("remember_last", False):
			self.data[key].text = self.config["layout"][key].get("default", value)

	def _update_destination_path(self):
		'''
		Connects to data.
		Event handler for changes to data relevant to destination path.
		Updates destination display.
		'''
		# TODO make this not hardcoded.
		path = os.path.join(
			self.config["default_path"],
			self.data["Model Type"].text,
			self.data["SD Version"].text,
			self.data["Category"].text
		)

		self.data["Path"].text = os.path.join(
			path,
			self.data["Model Name"].text + self.file_extension
		)
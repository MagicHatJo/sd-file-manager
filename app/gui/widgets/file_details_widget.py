import os
import json
import shutil

from PyQt5.QtWidgets import (
	QWidget,
	QVBoxLayout, QHBoxLayout,
	QLabel, QPushButton,QButtonGroup, QRadioButton,
	QLineEdit, QTextEdit, QSlider
)
from PyQt5.QtCore import Qt

from app.util.widget_helpers import (
	QGeneric,
	new_button,
	clear_layout
)
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

		self.destination_path    = ""

		self.data   = None
		self.layout = None
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
		self.data["Model Name"].setText(self.file_name)

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
		if not os.path.exists(self.destination_path):
			os.makedirs(self.destination_path)

		# Move file
		shutil.move(self.file_path, get_text(self.destination_display))

		# Create json
		with open(get_text(self.destination_display).replace(self.file_extension, ".json"), 'w') as f:
			json.dump(data, f, indent=4)

	########## Constructors ##########
	def _init_data(self):
		'''
		Helper function to initialize GUI data.
		Should only be used once on construction.
		'''
		self._new_load_parameters()
		self._connect_destination_paths(self.data)
		# load default data

	def _new_load_parameters(self):
		'''
		Initializes GI data and layout.
		These must be done concurrently due to limitations with accessing
		different QObjects.
		data   - contains QObjects
		layout - contains wrapped objects
		'''

		data = {}
		layout = QVBoxLayout()
		
		for label, table in self.config["layout"].items():
			data[label] = QGeneric(label, table)
			layout.addWidget(data[label].widget)
			# self._new_parameter(data, layout, label, table)
		
		layout.addWidget(new_button("Save", self.save_file))
		
		self.data   = data
		self.layout = layout
			
	def _connect_destination_paths(self, data):
		# TODO make this dynamic based on configuration path options
		data["Model Name"].widget_core.textChanged.connect(self._update_destination_path)
		
		data["Model Type"].widget_core.buttonClicked.connect(self._update_destination_path)
		data["Category"  ].widget_core.textChanged.connect(self._update_destination_path)
		data["Model ID"  ].widget_core.textChanged.connect(self._update_destination_path)
		data["SD Version"].widget_core.buttonClicked.connect(self._update_destination_path)

		# data["Weight"]["value"].textChanged.connect(self._weight_changed)
		# data["Weight"]["slider"].valueChanged.connect(self._weight_changed)
	
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
		print("entering update destination path")
		# TODO make this not hardcoded.
		self.destination_path = os.path.join(
			self.config["default_path"],
			self.data["Model Type"].text,
			self.data["SD Version"].text,
			self.data["Category"].text
		)

		self.data["Path"].setText(os.path.join(
			self.destination_path,
			self.data["Model Name"].text + self.file_extension
		))
	
	# def _weight_changed(self, value):
	# 	self.data["Weight"]["value"].setText(f"{value}")
	# 	self.data["Weight"]["slider"].setValue(value)
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
	new_widget, new_button, new_radio_button_group,
	get_text, set_text, clear_layout
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
		# self.destination_display = QLineEdit()

		self._fixed_width = 350

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
			"id"               : get_text(self.data["Model ID"]),
			"description"      : get_text(self.data["Description"]),
			"sd version"       : get_text(self.data["SD Version"]),
			"activation text"  : get_text(self.data["Activation"]),
			"preferred weight" : get_text(self.data["Weight"]),
			"notes"            : get_text(self.data["Notes"])
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
			self._new_parameter(data, layout, label, table)
		
		layout.addWidget(new_button("Save", self.save_file))
		
		self.data   = data
		self.layout = layout

	def _new_parameter(self, data, layout, label, line):
		# TODO maybe change this to not need "widget" tag
		match line["widget"]:
			case "line":
				insert = QLineEdit()
				insert.setFixedWidth(self._fixed_width)
				data[label] = insert
				layout.addWidget(new_widget(label, insert))
			case "text":
				insert = QTextEdit()
				insert.setFixedWidth(self._fixed_width)
				data[label] = insert
				layout.addWidget(new_widget(label, insert))
			case "radio":
				radio_widget = QWidget()
				radio_layout = QHBoxLayout()
				button_group = QButtonGroup()

				for option in line["options"]:
					radio_button = QRadioButton(str(option))
					radio_button.setStyleSheet(
						'''
						QRadioButton{
							border: 1px solid grey;
							border-radius: 4px;
							padding: 5px;
						}
						'''
					)
					
					radio_layout.addWidget(radio_button)
					button_group.addButton(radio_button)

					if option == line["default"]:
						radio_button.setChecked(True)

				radio_widget.setLayout(radio_layout)
				data[label] = button_group
				layout.addWidget(new_widget(label, radio_widget))
	
	def _connect_destination_paths(self, data):
		# TODO make this dynamic based on configuration path options
		pass
		data["Model Name"].textChanged.connect(self._update_destination_path)
		
		data["Model Type"].buttonClicked.connect(self._update_destination_path)
		data["Category"  ].textChanged.connect(self._update_destination_path)
		data["Model ID"  ].textChanged.connect(self._update_destination_path)
		data["SD Version"].buttonClicked.connect(self._update_destination_path)

		# TODO Remove Hard coding

		# Weight
		# data["Weight"].setRange(
		# 	self.config["preferred_weight"]["bounds"]["lower"],
		# 	self.config["preferred_weight"]["bounds"]["upper"]
		# )

		# data["Weight"].valueChanged.connect(self._weight_changed)
	
	########## Data Managers ##########
	def _set_text(self, key, value=""):
		'''
		Sets text on load.
		'''
		if value != "" or key not in self.config["layout"]:
			set_text(self.data[key], value)
		elif not self.config["layout"][key].get("remember_last", False):
			set_text(self.data[key], self.config["layout"][key].get("default", value))

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
			get_text(self.data["Model Type"]),
			get_text(self.data["SD Version"]),
			get_text(self.data["Category"])
		)

		self.data["Path"].setText(os.path.join(
			self.destination_path,
			get_text(self.data["Model Name"]) + self.file_extension
		))
	
	# def _weight_changed(self, value):
	# 	self.data["Weight"].label.setText(f"Weight {value}")
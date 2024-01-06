import re
from PyQt5.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QCheckBox,
    QPushButton
)

from app.util import config

class ConfigWindow(QDialog):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Configuration Window")
		self.resize(500, 200)

		self.config = config.load()
		self.data = {}
		self.init_ui()

	def init_ui(self):
		layout = QVBoxLayout()
		self.form_layout = QFormLayout()

		# Default Path
		self.data["default_path"] = QLineEdit(self.config["default_path"])
		self.form_layout.addRow(
			QLabel("Default Path"),
			self.data["default_path"]
		)

		# Layout
		data_layout = {}
		for key, settings in self.config["layout"].items():
			data_layout[key] = {}
			self.form_layout.addRow(QLabel(key))

			if "default" in settings:
				data_layout[key]["default"] = QLineEdit(str(settings["default"]))
				self.form_layout.addRow(QLabel("\tDefault"), data_layout[key]["default"])
			
			if "options" in settings:
				data_layout[key]["options"] = QLineEdit(", ".join(map(str, settings["options"])))
				self.form_layout.addRow(QLabel("\tOptions"), data_layout[key]["options"])

			if "bounds" in settings:
				data_layout[key]["bounds"] = {}
				data_layout[key]["bounds"]["lower"] = QLineEdit(str(settings["bounds"]["lower"]))
				data_layout[key]["bounds"]["upper"] = QLineEdit(str(settings["bounds"]["upper"]))
				
				box = QHBoxLayout()
				box.addWidget(data_layout[key]["bounds"]["lower"])
				box.addWidget(QLabel(" - "))
				box.addWidget(data_layout[key]["bounds"]["upper"])
				
				self.form_layout.addRow(QLabel("\tBounds"), box)

			if "remember_last" in settings:
				data_layout[key]["remember_last"] = QCheckBox()
				data_layout[key]["remember_last"].setChecked(settings["remember_last"])
				self.form_layout.addRow(QLabel("\tRemember Last"), data_layout[key]["remember_last"])
		
		self.data["layout"] = data_layout

		save_button = QPushButton("Save")
		save_button.clicked.connect(self.save_settings)

		layout.addLayout(self.form_layout)
		layout.addWidget(save_button)

		self.setLayout(layout)
	
	def save_settings(self):

		def filter_data(data):
			# Sanitize data and return in correct typing
			data = data.strip()
			if re.match(r'^-?\d+$', data):
				data = int(data)
			elif re.match(r'^-?\d+\.\d*$', data):
				try:
					data = float(data)
				except ValueError:
					pass
			return data

		try:
			data = {}

			data["default_path"] = self.data["default_path"].text()
			data["layout"] = {}

			for key, settings in self.data["layout"].items():
				match settings:
					case QLineEdit():
						data["layout"][key] = settings.text()

					case dict():
						data["layout"][key] = {"widget" : self.config["layout"][key]["widget"]}
						if "default" in settings:
							data["layout"][key]["default"] = filter_data(settings["default"].text())

						if "options" in settings:
							data["layout"][key]["options"] = [filter_data(option) for option in settings["options"].text().split(",")]

						if "bounds" in settings:
							data["layout"][key]["bounds"] = {
								"lower" : filter_data(settings["bounds"]["lower"].text()),
								"upper" : filter_data(settings["bounds"]["upper"].text())
							}
						
						if "remember_last" in settings:
							data["layout"][key]["remember_last"] = settings["remember_last"].isChecked()

			config.save(data)
			self.accept()
		except:
			self.reject()
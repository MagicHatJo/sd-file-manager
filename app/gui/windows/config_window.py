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
		self.data["layout"] = {}
		for key, settings in self.config["layout"].items():
			self.data["layout"][key] = {}
			self.form_layout.addRow(QLabel(key))

			if "default" in settings:
				self.data["layout"][key]["default"] = QLineEdit(str(settings["default"]))
				self.form_layout.addRow(QLabel("\tDefault"), self.data["layout"][key]["default"])
			
			if "options" in settings:
				self.data["layout"][key]["options"] = QLineEdit(", ".join(map(str, settings["options"])))
				self.form_layout.addRow(QLabel("\tOptions"), self.data["layout"][key]["options"])

			if "bounds" in settings:
				self.data["layout"][key]["bounds"] = {}
				self.data["layout"][key]["bounds"]["lower"] = QLineEdit(str(settings["bounds"]["lower"]))
				self.data["layout"][key]["bounds"]["upper"] = QLineEdit(str(settings["bounds"]["upper"]))
				
				box = QHBoxLayout()
				box.addWidget(self.data["layout"][key]["bounds"]["lower"])
				box.addWidget(QLabel(" - "))
				box.addWidget(self.data["layout"][key]["bounds"]["upper"])
				
				self.form_layout.addRow(QLabel("\tBounds"), box)

			if "remember_last" in settings:
				self.data["layout"][key]["remember_last"] = QCheckBox()
				self.data["layout"][key]["remember_last"].setChecked(settings["remember_last"])
				self.form_layout.addRow(QLabel("\tRemember Last"), self.data["layout"][key]["remember_last"])

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
			self.config["default_path"] = self.data["default_path"].text()

			for key, settings in self.data["layout"].items():
				match settings:
					case QLineEdit():
						self.config["layout"][key] = settings.text()

					case dict():
						self.config["layout"][key] = {"widget" : self.config["layout"][key]["widget"]}
						if "default" in settings:
							self.config["layout"][key]["default"] = filter_data(settings["default"].text())

						if "options" in settings:
							self.config["layout"][key]["options"] = [filter_data(option) for option in settings["options"].text().split(",")]

						if "bounds" in settings:
							self.config["layout"][key]["bounds"] = {
								"lower" : filter_data(settings["bounds"]["lower"].text()),
								"upper" : filter_data(settings["bounds"]["upper"].text())
							}
						
						if "remember_last" in settings:
							self.config["layout"][key]["remember_last"] = settings["remember_last"].isChecked()

			config.save(self.config)
			self.accept()
		except:
			self.reject()
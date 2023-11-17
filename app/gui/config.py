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

		for key, settings in self.config.items():
			match settings:
				case str():
					self.data[key] = QLineEdit(settings)
					self.form_layout.addRow(
						QLabel(key),
						self.data[key]
					)
				case dict():
					self.data[key] = {}
					self.form_layout.addRow(QLabel(key))

					if "default" in settings:
						self.data[key]["default"] = QLineEdit(str(settings["default"]))
						self.form_layout.addRow(QLabel("\tDefault"), self.data[key]["default"])
					
					if "options" in settings:
						self.data[key]["options"] = QLineEdit(", ".join(map(str, settings["options"])))
						self.form_layout.addRow(QLabel("\tOptions"), self.data[key]["options"])

					if "bounds" in settings:
						self.data[key]["bounds"] = {}
						self.data[key]["bounds"]["lower"] = QLineEdit(str(settings["bounds"]["lower"]))
						self.data[key]["bounds"]["upper"] = QLineEdit(str(settings["bounds"]["upper"]))
						box = QHBoxLayout()
						box.addWidget(self.data[key]["bounds"]["lower"])
						box.addWidget(QLabel(" - "))
						box.addWidget(self.data[key]["bounds"]["upper"])
						self.form_layout.addRow(QLabel("\tBounds"), box)

					if "remember_last" in settings:
						self.data[key]["remember_last"] = QCheckBox()
						self.data[key]["remember_last"].setChecked(settings["remember_last"])
						self.form_layout.addRow(QLabel("\tRemember Last"), self.data[key]["remember_last"])

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

			for key, settings in self.data.items():
				match settings:
					case QLineEdit():
						data[key] = settings.text()

					case dict():
						data[key] = {}
						if "default" in settings:
							data[key]["default"] = filter_data(settings["default"].text())

						if "options" in settings:
							data[key]["options"] = [filter_data(option) for option in settings["options"].text().split(",")]

						if "bounds" in settings:
							data[key]["bounds"] = {
								"lower" : filter_data(settings["bounds"]["lower"].text()),
								"upper" : filter_data(settings["bounds"]["upper"].text())
							}
						
						if "remember_last" in settings:
							data[key]["remember_last"] = settings["remember_last"].isChecked()

			config.save(data)
			self.accept()
		except:
			self.reject()
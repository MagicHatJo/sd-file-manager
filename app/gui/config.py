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
		form_layout = QFormLayout()

		for key, settings in self.config.items():
			match settings:
				case str():
					self.data[key] = QLineEdit(settings)
					form_layout.addRow(
						QLabel(key),
						self.data[key]
					)
				case dict():
					self.data[key] = {}
					form_layout.addRow(QLabel(key))

					if "default" in settings:
						self.data[key]["default"] = QLineEdit(str(settings["default"]))
						form_layout.addRow(QLabel("\tDefault"), self.data[key]["default"])
					
					if "options" in settings:
						self.data[key]["options"] = QLineEdit(", ".join(map(str, settings["options"])))
						form_layout.addRow(QLabel("\tOptions"), self.data[key]["options"])

					if "bounds" in settings:
						self.data[key]["bounds"] = QHBoxLayout()
						self.data[key]["bounds"].addWidget(QLineEdit(str(settings["bounds"]["lower"])))
						self.data[key]["bounds"].addWidget(QLabel(" - "))
						self.data[key]["bounds"].addWidget(QLineEdit(str(settings["bounds"]["upper"])))
						form_layout.addRow(QLabel("\tBounds"), self.data[key]["bounds"])

					if "remember_last" in settings:
						self.data[key]["remember_last"] = QCheckBox()
						self.data[key]["remember_last"].setChecked(settings["remember_last"])
						form_layout.addRow(QLabel("\tRemember Last"), self.data[key]["remember_last"])

		save_button = QPushButton("Save")
		save_button.clicked.connect(self.save_settings)

		layout.addLayout(form_layout)
		layout.addWidget(save_button)

		self.setLayout(layout)
	
	def save_settings(self):
		# Go through layout, turn data into json
		data = {}

		form_layout = self.layout.itemAt(0).widget()

		for i in range(form_layout.rowCount()):
			label_widget = self.form_layout.itemAt(i, QFormLayout.LabelRole).widget()
			field_widget = self.form_layout.itemAt(i, QFormLayout.FieldRole).widget()

			print(label_widget)


		print(data)
		#config.save(data)

		# close window
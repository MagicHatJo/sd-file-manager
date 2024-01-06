
from PyQt5.QtWidgets import (
	QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,QButtonGroup,QRadioButton,
	QLineEdit, QTextEdit, QCheckBox, QSlider
)
from PyQt5.QtCore import Qt

fixed_width = 350 # TODO move to config

class QGeneric:
	'''
	Generic wrapper for different QWidget composites.
	'''
	def __init__(self, label, table):
		self.label = label
		self.table = table
		self.widget_core = None
		self.value = ""

		self.widget = {
			"line"   : self._new_line,
			"text"   : self._new_text,
			"radio"  : self._new_radio,
			"slider" : self._new_slider
		}[self.table["widget"]](label, table)
	
	########## Attributes ##########
	@property
	def text(self):
		match self.table["widget"]:
			case "line":
				return self.widget_core.text()
			case "text":
				return self.widget_core.toPlainText()
			case "radio":
				for button in self.widget_core.buttons():
					if button.isChecked():
						return button.text()
		return ""

	@text.setter
	def text(self, new):
		match self.table["widget"]:
			case "line" | "text":
				self.widget_core.setText(str(new))
			case "radio":
				for button in self.widget_core.buttons():
					if button.text() == str(new):
						button.setChecked(True)
						return

	########## Constructors ##########
	def _new_line(self, label, table):
		'''
		Initializes self with QLineEdit data.
		'''
		self.widget_core = QLineEdit()
		self.widget_core.setFixedWidth(fixed_width)
		
		widget = QWidget()
		layout = QHBoxLayout()
		layout.addWidget(QLabel(label))
		layout.addWidget(self.widget_core)
		widget.setLayout(layout)
		return widget

	def _new_text(self, label, table):
		'''
		Initializes self with QTextEdit data.
		'''
		self.widget_core = QTextEdit()
		self.widget_core.setFixedWidth(fixed_width)

		widget = QWidget()
		layout = QHBoxLayout()
		layout.addWidget(QLabel(label))
		layout.addWidget(self.widget_core)
		widget.setLayout(layout)
		return widget
	
	def _new_radio(self, label, table):
		'''
		Initializes self with QButtonGroup for QRadioButton data.
		'''
		widget = QWidget()
		layout = QHBoxLayout()
		layout.addWidget(QLabel(label))
		self.widget_core = QButtonGroup()

		for option in table["options"]:
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
			
			layout.addWidget(radio_button)
			self.widget_core.addButton(radio_button)

			if option == table["default"]:
				radio_button.setChecked(True)

		widget.setLayout(layout)
		return widget
	
	def _new_slider(self, label, table):
		'''
		Initializes self with QSlider data.
		Slider step must be int, so multiply / divide by 10 to convert decimals.
		'''
		widget = QWidget()
		layout = QVBoxLayout()

		# Upper
		upper_widget = QWidget()
		upper_layout = QHBoxLayout()
		
		self.value = QLineEdit()
		self.value.setFixedWidth(50)
		self.value.setText(str(table.get("default", "1")))
		upper_layout.addWidget(QLabel(label))
		upper_layout.addWidget(self.value)
		upper_widget.setLayout(upper_layout)

		# Lower
		self.widget_core = QSlider()
		self.widget_core.setOrientation(Qt.Horizontal)
		self.widget_core.setRange(table["bounds"]["lower"] * 10, table["bounds"]["upper"] * 10)
		self.widget_core.setValue(table.get("default", 10))
		self.widget_core.setSingleStep(1)

		self.value.textChanged.connect(self._slider_sync)
		self.widget_core.valueChanged.connect(self._slider_sync)

		# Compose
		layout.addWidget(upper_widget)
		layout.addWidget(self.widget_core)
		widget.setLayout(layout)
		return widget
	
	########## Data Managers ##########
	def _slider_sync(self, value):
		'''
		Link to change in slider activity.
		Multiply / divide by 10 to convert decimals.
		'''
		match value:
			case "-" | "":
				return
			case int():
				self.value.setText(str(value / 10 if value % 10 else value // 10))
			case str():
				self.widget_core.setValue(int(float(value) * 10))
				if not self.table["bounds"]["lower"] <= float(value) <= self.table["bounds"]["upper"]:
					self.value.setText(str(min(max(
						float(value),
						self.table["bounds"]["lower"]),
						self.table["bounds"]["upper"]
					)))
	
	########## Signals ##########
	def connect(self, func):
		match self.table["widget"]:
			case "line" | "text":
				self.widget_core.textChanged.connect(func)
			case "radio":
				self.widget_core.buttonClicked.connect(func)
			case "slider":
				self.widget_core.valueChanged.connect(func)
def new_button(button_name, button_function):
	button = QPushButton(button_name)
	button.clicked.connect(button_function)
	return button

def clear_layout(layout):
	for i in reversed(range(layout.count())): 
		layout.itemAt(i).widget().setParent(None)
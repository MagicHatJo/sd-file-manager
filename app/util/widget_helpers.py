
from PyQt5.QtWidgets import (
	QWidget, QHBoxLayout, QLabel, QPushButton,QButtonGroup,QRadioButton,
	QLineEdit, QTextEdit, QCheckBox
)

fixed_width = 350 # TODO move to config

class QGeneric:
	'''
	Generic wrapper for different QWidget composites.
	'''
	def __init__(self, label, table):
		self.label = label
		self.table = table

		self.widget = {
			"line"  : self._new_line,
			"text"  : self._new_text,
			"radio" : self._new_radio
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
		self.widget_core = QLineEdit()
		self.widget_core.setFixedWidth(fixed_width)
		
		widget = QWidget()
		layout = QHBoxLayout()
		layout.addWidget(QLabel(label))
		layout.addWidget(self.widget_core)
		widget.setLayout(layout)
		return widget

	def _new_text(self, label, table):
		self.widget_core = QTextEdit()
		self.widget_core.setFixedWidth(fixed_width)

		widget = QWidget()
		layout = QHBoxLayout()
		layout.addWidget(QLabel(label))
		layout.addWidget(self.widget_core)
		widget.setLayout(layout)
		return widget
	
	def _new_radio(self, label, table):
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

def new_button(button_name, button_function):
	button = QPushButton(button_name)
	button.clicked.connect(button_function)
	return button

def clear_layout(layout):
	for i in reversed(range(layout.count())): 
		layout.itemAt(i).widget().setParent(None)
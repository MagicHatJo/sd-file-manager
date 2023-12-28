
from PyQt5.QtWidgets import (
	QWidget, QHBoxLayout, QLabel, QPushButton,QButtonGroup,QRadioButton,
	QLineEdit, QTextEdit, QCheckBox
)

def new_widget(line_name, line_class):
	widget = QWidget()
	layout = QHBoxLayout()
	layout.addWidget(QLabel(line_name))
	layout.addWidget(line_class)
	widget.setLayout(layout)
	return widget

def new_button(button_name, button_function):
	button = QPushButton(button_name)
	button.clicked.connect(button_function)
	return button

def new_checkbox(checkbox_default):
	checkbox = QCheckBox()
	checkbox.setChecked(checkbox_default)
	return checkbox

def new_radio_button_group(options, default):
	widget = QWidget()
	layout = QHBoxLayout()

	button_group = QButtonGroup()

	for option in options:
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
		button_group.addButton(radio_button)

		if option == default:
			radio_button.setChecked(True)

	widget.setLayout(layout)
	return widget

def get_text(widget):
	'''
	Gets a value from an unknown QObject.
	'''
	match widget:
		case QLineEdit():
			return widget.text()
		case QTextEdit():
			return widget.toPlainText()
		case QButtonGroup():
			for button in widget.buttons():
				if button.isChecked():
					return button.text()
	return ""

def set_text(widget, value):
	'''
	Sets a value to an unknown QObject.
	'''
	match widget:
		case QLineEdit() | QTextEdit():
			widget.setText(str(value))
		case QButtonGroup():
			for button in widget.buttons():
				if button.text() == str(value):
					button.setChecked(True)
					return

def clear_layout(layout):
	for i in reversed(range(layout.count())): 
		layout.itemAt(i).widget().setParent(None)
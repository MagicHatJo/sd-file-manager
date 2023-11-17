
from PyQt5.QtWidgets import (
	QWidget, QHBoxLayout, QLabel, QPushButton,
	QLineEdit, QTextEdit, QCheckBox
)

def new_widget(line_name, line_class):
	widget = QWidget()
	widget.layout = QHBoxLayout(widget)
	widget.layout.addWidget(QLabel(line_name))
	widget.layout.addWidget(line_class)
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
		radio_button = QRadioButton(option)
		layout.addWidget(radio_button)
		button_group.addButton(radio_button)

		if option == default:
			radio_button.setChecked(True)

	widget.setLayout(layout)
	return widget

def get_edit_text(widget, line_class):
	line_edit = widget.findChildren(line_class)[0]
	if line_class is QLineEdit:
		return line_edit.text()
	if line_class is QTextEdit:
		return line_edit.toPlainText()
	return None

def clear_layout(layout):
	for i in reversed(range(layout.count())): 
		layout.itemAt(i).widget().setParent(None)
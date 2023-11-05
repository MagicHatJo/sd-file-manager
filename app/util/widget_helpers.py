
from PyQt5.QtWidgets import (
	QWidget, QHBoxLayout, QLabel, QPushButton,
	QLineEdit, QTextEdit
)

def new_widget(line_name, line_class, default_text=""):
	widget = QWidget()
	widget.layout = QHBoxLayout(widget)

	label = QLabel(line_name)
	line_edit = line_class()
	line_edit.setText(default_text)

	widget.layout.addWidget(label)
	widget.layout.addWidget(line_edit)
	return widget

def new_button(button_name, button_function):
	button = QPushButton(button_name)
	button.clicked.connect(button_function)
	return button

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
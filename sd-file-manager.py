import sys
import logging

from PyQt5.QtWidgets import QApplication
from app.gui.file_manager import FileManager

if __name__ == "__main__":
	app = QApplication(sys.argv)
	logging.root.setLevel(logging.DEBUG)
	file_manager = FileManager()
	file_manager.show()
	sys.exit(app.exec_())
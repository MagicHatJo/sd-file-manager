import sys

from PyQt5.QtWidgets import QApplication
from app.gui.file_manager import FileManager

if __name__ == "__main__":
	app = QApplication(sys.argv)
	file_manager = FileManager()
	file_manager.show()
	sys.exit(app.exec_())
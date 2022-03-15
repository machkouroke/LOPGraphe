from GUI.main_windows import Main
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QApplication
from sys import argv

# Paramétrage avant le lancement de l'application
if __name__ == '__main__':
    app = QApplication(argv)
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(255, 255, 255))
    windows = Main('UI/interface.ui')
    app.setStyle('Fusion')
    app.setPalette(palette)
    app.exec()

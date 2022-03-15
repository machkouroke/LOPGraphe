from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMessageBox


class Warn(QMessageBox):
    """
    Boite de dialogue permettant le choix du fichier graphe et de son point de départ
    """

    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.setIcon(QMessageBox.Icon.Warning)
        self.setText(message)
        self.setWindowIcon(QIcon("../icons/lop.png"))
        self.setWindowTitle("Avertissement")
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.exec()



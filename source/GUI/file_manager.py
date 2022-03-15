import os
from GUI.DialogBox import Warn
import networkx as nx
from PyQt6 import uic
from PyQt6.QtWidgets import QFileDialog


def graphe_to_file(graphe, filename):
    with open(filename, 'w') as file:
        for i in graphe.edges:
            file.write(f"{i[0]} {graphe.edges[i[0], i[1]]['weight']} {i[1]}\n")


class Selection:
    """Sélectionne un fichier et en extrait un graphe"""
    def __init__(self, filename):
        self.temp_graphe = None
        self.selection = uic.loadUi(filename)
        self.selection.path_select.clicked.connect(self.file_select)

    def file_select(self):
        self.selection.path.setText(QFileDialog.getOpenFileName()[0])
        if self.selection.path.text():
            if os.path.basename(self.selection.path.text()).endswith(".lop"):
                self.temp_graphe = nx.Graph()
                with open(self.selection.path.text()) as file:
                    for choice in file:
                        a, w, b = choice.split()
                        self.temp_graphe.add_edge(a, b, weight=int(w))
                self.selection.depart_point.clear()
                for i in self.temp_graphe.nodes:
                    self.selection.depart_point.addItem(i)
            else:
                Warn("Veuillez sélectionner un fichier lop qui contient toute les informations requises"
                     " pour la construction de votre graphe")

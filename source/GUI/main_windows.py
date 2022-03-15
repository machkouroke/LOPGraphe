
from GUI.DialogBox import Warn
from prime import prime_optimized, prime_naif
from GUI.Plot import Plotter
from PyQt6 import uic
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from GUI.file_manager import Selection, graphe_to_file
from PyQt6.QtCore import QThreadPool
import networkx as nx
import random as rd


class Main:
    """
    Se charge de gérer la fenêtre principale, mais aussi de faire le lien entre tous les programmes
    """
    def __init__(self, filename):
        # Chargement de la fenêtre et de la fenêtre de selection de graphe à partir
        # de la feuille ui de Qt Designer
        self.maze = None
        self.windows = uic.loadUi(filename, None)
        self.graphe_file = Selection('UI/select.ui')

        # Initialisation des paramètres requis au graphe
        self.depart_point = None
        self.graphe = None

        # Plotter des versions simples
        self.plot = None

        # Version des algorithmes qu'on va utiliser pour le plot
        self.optimized = None
        self.naif = None

        # Connection slot/signal
        self.windows.charger_graphe.clicked.connect(self.graphe_file.selection.exec)
        self.graphe_file.selection.confirm.clicked.connect(self.graph_constructor)
        self.windows.naif.clicked.connect(self.drawer)
        self.windows.aleatoire.clicked.connect(self.aleatoire)
        self.windows.maze.clicked.connect(self.maze_maker)
        self.windows.optimized.clicked.connect(self.drawer)
        self.windows.comparaison.clicked.connect(self.comparaison)
        self.thread = QThreadPool()

        # Ouverture de la fenêtre
        self.windows.show()

    def aleatoire(self):
        """
        Génère un graphe aléatoire
        """
        # Formation du graphe et choix d'un point aléatoire
        self.graphe = nx.gnm_random_graph(5, 12)
        for i in self.graphe.edges:
            self.graphe.edges[i[0], i[1]]['weight'] = rd.randint(1, 1000)
        self.depart_point = rd.choice(list(self.graphe.nodes))

        # Propose à l'utilisateur d'enregistrer le graphe
        button = QMessageBox.question(self.windows, "Enregistrer le fichier", "Vouliez vous enregistrer votre"
                                                                              " graphe en fichier lop?")
        if button == QMessageBox.StandardButton.Yes:
            path_to_save = QFileDialog.getSaveFileName()[0]
            if path_to_save:
                graphe_to_file(self.graphe, path_to_save)
            else:
                Warn("Aucun fichier n'a été sélectionné")

    def graph_constructor(self):
        """
        Remplis les informations de notre graphe avec les informations
        renseigné par l'utilisateur
        """
        if self.graphe_file.selection.path.text():
            self.graphe = self.graphe_file.temp_graphe
            self.depart_point = self.graphe_file.selection.depart_point.currentText()
        else:
            Warn("Aucun fichier n'a été sélectionné")

    def drawer(self):
        """
        Se charge de sélectionner l'algorithme à lancer en fonction du bouton appuyé
        """
        # fenêtre de plot
        version = prime_naif if self.windows.sender().objectName() == 'naif' else prime_optimized
        if self.graphe is None:
            Warn("Veuillez choisir un fichier d'abord")
            return
        self.plot = Plotter(version, self.depart_point, self.graphe)

    def comparaison(self):
        """
        Ici on effectue une comparaison entre les deux versions de l'algorithme
        """
        if self.graphe is None:
            Warn("Veuillez choisir un fichier d'abord")
            return
        self.naif = Plotter(prime_naif, self.depart_point, self.graphe, 700, 0, mode='speed_test')
        self.optimized = Plotter(prime_optimized, self.depart_point, self.graphe, 0, 0, mode='speed_test')

    def maze_maker(self):
        """
        Forme une grille de poids aléatoire qu'on va transformer en labyrinthes avec algorithm de Prime
        """
        self.maze = nx.grid_2d_graph(20, 20)
        for i in self.maze.edges:
            self.maze.edges[i[0], i[1]]['weight'] = rd.randint(1, 1000)
        self.maze = Plotter(prime_optimized, rd.choice(list(self.maze.nodes)), self.maze, mode='maze')

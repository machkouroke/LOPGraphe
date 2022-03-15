from PyQt6.QtCore import QRunnable, QObject, pyqtSignal, QThreadPool
import networkx as nx

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QProgressBar, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt


class TreatmentSignal(QObject):
    """
    Signal envoyé par le tracé de graphe
    """
    progression = pyqtSignal(int)
    plotting = pyqtSignal(int)
    finished = pyqtSignal(float)


class Runner(QRunnable):
    """
    Thread des tracé de graphe
    """

    def __init__(self):
        super().__init__()
        self.signals = TreatmentSignal()

    def run(self):
        n = 100
        for i in range(n):
            prog = int(100 * float(i + 1) / n)
            self.signals.plotting.emit(n)
            self.signals.progression.emit(prog)
        self.signals.finished.emit(1)


class Plotter(QDialog):
    def __init__(self, version, depart, graph, x=0, y=0, mode='simple', parent=None):
        super(Plotter, self).__init__(parent)
        self.setWindowTitle("LOP Graph")
        self.setWindowIcon(QIcon("../icons/lop.png"))
        # Fonction de l'algorithme et point de départ
        self.version = version
        self.depart = depart
        self.graph = graph
        # Chef d'orchestre des taches
        self.thread = QThreadPool()
        self.i = 0
        # Figure pour afficher les graphes
        self.figure = plt.figure()

        # Déplacer la fenêtre dans un angle donné
        self.move(x, y)

        # Widget qt pour l'affichage
        self.canvas = FigureCanvas(self.figure)

        # Barre de navigation
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.time_average = 0
        # Layout et ajout des fichiers
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        if mode != 'simple':
            self.label_average = QLabel()
            self.load_bar = QProgressBar()
            self.label_average.hide()
            layout.addWidget(self.label_average)
            layout.addWidget(self.load_bar)
        self.setLayout(layout)
        if mode == 'simple':
            self.plot()
        elif mode == 'maze':
            self.label_average.hide()
            self.maze_plot()
        else:
            self.plot()
            self.benchmark()

    def benchmark(self):
        process = Runner()
        process.signals.plotting.connect(self.plot)
        process.signals.progression.connect(self.load_bar.setValue)
        process.signals.finished.connect(self.label_show)
        self.thread.start(process)

    def label_show(self):
        self.label_average.setText(
            f"Le temps d'exécution relativement au processeur de {self.version.__name__} algorithm est {self.time_average} "
            f"nanoseconds en {self.i} fois")
        self.label_average.show()

    def maze_plot(self):
        self.figure.clear()
        # Ajout des deux exe qui vont contenir
        # respectivement l'arbre et son mst
        ax1 = self.figure.add_subplot(121)
        ax1.set_title('Grille')
        ax2 = self.figure.add_subplot(122)
        ax2.set_title('Labyrinthe')

        # Tracé du graphe
        t = self.graph
        pos = {(x, y): (x, y) for x, y in t.nodes}
        nx.draw(t, pos=pos, ax=ax1, node_size=10)

        # On reçoit ici le mst et on le trace également
        i, time = self.version(t, self.depart)
        nx.draw(i, pos=pos, ax=ax2, node_color="tab:orange", node_size=0)

        # Actualise le canvas du plot
        self.canvas.draw()
        self.show()

    def plot(self):
        self.figure.clear()

        # Ajout des deux exe qui vont contenir
        # respectivement l'arbre et son mst
        ax1 = self.figure.add_subplot(121)
        ax1.set_title('Graphe')
        ax2 = self.figure.add_subplot(122)
        ax2.set_title('Arbre couvrant minimal')

        # Tracé du graphe
        t = self.graph
        pos1 = nx.spring_layout(t, k=2)
        nx.draw(t, pos1, with_labels=True, font_weight='bold', ax=ax1)
        labels1 = nx.get_edge_attributes(t, 'weight')
        nx.draw_networkx_edge_labels(t, pos1, edge_labels=labels1, ax=ax1)

        # On reçoit ici le mst et on le trace également
        i, time = self.version(t, self.depart)
        self.time_average += time
        self.i += 1
        pos2 = nx.spring_layout(i, k=2)
        nx.draw(i, pos2, with_labels=True, font_weight='bold', ax=ax2)
        labels2 = nx.get_edge_attributes(i, 'weight')
        nx.draw_networkx_edge_labels(i, pos2, edge_labels=labels2, ax=ax2)
        # Actualise le canvas du plot
        self.canvas.draw()
        self.show()

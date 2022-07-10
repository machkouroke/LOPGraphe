LOPGraphe
============

### Générateur d'arbre couvrant minimum avec l'algorithme de Prime
![image](https://user-images.githubusercontent.com/40785379/178157179-fba674de-2f26-4737-baa9-d040b61c41a8.png)

<a href="https://buymeacoffee.com/machkouroke" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>


## Caractéristique
- Génération de graphe aléatoire
- Support de fichier lop permettant une description très simple d'un graphe
- Benchmark comparant l'algorithme avec et sans file de priorité
- Génration d'un motif de labyrinthe à base de l'algorithme de Prime

---

## Configuration
- Cloner le répository
```
git clone
```
- Installer les dépendances (Windows)
```
pip install virtualenv

python -m venv venv

source venv/bin/activate

.\venv\Scripts\activate 

pip install -r requirements.txt    

```
- Executer le fichier main.py


## Language Lop
Vous pouviez utiliser le language lop pour décrire très simplement vos graphe

### Syntaxe
```
node1 weight1 node 2
node2 weight2 node 3
...
nodei weighti node i
```

### Exemple
```
a 2 b
a 5 g
b 15 g
b 10 d
g 3 d
b 3 e
d 1 e
c 7 d
c 5 g
c 10 e
c 12 f
f 11 e
```

Pour pouvoir l'utiliser dans le programme vous deviez enrégistrer votre fichier avec l'extension <b>.lop</b>



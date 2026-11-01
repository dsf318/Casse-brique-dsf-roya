# Casse-brique-dsf-roy
Projet de groupe : Sacha Roy et Da Silva Ferraz Alexis

## Dépôt Git
Adresse du dépôt : https://github.com/dsf318/Casse-brique-dsf-roya

## Lancer le jeu
Python 3 avec Tkinter est nécessaire. Garder le dossier `Images` avec les fichiers Python.

```sh
python3 Cassebrique.py
```
## Règles du jeu
- Le menu propose 3 niveaux : plus le niveau est élevé, plus il y a de lignes de briques.
- On déplace le padel avec les flèches gauche/droite ou les touches Q / D.
- La balle rebondit sur les murs, le plafond, le padel et les briques avec une vitesse constante. Sur la raquette, le rebond inverse la vitesse verticale et conserve la vitesse horizontale.
- Chaque brique rapporte 10 points.
- On a 3 vies : si la balle tombe en bas, on perd une vie.
- Plus de vies : GAME OVER.
- Toutes les briques détruites : VICTOIRE.
- Dans un niveau, « Quitter » ramène au menu ; dans le menu principal, « Quitter le jeu »  ferme le programme.



## Fichiers
- `Cassebrique.py` : fichier à lancer
- `fenetre.py` : menu et niveaux classes `interface` et `FenetreSecondaire` pour les niveaux et les canevas
- `Balle.py`, `Raquette.py`, `brique.py` : les classes des éléments du jeu
- `structures.py` : liste, pile et file

## Structures de données

Dans `structures.py`, les structures sont construites avec des maillons :
- `Liste` conserve les briques encore présentes.
- `Pile` conserve les trois vies ; une vie perdue retire le dernier élément.
- `File` fait tourner les couleurs rouge, orange et jaune entre les rangées.

La balle utilise `Images/ball.png` et le fond utilise `Images/fond.png`.
Après une vie perdue, une touche de déplacement relance la balle.
Les collisions utilisent les rectangles qui entourent les images.

Pour le rendu, conserver les fichiers Python, le README et le dossier `Images`
dans la même archive.

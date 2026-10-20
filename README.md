# Casse-brique-dsf-roy
Projet de groupe : Sacha Roy et Da Silva Ferraz Alexis

## Dépôt Git
Adresse du dépôt : https://github.com/dsf318/Casse-brique-dsf-roya

## Lancer le jeu
```
on utilise le fichier ci dessous 
python Cassebrique.py
```
## Règles du jeu
- Le menu propose 3 niveaux : plus le niveau est élevé, plus il y a de lignes de briques.
- On déplace le padel avec les flèches gauche/droite ou les touches Q / D.
- La balle rebondit sur les murs, le plafond, le padel et les briques selon la loi de Descartes sa vitesse ne change pas.
- Chaque brique  rapporte 10 points.
- On a 3 vies : si la balle tombe en bas, on perd une vie. 
- Plus de vie fin du jeu  GAME OVER.
- Toutes les briques détruites fin du jeu VICTOIRE.
- Dans un niveau, « Quitter » ramène au menu ; dans le menu principal, « Quitter le jeu »  ferme le programme.



## Fichiers
- `Cassebrique.py` : fichier à lancer
- `fenetre.py` : menu et niveaux classes `interface` et `FenetreSecondaire` pour les niveaux et les canevas 
- `Balle.py`, `Raquette.py`, `brique.py` : les différentes classe qui permettent de joué 
- `structures.py` : liste, pile et file

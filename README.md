# Casse-brique

Projet de Sacha Roya et Alexis Da Silva Ferraz — TP4, 5 et 6, CPE 3ETI.

## Lancement

Python 3 et Tkinter sont nécessaires. Aucune bibliothèque Python externe n'est utilisée.
Conserver `fond.png` dans le même dossier que les fichiers Python.
Depuis le dossier du projet, lancer :

```sh
python3 Cassebrique.py
```

## Règles et commandes

Choisir un niveau, puis cliquer sur « Démarrer ».
Déplacer la raquette avec les flèches gauche et droite ou les touches Q et D.
Détruire toutes les briques pour gagner. Chaque brique rapporte 10 points.
Le joueur commence avec trois vies. Une balle qui touche le bas du canevas
fait perdre une vie. La balle et la raquette sont alors replacées au centre,
puis le jeu reprend après une seconde. Le score et les briques restantes sont conservés.
La partie est perdue lorsque les trois vies sont épuisées.

« Retour au menu » arrête la partie et permet d'en démarrer une nouvelle.
La croix de la fenêtre de jeu a le même effet. Le bouton « Quitter » du menu
ou sa croix ferme le programme.

## Organisation du code

- `Cassebrique.py` : point d'entrée du programme.
- `fenetre.py` : classes `MenuPrincipal` et `Partie`, interface, animation,
  score, vies et création des briques.
- `balle.py` : classe `Balle`, cercle, déplacement et rebonds sur les murs.
- `Padelorigine.py` : classe `Padel`, raquette et commandes au clavier.
- `brique.py` : classe `Brique`, détection de collision, rebond et destruction.
- `structures.py` : classes `Pile` et `File`.

## Structures de données demandées

### Liste

Dans `fenetre.py`, `Partie.creer_briques()` construit `self.briques`,
une liste native Python contenant les objets `Brique`. Il ne s'agit pas
d'une classe Liste programmée à la main. La méthode `collision_briques()`
la parcourt et retire la brique détruite. Une liste vide indique la victoire.

### Pile : dernier entré, premier sorti (LIFO)

La classe `Pile`, dans `structures.py`, utilise une liste Python.
`empiler()` ajoute à la fin et `depiler()` retire à la fin.
`est_vide()` et `taille()` permettent de consulter son état.
Dans `fenetre.py`, `self.vies` contient les vies numérotées 1, 2 et 3.
À chaque chute, `perdre_vie()` dépile une vie : 3, puis 2, puis 1.

### File : premier entré, premier sorti (FIFO)

La classe `File`, dans `structures.py`, utilise une liste Python.
`enfiler()` ajoute à la fin et `defiler()` retire au début.
Dans `fenetre.py`, `self.messages` contient les messages de début de partie,
de perte de vie et de fin de partie. `afficher_message()` les affiche dans
leur ordre d'arrivée, à raison d'un message toutes les 1,5 seconde.

## Choix et limites de l'implémentation

La balle est un cercle dessiné avec Tkinter. Sur la raquette horizontale,
le rebond conserve `dx` et inverse `dy` : l'angle de réflexion est égal à
l'angle d'incidence. Les collisions balle-brique utilisent le rectangle
englobant de la balle. La position avant le déplacement sert à déterminer
le côté touché. Les contacts aux coins restent approximatifs. La raquette
ne renvoie la balle que si elle franchit son dessus en descendant.

Les trois niveaux déjà présents proposent respectivement 3, 4 et 5 rangées
de 10 briques. La vitesse reste identique entre les niveaux.
La boucle utilise `after()` pour laisser l'interface répondre au clavier.
Les rappels programmés sont annulés à la fermeture de la partie.
La perte de focus vide les touches mémorisées pour éviter un déplacement bloqué.

## Dépôt Git

https://github.com/dsf318/Casse-brique-dsf-roya

## Archive de rendu

Inclure les six fichiers Python, ce README et `fond.png` dans une archive ZIP.
`ball.png` n'est plus utilisé. Les dossiers `.git`, `__pycache__`, les fichiers
`.DS_Store` et ceux commençant par `._` ne sont pas nécessaires au rendu.

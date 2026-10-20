
import tkinter as tk
from tkinter import messagebox
import os
from Balle import balle
from Raquette import raquette
from brique import Brique
from structures import Liste, Pile, File

POLICE = ("Times New Roman", 16)

class FenetreSecondaire:
    def __init__(self, menu, numero):
        self.menu = menu
        self.after_id = None
        self.fenetre = tk.Toplevel(menu.root)
        self.fenetre.title(f"Nivaux {numero}")
        self.fenetre.resizable(False, False)
        self.fenetre.geometry(f"{menu.largeur}x{menu.hauteur}")
        self.numero = numero

        self.canvas = tk.Canvas(self.fenetre, width=menu.largeur,
                                height=menu.hauteur, highlightthickness=0)
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=menu.photo, anchor="nw")

        self.canvas.create_text(menu.largeur // 2, 40,
                                text=f"Niveau {numero}",
                                fill="yellow", font=POLICE)

        bouton_retour = tk.Button(self.fenetre, text="Quitter",
                                  font=POLICE, command=self.retour)
        self.canvas.create_window(menu.largeur - 50, menu.hauteur - 40,
                                  window=bouton_retour)

        self.fenetre.protocol("WM_DELETE_WINDOW", self.retour)

        self.creer_jeu()   # 1. on crée la balle
        self.boucle()      # 2. on la fait bouger


    def creer_jeu(self):
        self.score = 0
        self.texte_score = self.canvas.create_text(
            10, 10, text="Score : 0", anchor="nw",
            fill="blue", font=POLICE)

        # Les vies sont rangées dans une PILE : une vie perdue = un depiler()
        self.vies = Pile()
        for i in range(3):
            self.vies.empiler(i)
        self.texte_vies = self.canvas.create_text(
            self.menu.largeur - 10, 10, text="Vies : 3", anchor="ne",
            fill="orange", font=POLICE)

        self.creer_briques()

        self.padel = raquette(self.canvas,
                           self.menu.largeur // 2,
                           self.menu.hauteur - 70)
        self.padel.activer_clavier(self.fenetre)

        self.en_attente = False
        self.nouvelle_balle()

    def nouvelle_balle(self):
        """Crée une balle au centre (ou la remplace si elle est perdue)."""
        if hasattr(self, "balle"):
            self.canvas.delete(self.balle.id)
        self.balle = balle(self.canvas,
                           self.menu.largeur // 2,
                           self.menu.hauteur - 130,
                           fichier="ball.png", taille=30)

    def creer_briques(self):
        largeur = self.menu.largeur
        nb_colonnes = 10
        nb_lignes = 2 + self.numero     # plus de lignes à chaque niveau
        marge, espace, hauteur = 20, 5, 20
        l_brique = (largeur - 2 * marge - (nb_colonnes - 1) * espace) // nb_colonnes

        # Les couleurs sont dans une FILE : on prend la première (defiler)
        # puis on la remet à la fin (enfiler) pour recommencer le cycle
        couleurs = File()
        for c in ["red"]:
            couleurs.enfiler(c)

        # Les briques sont dans une LISTE
        self.briques = Liste()
        for ligne in range(nb_lignes):
            couleur = couleurs.defiler()
            couleurs.enfiler(couleur)
            for col in range(nb_colonnes):
                x = marge + col * (l_brique + espace)
                y = 70 + ligne * (hauteur + espace)
                self.briques.ajouter(
                    Brique(self.canvas, x, y, l_brique, hauteur, couleur))

    def collision_briques(self):
        for brique in self.briques:
            if brique.toucher(self.balle):
                brique.detruire()
                self.briques.supprimer(brique)
                self.score += 10
                self.canvas.itemconfig(self.texte_score,
                                       text=f"Score : {self.score}")
                break   # une seule brique par image, évite les doubles rebonds

    def boucle(self):
        self.padel.deplacer()

        # Balle en attente : elle reste à sa place tant qu'on n'a pas
        # appuyé sur une touche de déplacement du padel
        if self.en_attente:
            if self.padel.touches & {"left", "q", "right", "d"}:
                self.en_attente = False
            else:
                self.after_id = self.fenetre.after(16, self.boucle)
                return

        if not self.balle.deplacer():
            self.vies.depiler()
            self.canvas.itemconfig(self.texte_vies,
                                   text=f"Vies : {self.vies.taille()}")
            if self.vies.est_vide():
                self.game_over()
                return
            self.nouvelle_balle()
            self.en_attente = True        # la balle attend une touche
            self.padel.touches.clear()    # oublie les touches déjà enfoncées
        self.padel.rebond(self.balle)
        self.collision_briques()
        if self.briques.est_vide():
            self.victoire()
            return
        self.after_id = self.fenetre.after(16, self.boucle)

    def victoire(self):
        self.after_id = None
        self.canvas.create_text(self.menu.largeur // 2,
                                self.menu.hauteur // 2,
                                text="VICTOIRE !",
                                fill="green",
                                font=("Times New Roman", 48, "bold"))

    def game_over(self):
        self.after_id = None
        self.canvas.create_text(self.menu.largeur // 2,
                                self.menu.hauteur // 2,
                                text="GAME OVER",
                                fill="red",
                                font=("Times New Roman", 48, "bold"))

    def retour(self):
        # On arrête l'animation avant de détruire la fenêtre
        if self.after_id is not None:
            self.fenetre.after_cancel(self.after_id)
        self.fenetre.destroy()
        self.menu.root.deiconify()

class interface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Casse Brique")
        self.root.resizable(False, False)

        dossier = os.path.dirname(os.path.abspath(__file__))
        self.photo = tk.PhotoImage(file=os.path.join(dossier, "fond.png"))

        # Réduction automatique si l'image dépasse l'écran
        ecran_l = self.root.winfo_screenwidth()
        ecran_h = self.root.winfo_screenheight() - 150
        facteur = 1
        while (self.photo.width() // facteur > ecran_l or
               self.photo.height() // facteur > ecran_h):
            facteur += 1
        if facteur > 1:
            self.photo = self.photo.subsample(facteur, facteur)

        self.largeur = self.photo.width()
        self.hauteur = self.photo.height()
        self.root.geometry(f"{self.largeur}x{self.hauteur}")

        self.canvas = tk.Canvas(self.root, width=self.largeur,
                                height=self.hauteur, highlightthickness=0)
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")

    def creer_menu(self):
        """Barre de menu en haut de la fenêtre (consigne : un menu avec options)."""
        barre = tk.Menu(self.root)

        menu_jeu = tk.Menu(barre, tearoff=0)
        for i in range(1, 4):
            menu_jeu.add_command(label=f"Niveau {i}",
                                 command=lambda n=i: self.ouvrir(n))
        menu_jeu.add_separator()
        menu_jeu.add_command(label="Quitter", command=self.quitter)
        barre.add_cascade(label="Jeu", menu=menu_jeu)

        menu_aide = tk.Menu(barre, tearoff=0)
        menu_aide.add_command(label="Règles", command=self.afficher_regles)
        barre.add_cascade(label="Aide", menu=menu_aide)

        self.root.config(menu=barre)

    def afficher_regles(self):
        messagebox.showinfo("Règles",
                            "Déplace la raquette avec les flèches (ou Q / D).\n"
                            "Détruis toutes les briques avec la balle.\n"
                            "Tu as 3 vies : si la balle tombe, tu en perds une.")

    def quitter(self):
        self.root.destroy()

    def boutons(self):
        self.creer_menu()
        for i in range(1, 4):
            bouton = tk.Button(self.root, text=f"Niveau {i}", font=POLICE,
                               command=lambda n=i: self.ouvrir(n))
            # Boutons répartis verticalement au centre
            self.canvas.create_window(self.largeur // 2,
                                      self.hauteur * i // 5,
                                      window=bouton)

        # Bouton pour quitter tout le jeu
        bouton_quitter = tk.Button(self.root, text="Quitter le jeu",
                                   font=POLICE, command=self.quitter)
        self.canvas.create_window(self.largeur // 2,
                                  self.hauteur * 4 // 5,
                                  window=bouton_quitter)

    def ouvrir(self, numero):
        self.root.withdraw()  # cache la fenêtre principale
        FenetreSecondaire(self, numero)

    def score(self):
        self.texte_score = self.canvas.create_text(
            10, 10, text="Score : 0", anchor="nw",
            fill="white", font=POLICE
        )

    def demarrer(self):
        self.root.mainloop()
    

if __name__ == "__main__":
    fenetre = interface()
    fenetre.boutons()
    fenetre.demarrer()
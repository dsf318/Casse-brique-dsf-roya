
import tkinter as tk
import os
from balle import Balle
from Padelorigine import Padel
from brique import Brique

POLICE = ("Times New Roman", 16)

class FenetreSecondaire:
    def __init__(self, menu, numero):
        self.menu = menu
        self.after_id = None
        self.fenetre = tk.Toplevel(menu.root)
        self.fenetre.title(f"Difficultés {numero}")
        self.fenetre.resizable(False, False)
        self.fenetre.geometry(f"{menu.largeur}x{menu.hauteur}")
        self.numero = numero

        self.canvas = tk.Canvas(self.fenetre, width=menu.largeur,
                                height=menu.hauteur, highlightthickness=0)
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=menu.photo, anchor="nw")

        self.canvas.create_text(menu.largeur // 2, 40,
                                text=f"Difficultés {numero}",
                                fill="white", font=POLICE)

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
            fill="white", font=POLICE)

        self.creer_briques()

        self.padel = Padel(self.canvas,
                           self.menu.largeur // 2,
                           self.menu.hauteur - 70)
        self.padel.activer_clavier(self.fenetre)

        self.balle = Balle(self.canvas,
                           self.menu.largeur // 2,
                           self.menu.hauteur - 130,
                           fichier="ball.png", taille=30)

    def creer_briques(self):
        largeur = self.menu.largeur
        nb_colonnes = 10
        nb_lignes = 2 + self.numero     # plus de lignes à chaque niveau
        marge, espace, hauteur = 20, 5, 20
        l_brique = (largeur - 2 * marge - (nb_colonnes - 1) * espace) // nb_colonnes
        couleurs = ["red", "orange", "yellow", "green", "cyan", "violet"]

        self.briques = []
        for ligne in range(nb_lignes):
            for col in range(nb_colonnes):
                x = marge + col * (l_brique + espace)
                y = 70 + ligne * (hauteur + espace)
                self.briques.append(
                    Brique(self.canvas, x, y, l_brique, hauteur,
                           couleurs[ligne % len(couleurs)]))

    def collision_briques(self):
        for brique in self.briques:
            if brique.toucher(self.balle):
                brique.detruire()
                self.briques.remove(brique)
                self.score += 10
                self.canvas.itemconfig(self.texte_score,
                                       text=f"Score : {self.score}")
                break   # une seule brique par image, évite les doubles rebonds

    def boucle(self):
        self.padel.deplacer()
        if not self.balle.deplacer():
            self.game_over()
            return
        self.padel.rebond(self.balle)
        self.collision_briques()
        if not self.briques:
            self.victoire()
            return
        self.after_id = self.fenetre.after(16, self.boucle)

    def victoire(self):
        self.after_id = None
        self.canvas.create_text(self.menu.largeur // 2,
                                self.menu.hauteur // 2,
                                text="VICTOIRE !",
                                fill="lime",
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

    def boutons(self):
        for i in range(1, 4):
            bouton = tk.Button(self.root, text=f"Niveau {i}", font=POLICE,
                               command=lambda n=i: self.ouvrir(n))
            # Boutons répartis verticalement au centre
            self.canvas.create_window(self.largeur // 2,
                                      self.hauteur * i// 4,
                                      window=bouton)

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

import tkinter as tk
import os
from balle import Balle
from Padelorigine import Padel

POLICE = ("Times New Roman", 16)

class FenetreSecondaire:
    def __init__(self, fenetre, numero):
        self.fenetre = fenetre
        self.after_id = None
        self.fenetre = tk.Toplevel(fenetre.root)
        self.fenetre.title(f"Difficultés {numero}")
        self.fenetre.resizable(False, False)
        self.fenetre.geometry(f"{fenetre.largeur}x{fenetre.hauteur}")

        self.canvas = tk.Canvas(self.fenetre, width=fenetre.largeur,
                                height=fenetre.hauteur, highlightthickness=0)
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=fenetre.photo, anchor="nw")

        self.canvas.create_text(fenetre.largeur // 2, 40,
                                text=f"Difficultés {numero}",
                                fill="white", font=POLICE)

        bouton_retour = tk.Button(self.fenetre, text="Quitter",
                                  font=POLICE, command=self.retour)
        self.canvas.create_window(fenetre.largeur - 50, fenetre.hauteur - 40,
                                  window=bouton_retour)

        self.fenetre.protocol("WM_DELETE_WINDOW", self.retour)

        self.creer_jeu()   # 1. on crée la balle
        self.boucle()      # 2. on la fait bouger

    def creer_jeu(self):
        self.balle = Balle(self.canvas,
                           self.fenetre.largeur // 2,
                           self.fenetre.hauteur - 60,
                           fichier="ball.png", taille=30)
        self.padel = Padel(self.canvas,
                           self.fenetre.largeur // 2,
                           self.fenetre.hauteur - 70)
        self.padel.activer_clavier(self.fenetre)

        # La balle démarre au-dessus du padel
        self.balle = Balle(self.canvas,
                           self.fenetre.largeur // 2,
                           self.fenetre.hauteur - 130,
                           fichier="ball.png", taille=30)

    def boucle(self):
        self.padel.deplacer()
        if not self.balle.deplacer():
            self.game_over()
            return
        self.padel.rebond(self.balle)
        self.after_id = self.fenetre.after(16, self.boucle)

    def game_over(self):
        self.after_id = None
        self.canvas.create_text(self.fenetre.largeur // 2,
                                self.fenetre.hauteur // 2,
                                text="GAME OVER",
                                fill="red",
                                font=("Times New Roman", 48, "bold"))

    def retour(self):
        # On arrête l'animation avant de détruire la fenêtre
        if self.after_id is not None:
            self.fenetre.after_cancel(self.after_id)
        self.fenetre.destroy()
        self.fenetre.root.deiconify()

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
    fenetre.score()
    fenetre.demarrer()
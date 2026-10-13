
import tkinter as tk
import os

POLICE = ("Times New Roman", 16)


class FenetreSecondaire:
    def __init__(self, parent, numero):
        self.parent = parent
        self.fenetre = tk.Toplevel(parent.root)
        self.fenetre.title(f"Difficultés{numero}")
        self.fenetre.resizable(False, False)
        self.fenetre.geometry(f"{parent.largeur}x{parent.hauteur}")

        # Même fond : on réutilise l'image du parent
        self.canvas = tk.Canvas(self.fenetre, width=parent.largeur,
                                height=parent.hauteur, highlightthickness=0)
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=parent.photo, anchor="nw")

        self.canvas.create_text(parent.largeur // 2, 40,
                                text=f"Difficultés {numero}",
                                fill="white", font=POLICE)

        # Bouton de retour
        bouton_retour = tk.Button(self.fenetre, text="Quitter ",
                                  font=POLICE, command=self.retour)
        self.canvas.create_window(parent.largeur -50, parent.hauteur - 40,
                                  window=bouton_retour)

        # Si on ferme avec la croix, on revient aussi à la fenêtre d'origine
        self.fenetre.protocol("WM_DELETE_WINDOW", self.retour)

    def retour(self):
        self.fenetre.destroy()
        self.parent.root.deiconify()  # réaffiche la fenêtre principale


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
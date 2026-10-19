import os
import tkinter as tk

from balle import Balle
from Padelorigine import Padel
from brique import Brique
from structures import Pile, File

POLICE = ("Times New Roman", 16)
DELAI = 16
POINTS_BRIQUE = 10


class Partie:
    def __init__(self, menu, numero):
        self.menu = menu
        self.numero = numero
        self.after_id = None
        self.message_id = None
        self.fenetre = tk.Toplevel(menu.root)
        self.fenetre.title(f"Casse-brique - Niveau {numero}")
        self.fenetre.resizable(False, False)
        self.fenetre.protocol("WM_DELETE_WINDOW", self.retour)

        self.canvas = tk.Canvas(self.fenetre, width=menu.largeur,
                                height=menu.hauteur, highlightthickness=0)
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=menu.photo, anchor="nw")
        self.canvas.create_text(menu.largeur // 2, 40,
                                text=f"Niveau {numero}",
                                fill="white", font=POLICE)
        bouton = tk.Button(self.fenetre, text="Retour au menu",
                           font=POLICE, command=self.retour)
        self.canvas.create_window(menu.largeur - 110, menu.hauteur - 30,
                                  window=bouton)

        self.creer_jeu()
        self.afficher_message()
        self.boucle()

    def creer_jeu(self):
        self.score = 0
        self.vies = Pile()
        for numero in range(1, 4):
            self.vies.empiler(numero)
        self.messages = File()
        self.messages.enfiler("Début de partie")
        self.texte_score = self.canvas.create_text(
            10, 10, text="Score : 0", anchor="nw", fill="white", font=POLICE)
        self.texte_vies = self.canvas.create_text(
            self.menu.largeur - 10, 10, text="Vies : 3", anchor="ne",
            fill="white", font=POLICE)
        self.texte_message = self.canvas.create_text(
            10, self.menu.hauteur - 30, anchor="w", fill="white", font=POLICE)
        self.creer_briques()
        self.padel = Padel(self.canvas, self.menu.largeur // 2,
                           self.menu.hauteur - 70)
        self.balle = Balle(self.canvas, self.menu.largeur // 2,
                           self.menu.hauteur - 130)
        self.padel.activer_clavier(self.fenetre)

    def creer_briques(self):
        nb_colonnes = 10
        nb_lignes = 2 + self.numero
        marge = 20
        espace = 5
        hauteur = 20
        place = self.menu.largeur - 2 * marge - (nb_colonnes - 1) * espace
        largeur = place // nb_colonnes
        couleurs = ["red", "orange", "yellow", "green", "cyan"]
        self.briques = []
        for ligne in range(nb_lignes):
            for colonne in range(nb_colonnes):
                x = marge + colonne * (largeur + espace)
                y = 70 + ligne * (hauteur + espace)
                brique = Brique(self.canvas, x, y, largeur, hauteur,
                                couleurs[ligne])
                self.briques.append(brique)

    def collision_briques(self):
        for brique in self.briques:
            if brique.toucher(self.balle):
                brique.detruire()
                self.briques.remove(brique)
                self.score += POINTS_BRIQUE
                self.canvas.itemconfig(self.texte_score,
                                       text=f"Score : {self.score}")
                break

    def perdre_vie(self):
        self.vies.depiler()
        self.canvas.itemconfig(self.texte_vies,
                               text=f"Vies : {self.vies.taille()}")
        self.messages.enfiler("Une vie perdue")
        if self.vies.est_vide():
            self.terminer("DÉFAITE", "red")
            return
        self.balle.replacer(self.menu.largeur // 2, self.menu.hauteur - 130)
        self.padel.replacer(self.menu.largeur // 2, self.menu.hauteur - 70)
        self.after_id = self.fenetre.after(1000, self.boucle)

    def boucle(self):
        self.after_id = None
        self.padel.deplacer()
        if not self.balle.deplacer():
            self.perdre_vie()
            return
        self.padel.rebond(self.balle)
        self.collision_briques()
        if not self.briques:
            self.terminer("VICTOIRE !", "lime")
            return
        self.after_id = self.fenetre.after(DELAI, self.boucle)

    def afficher_message(self):
        # Les messages sont retirés dans leur ordre d'arrivée (file).
        texte = ""
        if not self.messages.est_vide():
            texte = self.messages.defiler()
        self.canvas.itemconfig(self.texte_message, text=texte)
        self.message_id = self.fenetre.after(1500, self.afficher_message)

    def terminer(self, texte, couleur):
        self.messages.enfiler(texte)
        self.canvas.create_text(self.menu.largeur // 2,
                                self.menu.hauteur // 2, text=texte,
                                fill=couleur, font=("Times New Roman", 48, "bold"))

    def retour(self):
        if self.after_id is not None:
            self.fenetre.after_cancel(self.after_id)
        if self.message_id is not None:
            self.fenetre.after_cancel(self.message_id)
        self.fenetre.destroy()
        self.menu.root.deiconify()


class MenuPrincipal:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Casse-brique")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)
        dossier = os.path.dirname(os.path.abspath(__file__))
        self.photo = tk.PhotoImage(file=os.path.join(dossier, "fond.png"))
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
        self.canvas = tk.Canvas(self.root, width=self.largeur,
                                height=self.hauteur, highlightthickness=0)
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
        self.boutons()

    def boutons(self):
        self.niveau = tk.IntVar(value=1)
        self.canvas.create_text(self.largeur // 2, self.hauteur // 6,
                                text="CASSE-BRIQUE", fill="white",
                                font=("Times New Roman", 28, "bold"))
        choix = tk.Frame(self.root)
        for numero in range(1, 4):
            bouton = tk.Radiobutton(choix, text=f"Niveau {numero}",
                                    variable=self.niveau, value=numero,
                                    font=POLICE)
            bouton.pack(side="left")
        self.canvas.create_window(self.largeur // 2, self.hauteur // 3,
                                  window=choix)
        bouton = tk.Button(self.root, text="Démarrer", font=POLICE,
                           command=self.ouvrir)
        self.canvas.create_window(self.largeur // 2, self.hauteur // 2,
                                  window=bouton)
        bouton = tk.Button(self.root, text="Quitter", font=POLICE,
                           command=self.root.destroy)
        self.canvas.create_window(self.largeur // 2, self.hauteur * 2 // 3,
                                  window=bouton)
        self.canvas.create_text(self.largeur // 2, self.hauteur * 5 // 6,
                                text="Déplacement : flèches gauche/droite ou Q/D",
                                fill="white", font=POLICE)

    def ouvrir(self):
        Partie(self, self.niveau.get())
        self.root.withdraw()

    def demarrer(self):
        self.root.mainloop()


if __name__ == "__main__":
    menu = MenuPrincipal()
    menu.demarrer()

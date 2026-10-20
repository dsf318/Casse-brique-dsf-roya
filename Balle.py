import os
import tkinter as tk


class balle:
    def __init__(self, canvas, x, y, fichier="ball.png", taille=30):
        self.canvas = canvas
        self.dx = 4
        self.dy = -4

        dossier = os.path.dirname(os.path.abspath(__file__))
        self.photo = tk.PhotoImage(file=os.path.join(dossier, fichier))

        # Réduction automatique pour approcher la taille voulue (en pixels)
        facteur = max(1, round(self.photo.width() / taille))
        if facteur > 1:
            self.photo = self.photo.subsample(facteur, facteur)

        self.id = canvas.create_image(x, y, image=self.photo)

    def deplacer(self):
        """Déplace la balle. Renvoie False si elle touche le bas (perdu)."""
        self.canvas.move(self.id, self.dx, self.dy)
        x1, y1, x2, y2 = self.canvas.bbox(self.id)
        largeur = int(self.canvas["width"])
        hauteur = int(self.canvas["height"])

        # Rebond sur les murs gauche/droite et le plafond
        if x1 <= 0:
            self.dx = abs(self.dx)
        if x2 >= largeur:
            self.dx = -abs(self.dx)
        if y1 <= 0:
            self.dy = abs(self.dy)

        # Le bas = game over
        if y2 >= hauteur:
            return False
        return True
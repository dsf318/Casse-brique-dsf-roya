class Balle:
    def __init__(self, canvas, x, y, taille=20):
        self.canvas = canvas
        self.rayon = taille / 2
        self.dx = 4
        self.dy = -4
        self.id = canvas.create_oval(
            x - self.rayon, y - self.rayon,
            x + self.rayon, y + self.rayon,
            fill="white", outline="")
        self.ancienne_position = self.canvas.coords(self.id)

    def replacer(self, x, y):
        self.canvas.coords(self.id,
                           x - self.rayon, y - self.rayon,
                           x + self.rayon, y + self.rayon)
        self.dx = 4
        self.dy = -4
        self.ancienne_position = self.canvas.coords(self.id)

    def deplacer(self):
        """Renvoie False lorsque la balle touche le bas du canevas."""
        self.ancienne_position = self.canvas.coords(self.id)
        self.canvas.move(self.id, self.dx, self.dy)
        x1, y1, x2, y2 = self.canvas.coords(self.id)
        largeur = int(self.canvas["width"])
        hauteur = int(self.canvas["height"])

        if x1 <= 0:
            self.canvas.move(self.id, -x1, 0)
            self.dx = abs(self.dx)
        elif x2 >= largeur:
            self.canvas.move(self.id, largeur - x2, 0)
            self.dx = -abs(self.dx)
        if y1 <= 0:
            self.canvas.move(self.id, 0, -y1)
            self.dy = abs(self.dy)

        return y2 < hauteur

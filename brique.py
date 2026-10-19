class Brique:
    def __init__(self, canvas, x, y, largeur=60, hauteur=20, couleur="red"):
        self.canvas = canvas
        self.id = canvas.create_rectangle(x, y, x + largeur, y + hauteur,
                                          fill=couleur, outline="white")

    def toucher(self, balle):
        """Renvoie True si la balle touche la brique, et la fait rebondir."""
        bx1, by1, bx2, by2 = self.canvas.coords(balle.id)
        x1, y1, x2, y2 = self.canvas.coords(self.id)

        # Pas de contact
        if bx2 < x1 or bx1 > x2 or by2 < y1 or by1 > y2:
            return False

        ancien_x1, ancien_y1, ancien_x2, ancien_y2 = balle.ancienne_position

        # On regarde de quel côté venait la balle avant son déplacement.
        if ancien_y2 <= y1 or ancien_y1 >= y2:
            balle.dy = -balle.dy
        elif ancien_x2 <= x1 or ancien_x1 >= x2:
            balle.dx = -balle.dx
        else:
            balle.dy = -balle.dy
        return True

    def detruire(self):
        self.canvas.delete(self.id)
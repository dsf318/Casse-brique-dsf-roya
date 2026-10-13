class Brique:
    def __init__(self, canvas, x, y, largeur=60, hauteur=20, couleur="red"):
        self.canvas = canvas
        self.id = canvas.create_rectangle(x, y, x + largeur, y + hauteur,
                                          fill=couleur, outline="white")

    def toucher(self, balle):
        """Renvoie True si la balle touche la brique, et la fait rebondir."""
        bx1, by1, bx2, by2 = self.canvas.bbox(balle.id)
        x1, y1, x2, y2 = self.canvas.coords(self.id)

        # Pas de contact
        if bx2 < x1 or bx1 > x2 or by2 < y1 or by1 > y2:
            return False

        # Taille du chevauchement sur chaque axe
        chevauche_x = min(bx2, x2) - max(bx1, x1)
        chevauche_y = min(by2, y2) - max(by1, y1)

        centre_bx = (bx1 + bx2) / 2
        centre_by = (by1 + by2) / 2
        centre_x = (x1 + x2) / 2
        centre_y = (y1 + y2) / 2

        if chevauche_x < chevauche_y:
            # Touchée sur un côté : on inverse dx, en forçant la bonne direction
            if centre_bx < centre_x:
                balle.dx = -abs(balle.dx)
            else:
                balle.dx = abs(balle.dx)
        else:
            # Touchée dessus ou dessous : on inverse dy
            if centre_by < centre_y:
                balle.dy = -abs(balle.dy)
            else:
                balle.dy = abs(balle.dy)
        return True

    def detruire(self):
        self.canvas.delete(self.id)
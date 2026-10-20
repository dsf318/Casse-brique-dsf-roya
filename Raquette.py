
class raquette:
    def __init__(self, canvas, x, y, largeur=100, hauteur=15,
                 vitesse=8, couleur="white"):
        self.canvas = canvas
        self.largeur = largeur
        self.vitesse = vitesse
        self.touches = set()  # touches actuellement enfoncées

        # (x, y) = centre du haut du padel
        self.id = canvas.create_rectangle(
            x - largeur // 2, y,
            x + largeur // 2, y + hauteur,
            fill=couleur, outline=""
        )

    def activer_clavier(self, fenetre):
        """Relie le clavier à la fenêtre du niveau."""
        fenetre.bind("<KeyPress>", self.appui)
        fenetre.bind("<KeyRelease>", self.relache)
        fenetre.focus_force()  # la fenêtre doit avoir le focus pour lire le clavier

    def appui(self, event):
        self.touches.add(event.keysym.lower())

    def relache(self, event):
        self.touches.discard(event.keysym.lower())

    def deplacer(self):
        """Déplace le padel selon les touches enfoncées (flèches ou Q / D)."""
        dx = 0
        if self.touches & {"left", "q"}:
            dx -= self.vitesse
        if self.touches & {"right", "d"}:
            dx += self.vitesse

        x1, y1, x2, y2 = self.canvas.coords(self.id)
        largeur_canvas = int(self.canvas["width"])

        # Empêche le padel de sortir de la fenêtre
        if x1 + dx < 0:
            dx = -x1
        if x2 + dx > largeur_canvas:
            dx = largeur_canvas - x2

        self.canvas.move(self.id, dx, 0)

    def rebond(self, balle):
        bx1, by1, bx2, by2 = self.canvas.bbox(balle.id)
        px1, py1, px2, py2 = self.canvas.coords(self.id)

        if (balle.dy > 0 and bx2 >= px1 and bx1 <= px2
                and by2 >= py1 and by1 <= py2):
            self.canvas.move(balle.id, 0, py1 - by2)

            # Loi de Descartes : l'angle de rebond = l'angle d'arrivée.
            # Seul dy s'inverse, dx est conservé : la vitesse ne change pas.
            balle.dy = -abs(balle.dy)

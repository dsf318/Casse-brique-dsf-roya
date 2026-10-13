
class Padel:
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

        self.effet = 6      # force de l'effet (0 = miroir pur)
        self.dx_max = 7     # vitesse horizontale maximale

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

            # 1. Effet miroir : dy s'inverse, dx est conservé
            balle.dy = -abs(balle.dy)

            # 2. Effet du padel : décalage selon la zone touchée (-1 à +1)
            centre_balle = (bx1 + bx2) / 2
            centre_padel = (px1 + px2) / 2
            ratio = (centre_balle - centre_padel) / (self.largeur / 2)
            ratio = max(-1, min(1, ratio))
            balle.dx += ratio * self.effet

            # 3. Limiter dx pour éviter les angles trop plats
            balle.dx = max(-self.dx_max, min(self.dx_max, balle.dx))

class Padel:
    def __init__(self, canvas, x, y, largeur=100, hauteur=15,
                 vitesse=8, couleur="white"):
        self.canvas = canvas
        self.largeur = largeur
        self.vitesse = vitesse
        self.touches = []  # touches actuellement enfoncées

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
        fenetre.bind("<FocusOut>", self.perdre_focus)
        fenetre.focus_force()  # la fenêtre doit avoir le focus pour lire le clavier

    def appui(self, event):
        touche = event.keysym.lower()
        if touche not in self.touches:
            self.touches.append(touche)

    def relache(self, event):
        touche = event.keysym.lower()
        if touche in self.touches:
            self.touches.remove(touche)

    def perdre_focus(self, event):
        self.touches.clear()

    def replacer(self, x, y):
        x1, y1, x2, y2 = self.canvas.coords(self.id)
        self.canvas.move(self.id, x - (x1 + x2) / 2, y - y1)
        self.touches.clear()

    def deplacer(self):
        """Déplace le padel selon les touches enfoncées (flèches ou Q / D)."""
        dx = 0
        if "left" in self.touches or "q" in self.touches:
            dx -= self.vitesse
        if "right" in self.touches or "d" in self.touches:
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
        bx1, by1, bx2, by2 = self.canvas.coords(balle.id)
        px1, py1, px2, py2 = self.canvas.coords(self.id)

        ancien_bas = balle.ancienne_position[3]

        if (balle.dy > 0 and ancien_bas <= py1 and by2 >= py1
                and bx2 >= px1 and bx1 <= px2):
            self.canvas.move(balle.id, 0, py1 - by2)

            # Sur une surface horizontale, seule la vitesse verticale change.
            balle.dy = -abs(balle.dy)

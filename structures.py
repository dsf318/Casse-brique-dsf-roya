"""
Fait par : Da Silva Ferraz Alexis
Objectif : les 3 structures de données demandées dans le TP
           (une liste, une pile et une file), écrites "à la main"
           avec des maillons (sans utiliser list ni deque).
"""


class Maillon:
    """Une case de la chaîne : une valeur + un lien vers la case suivante."""
    def __init__(self, valeur):
        self.valeur = valeur
        self.suivant = None


class Liste:
    def __init__(self):
        self.debut = None

    def est_vide(self):
        return self.debut is None

    def ajouter(self, valeur):
        """Ajoute la valeur à la fin de la liste."""
        nouveau = Maillon(valeur)
        if self.debut is None:
            self.debut = nouveau
        else:
            courant = self.debut
            while courant.suivant is not None:
                courant = courant.suivant
            courant.suivant = nouveau

    def supprimer(self, valeur):
        """Supprime la première case qui contient la valeur."""
        precedent = None
        courant = self.debut
        while courant is not None:
            if courant.valeur is valeur:
                if precedent is None:
                    self.debut = courant.suivant
                else:
                    precedent.suivant = courant.suivant
                return True
            precedent = courant
            courant = courant.suivant
        return False

    def __iter__(self):
        """Permet d'écrire : for x in ma_liste"""
        courant = self.debut
        while courant is not None:
            yield courant.valeur
            courant = courant.suivant



class Pile:
    def __init__(self):
        self.sommet = None
        self.nombre = 0

    def est_vide(self):
        return self.sommet is None

    def taille(self):
        return self.nombre

    def empiler(self, valeur):
        nouveau = Maillon(valeur)
        nouveau.suivant = self.sommet
        self.sommet = nouveau
        self.nombre += 1

    def depiler(self):
        """Enlève et renvoie le dernier élément ajouté."""
        if self.sommet is None:
            return None
        valeur = self.sommet.valeur
        self.sommet = self.sommet.suivant
        self.nombre -= 1
        return valeur



class File:
    def __init__(self):
        self.tete = None     # le prochain à sortir
        self.queue = None    # le dernier arrivé

    def est_vide(self):
        return self.tete is None

    def enfiler(self, valeur):
        nouveau = Maillon(valeur)
        if self.queue is None:
            self.tete = nouveau
        else:
            self.queue.suivant = nouveau
        self.queue = nouveau

    def defiler(self):
        """Enlève et renvoie le plus ancien élément."""
        if self.tete is None:
            return None
        valeur = self.tete.valeur
        self.tete = self.tete.suivant
        if self.tete is None:
            self.queue = None
        return valeur

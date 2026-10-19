class Pile:
    """Le dernier élément ajouté est le premier retiré """

    def __init__(self):
        self.elements = []

    def empiler(self, element):
        self.elements.append(element)

    def depiler(self):
        if not self.est_vide():
            return self.elements.pop()

    def est_vide(self):
        return len(self.elements) == 0

    def taille(self):
        return len(self.elements)


class File:
    """Le premier élément ajouté est le premier retiré """

    def __init__(self):
        self.elements = []

    def enfiler(self, element):
        self.elements.append(element)

    def defiler(self):
        if not self.est_vide():
            return self.elements.pop(0)

    def est_vide(self):
        return len(self.elements) == 0

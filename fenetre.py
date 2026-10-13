import tkinter as tk

class interface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Casse Brique")
        self.root.geometry("800x400")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(self.root, width=800, height=400, bg="black")
        self.canvas.pack()


    def score(self):
        heading = tk.Frame(self.root)
        heading.pack()
        tk.Label(heading, text="Score : ").pack()

    def demarrer(self):
        self.root.mainloop()

if __name__ == "__main__":
    fenetre = interface()
    fenetre.score()
    fenetre.demarrer()


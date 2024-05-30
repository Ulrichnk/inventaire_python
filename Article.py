
from datetime import datetime
import csv
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class Article:
    def __init__(self, id_article, nom, prix_achat, prix_vente, date_ajout):
        self.id_article = id_article
        self.nom = nom
        self.prix_achat = prix_achat
        self.prix_vente = prix_vente
        self.date_ajout = date_ajout or datetime.now()

    def __eq__(self, other):
        if (self.id_article == other.id_article and
            self.nom.lower() == other.nom.lower() and
            self.prix_achat == other.prix_achat and
                self.prix_vente == other.prix_vente):
            return True
        else:
            return False


class Vente:
    def __init__(self, article, nb_vente, date):
        self.article = article
        self.nb_vente = nb_vente
        self.date = date

    def __add__(self, other):
        return Vente(self.article, self.nb_vente+other.nb_vente)

    def __sub__(self, other):
        return Vente(self.article, self.nb_vente-other.nb_vente)


class Achat:
    def __init__(self, article, nb_achat):
        self.article = article
        self.nb_achat = nb_achat

    def __add__(self, other):
        return Achat(self.article, self.nb_achat + other.nb_achat)

    def __sub__(self, other):
        return Achat(self.article, self.nb_achat - other.nb_achat)


class GestionStock:

    FILENAME_ARTICLES = "articles.csv"
    FILENAME_VENTES = "ventes.csv"
    FILENAME_ACHATS = "achats.csv"

    def __init__(self):
        self.articles = []
        self.ventes = []
        self.achats = []
        self.charger_articles()
        self.charger_ventes()
        self.charger_achats()

    def charger_articles(self):
        try:
            with open(self.FILENAME_ARTICLES, "r", newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    article = Article(int(row["id_article"]), row["nom"], float(row["prix_achat"]), float(
                        row["prix_vente"]), int(row["stock"]), row["date_ajout"])
                    self.articles.append(article)
        except FileNotFoundError:
            pass

    def charger_ventes(self):
        try:
            with open(self.FILENAME_VENTES, "r", newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    vente = {"id_article": int(row["id_article"]), "nb_ventes": int(
                        row["nb_ventes"]), "date": datetime.strptime(row["date"], "%Y-%m-%d %H:%M:%S")}
                    self.ventes.append(vente)
        except FileNotFoundError:
            pass

    def charger_achats(self):
        try:
            with open(self.FILENAME_ACHATS, "r", newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    achat = {"id_article": int(row["id_article"]), "nb_achats": int(
                        row["nb_achats"]), "date": datetime.strptime(row["date"], "%Y-%m-%d %H:%M:%S")}
                    self.achats.append(achat)
        except FileNotFoundError:
            pass


class StockApp():
    def __init__(self):
        super().__init__()
        self.title("Gestion de Stock")
        self.geometry("800x600")
        self.gestion_stock = GestionStock()
        self.create_widgets()

    def create_widgets(self):
        # Notebook for the tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        # Create frames for each tab
        self.frame_articles = ttk.Frame(self.notebook)
        self.frame_ajout_vente = ttk.Frame(self.notebook)
        self.frame_ajout_achat = ttk.Frame(self.notebook)
        self.frame_inventaire = ttk.Frame(self.notebook)

        # Add tabs to the notebook
        self.notebook.add(self.frame_articles, text="Articles")
        self.notebook.add(self.frame_ajout_vente, text="Ajouter Vente")
        self.notebook.add(self.frame_ajout_achat, text="Ajouter Achat")
        self.notebook.add(self.frame_inventaire, text="Inventaire")

        # Create widgets for each tab
        self.create_articles_widgets()
        self.create_ajout_vente_widgets()
        self.create_ajout_achat_widgets()
        self.create_inventaire_widgets()


if __name__ == "__main__":
    app = StockApp()
    app.mainloop()

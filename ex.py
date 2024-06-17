from datetime import datetime
import csv
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class Article:
    
    def __init__(self, id_article, nom, prix_vente, prix_achat, stock=0, date=None):
        if prix_vente <= 0 or prix_achat <= 0:
            raise ValueError("Les prix de vente et d'achat doivent être supérieurs à zéro.")
        self.id_article = id_article
        self.nom = nom
        self.prix_vente = prix_vente
        self.prix_achat = prix_achat
        self.stock = stock
        self.date = date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __eq__(self, other):
        return (isinstance(other, Article) and
                self.id_article == other.id_article and
                self.nom == other.nom and
                self.prix_vente == other.prix_vente and
                self.prix_achat == other.prix_achat)

    def __str__(self):
        return (f"{self.id_article}: {self.nom} - Vente: {self.prix_vente} - Achat: {self.prix_achat} - "
                f"Stock: {self.stock} - Date d'ajout: {self.date}")


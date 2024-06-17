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
                    article = Article(int(row["id_article"]), row["nom"], float(
                        row["prix_vente"]), float(row["prix_achat"]), int(row["stock"]), row["date"])
                    self.articles.append(article)
        except FileNotFoundError:
            pass

    def charger_ventes(self):
        self._charger_transactions(self.FILENAME_VENTES, self.ventes)

    def charger_achats(self):
        self._charger_transactions(self.FILENAME_ACHATS, self.achats)

    def _charger_transactions(self, filename, transaction_list):
        try:
            with open(filename, "r", newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    transaction = {
                        "id_article": int(row["id_article"]),
                        "quantite":float(row["quantite"]),
                        "date": datetime.strptime(row["date"], "%Y-%m-%d %H:%M:%S")
                    }
                    transaction_list.append(transaction)
        except FileNotFoundError:
            pass

    def sauvegarder_articles(self):
        self._sauvegarder(self.FILENAME_ARTICLES, self.articles, ["id_article", "nom", "prix_vente", "prix_achat", "stock", "date"])

    def sauvegarder_ventes(self):
        print(self.ventes[0])
        self._sauvegarder(self.FILENAME_VENTES, self.ventes, ["id_article", "quantite", "date"])

    def sauvegarder_achats(self):
        self._sauvegarder(self.FILENAME_ACHATS, self.achats, ["id_article", "quantite", "date"])

    def _sauvegarder(self, filename, data_list, fieldnames):
        with open(filename, "w", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for item in data_list:
                row = {field: getattr(item, field) if hasattr(item, field) else item[field] for field in fieldnames}
                row["date"] = row["date"].strftime("%Y-%m-%d %H:%M:%S") if isinstance(row["date"], datetime) else row["date"]
                writer.writerow(row)

    def ajouter_article(self, nom, prix_vente, prix_achat):
        id_article = len(self.articles) + 1
        article = Article(id_article, nom, prix_vente, prix_achat)

        if article in self.articles:
            return False

        self.articles.append(article)
        self.sauvegarder_articles()
        return True

    def supprimer_article(self, id_article):
        article_to_remove = next((article for article in self.articles if article.id_article == id_article), None)
        if article_to_remove:
            self.articles.remove(article_to_remove)
            self.sauvegarder_articles()
            return True
        return False

    def modifier_article(self, id_article, nom=None, prix_vente=None, prix_achat=None):
        article = next((article for article in self.articles if article.id_article == id_article), None)
        if article:
            if nom:
                article.nom = nom
            if prix_vente:
                article.prix_vente = prix_vente
            if prix_achat:
                article.prix_achat = prix_achat
            self.sauvegarder_articles()
            return True
        return False

    def modifier_vente(self, id_article, quantite, date):
        print(date)
        # date=datetime.strptime(date,"%Y-%m-%d %H:%M:%S")
        date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
        date= date_obj.strftime("%Y-%m-%d %H:%M:%S")

        vente = next((vente for vente in self.ventes if vente["id_article"] == id_article and vente["date"].strftime("%Y-%m-%d %H:%M:%S")==date), None)
        # print(vente)
        if vente:
            vente["id_article"]=id_article
            vente["quantite"]=quantite
            vente["date"]=datetime.now()
            self.sauvegarder_ventes()
            print(vente)
            return True
        return False
    def modifier_achat(self, id_article, quantite, date):
        # Trouver l'achat correspondant
        date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
        date= date_obj.strftime("%Y-%m-%d %H:%M:%S")
        achat = next((achat for achat in self.achats if achat["id_article"] == id_article and achat["date"].strftime("%Y-%m-%d %H:%M:%S") == date), None)
        print(achat)

        if achat and quantite:
            # Mettre à jour les champs de l'achat
            achat["id_article"] = id_article
            achat["quantite"] = quantite
            achat["date"] = datetime.now()
            self.sauvegarder_achats()
            print(achat)
            return True

        return False


    def rechercher_article(self, id_article):
        return next((article for article in self.articles if article.id_article == id_article), None)

    def rechercher_article_par_nom(self, nom):
        # return [article for article in self.articles if nom.lower() in article.nom.lower()]
        resultats = []
        # for nom in liste_noms:
        #     if nom.startswith(noms_recherche):
        #         resultats.append(nom)
        # return resultats
        for article in self.articles:
            if article.nom.lower().startswith(nom):
                resultats.append(article)
        return resultats

    def lister_articles(self):
        return self.articles

    def lister_ventes(self):
        return self.ventes

    def lister_achats(self):
        return self.achats

    def enregistrer_vente(self, nom, prix_vente, prix_achat, quantite):
        article = next((article for article in self.articles if article.nom == nom and article.prix_vente == prix_vente and article.prix_achat == prix_achat), None)
        if article:
            vente = {"id_article": article.id_article, "quantite": quantite, "date": datetime.now()}
            self.ventes.append(vente)
            self.sauvegarder_ventes()
            return True
        return False

    def enregistrer_achat(self, nom, prix_vente, prix_achat, quantite):
        article = next((article for article in self.articles if article.nom == nom and article.prix_vente == prix_vente and article.prix_achat == prix_achat), None)
        if article:
            achat = {"id_article": article.id_article, "quantite": quantite, "date": datetime.now()}
            self.achats.append(achat)
            self.sauvegarder_achats()
            return True
        return False

    def rapport_inventaire(self, date_debut, date_fin):
        ventes = [vente for vente in self.ventes if date_debut <= vente["date"] <= date_fin]
        achats = [achat for achat in self.achats if date_debut <= achat["date"] <= date_fin]

        rapport = {}

        for vente in ventes:
            article = self.rechercher_article(vente["id_article"])
            if article:
                if article.nom not in rapport:
                    rapport[article.nom] = {"vente": 0, "achat": 0, "valeur_vente": 0, "valeur_achat": 0,
                                            "prix_vente": article.prix_vente, "prix_achat": article.prix_achat}
                rapport[article.nom]["vente"] += vente["quantite"]
                rapport[article.nom]["valeur_vente"] += vente["quantite"] * article.prix_vente

        for achat in achats:
            article = self.rechercher_article(achat["id_article"])
            if article:
                if article.nom not in rapport:
                    rapport[article.nom] = {"vente": 0, "achat": 0, "valeur_vente": 0, "valeur_achat": 0,
                                            "prix_vente": article.prix_vente, "prix_achat": article.prix_achat}
                rapport[article.nom]["achat"] += achat["quantite"]
                rapport[article.nom]["valeur_achat"] += achat["quantite"] * article.prix_achat

        return rapport


class StockApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion de Stock")
        self.geometry("800x600")
        self.gestion_stock = GestionStock()
        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        self.frame_articles = ttk.Frame(self.notebook)

        self.frame_ajout_vente = ttk.Frame(self.notebook)
        self.frame_ajout_achat = ttk.Frame(self.notebook)
        self.frame_inventaire = ttk.Frame(self.notebook)

        self.notebook.add(self.frame_articles, text="Articles")
        self.notebook.add(self.frame_ajout_vente, text="Ajouter Vente")
        self.notebook.add(self.frame_ajout_achat, text="Ajouter Achat")
        self.notebook.add(self.frame_inventaire, text="Inventaire")

        self.create_articles_widgets()
        self.create_ajout_vente_widgets()
        self.create_ajout_achat_widgets()
        self.create_inventaire_widgets()

    def create_articles_widgets(self):
        # self.frame_articles.grid(row=0, column=0, padx=50, pady=50)

        lbl_nom_article = ttk.Label(self.frame_articles, text="Nom de l'article:")
        lbl_nom_article.grid(row=0, column=0, sticky=tk.E)
        self.ent_nom_article = ttk.Entry(self.frame_articles)
        self.ent_nom_article.grid(row=0, column=1, sticky=tk.W)

        lbl_prix_vente = ttk.Label(self.frame_articles, text="Prix de vente:")
        lbl_prix_vente.grid(row=1, column=0, sticky=tk.E)
        self.ent_prix_vente = ttk.Entry(self.frame_articles)
        self.ent_prix_vente.grid(row=1, column=1, sticky=tk.W)

        lbl_prix_achat = ttk.Label(self.frame_articles, text="Prix d'achat:")
        lbl_prix_achat.grid(row=2, column=0, sticky=tk.E)
        self.ent_prix_achat = ttk.Entry(self.frame_articles)
        self.ent_prix_achat.grid(row=2, column=1, sticky=tk.W)

        lbl_quantite_aa1 = ttk.Label(self.frame_articles, text="Quantité:")
        lbl_quantite_aa1.grid(row=3, column=3, sticky=tk.E)
        self.ent_quantite_aa1 = ttk.Entry(self.frame_articles)
        self.ent_quantite_aa1.grid(row=3, column=4, sticky=tk.W)

        btn_ajouter_article = ttk.Button(self.frame_articles, text="Ajouter", command=self.add_article)
        btn_ajouter_article.grid(row=3, column=0)

        btn_modifier_article = ttk.Button(self.frame_articles, text="Modifier", command=self.modify_article)
        btn_modifier_article.grid(row=3, column=1)

        btn_supprimer_article = ttk.Button(self.frame_articles, text="Supprimer", command=self.delete_article)
        btn_supprimer_article.grid(row=3, column=2)

        btn_enregistrer_vente1 = ttk.Button(self.frame_articles, text="Enregistrer Vente", command=self.enregistrer_vente1)
        btn_enregistrer_vente1.grid(row=3, column=5)

        btn_enregistrer_achat1 = ttk.Button(self.frame_articles, text="Enregistrer achat", command=self.enregistrer_achat1)
        btn_enregistrer_achat1.grid(row=3, column=6)


        btn_rechercher = ttk.Button(self.frame_articles, text="rechercher", command=self.fct_rechercher)
        btn_rechercher.grid(row=0, column=3)
        self.ent_rechercher = ttk.Entry(self.frame_articles)
        self.ent_rechercher.grid(row=1, column=3, sticky=tk.W)

        self.tree_articles = ttk.Treeview(self.frame_articles, columns=("ID", "Nom", "Prix de Vente", "Prix d'Achat", "Stock", "Date d'Ajout"), show="headings")
        self.tree_articles.grid(row=5, column=0, columnspan=8, sticky="nsew")
        self.tree_articles.heading("ID", text="ID")
        self.tree_articles.heading("Nom", text="Nom")
        self.tree_articles.heading("Prix de Vente", text="Prix de Vente")
        self.tree_articles.heading("Prix d'Achat", text="Prix d'Achat")
        self.tree_articles.heading("Stock", text="Stock")
        self.tree_articles.heading("Date d'Ajout", text="Date d'Ajout")

        self.frame_articles.grid_columnconfigure(7, weight=1)
        self.frame_articles.grid_rowconfigure(5, weight=1)

        self.update_articles_listbox()

    def fct_rechercher(self):
        result=[]
        try:
            nom=self.ent_rechercher.get()
            result=self.gestion_stock.rechercher_article_par_nom(nom)
            if result:
                    self.update_articles_listbox(result)
                    self.ent_nom_article.delete(0, tk.END)
                    self.ent_prix_vente.delete(0, tk.END)
                    self.ent_prix_achat.delete(0, tk.END)
                    # messagebox.showinfo("Succès", "Article ajouté avec succès.")
            else:
                    messagebox.showerror("Erreur", "L'article introuvable.")
        except ValueError:
            messagebox.showerror("Erreur", "Aucun article trouvé.")
        return result

    def create_ajout_vente_widgets(self):
        # lbl_nom_article_va = ttk.Label(self.frame_ajout_vente, text="Nom de l'article:")
        # lbl_nom_article_va.grid(row=0, column=0, sticky=tk.E)
        # self.ent_nom_article_va = ttk.Entry(self.frame_ajout_vente)
        # self.ent_nom_article_va.grid(row=0, column=1, sticky=tk.W)

        # lbl_prix_vente_va = ttk.Label(self.frame_ajout_vente, text="Prix de vente:")
        # lbl_prix_vente_va.grid(row=1, column=0, sticky=tk.E)
        # self.ent_prix_vente_va = ttk.Entry(self.frame_ajout_vente)
        # self.ent_prix_vente_va.grid(row=1, column=1, sticky=tk.W)

        # lbl_prix_achat_va = ttk.Label(self.frame_ajout_vente, text="Prix d'achat:")
        # lbl_prix_achat_va.grid(row=2, column=0, sticky=tk.E)
        # self.ent_prix_achat_va = ttk.Entry(self.frame_ajout_vente)
        # self.ent_prix_achat_va.grid(row=2, column=1,  sticky=tk.W)

        lbl_quantite_va = ttk.Label(self.frame_ajout_vente, text="Quantité:")
        lbl_quantite_va.grid(row=3, column=0, sticky=tk.E)
        self.ent_quantite_va = ttk.Entry(self.frame_ajout_vente)
        self.ent_quantite_va.grid(row=3, column=1,  sticky=tk.W)

        # btn_enregistrer_vente = ttk.Button(self.frame_ajout_vente, text="Enregistrer Vente", command=self.enregistrer_vente)
        # btn_enregistrer_vente.grid(row=4, column=0)


        btn_modifier_vente = ttk.Button(self.frame_ajout_vente, text="Modifier", command=self.modify_vente)
        btn_modifier_vente.grid(row=4, column=1)

        # btn_rechercher = ttk.Button(self.frame_ajout_vente, text="rechercher", command=self.fct_rechercher)
        # btn_rechercher.grid(row=0, column=3)
        # self.ent_rechercher = ttk.Entry(self.frame_ajout_vente)
        # self.ent_rechercher.grid(row=1, column=3, sticky=tk.W)

        self.tree_ventes = ttk.Treeview(self.frame_ajout_vente, columns=("ID", "Nom", "Quantité", "Prix de Vente", "Prix d'Achat", "Date"), show="headings")
        self.tree_ventes.grid(row=5, column=0, columnspan=5, sticky="nsew")
        self.tree_ventes.heading("ID", text="ID")
        self.tree_ventes.heading("Nom", text="Nom")
        self.tree_ventes.heading("Quantité", text="Quantité")
        self.tree_ventes.heading("Prix de Vente", text="Prix de Vente")
        self.tree_ventes.heading("Prix d'Achat", text="Prix d'Achat")
        self.tree_ventes.heading("Date", text="Date")

        self.frame_ajout_vente.grid_columnconfigure(4, weight=1)
        self.frame_ajout_vente.grid_rowconfigure(5, weight=1)

        self.update_ventes_listbox()

    def create_ajout_achat_widgets(self):
        # lbl_nom_article_aa = ttk.Label(self.frame_ajout_achat, text="Nom de l'article:")
        # lbl_nom_article_aa.grid(row=0, column=0, sticky=tk.E)
        # self.ent_nom_article_aa = ttk.Entry(self.frame_ajout_achat)
        # self.ent_nom_article_aa.grid(row=0, column=1,sticky=tk.W)

        # lbl_prix_vente_aa = ttk.Label(self.frame_ajout_achat, text="Prix de vente:")
        # lbl_prix_vente_aa.grid(row=1, column=0, sticky=tk.E)
        # self.ent_prix_vente_aa = ttk.Entry(self.frame_ajout_achat)
        # self.ent_prix_vente_aa.grid(row=1, column=1, sticky=tk.W)

        # lbl_prix_achat_aa = ttk.Label(self.frame_ajout_achat, text="Prix d'achat:")
        # lbl_prix_achat_aa.grid(row=2, column=0, sticky=tk.E)
        # self.ent_prix_achat_aa = ttk.Entry(self.frame_ajout_achat)
        # self.ent_prix_achat_aa.grid(row=2, column=1,sticky=tk.W)

        lbl_quantite_aa = ttk.Label(self.frame_ajout_achat, text="Quantité:")
        lbl_quantite_aa.grid(row=3, column=0, sticky=tk.E)
        self.ent_quantite_aa = ttk.Entry(self.frame_ajout_achat)
        self.ent_quantite_aa.grid(row=3, column=1, sticky=tk.W)

        # btn_enregistrer_achat = ttk.Button(self.frame_ajout_achat, text="Enregistrer Achat", command=self.enregistrer_achat)
        # btn_enregistrer_achat.grid(row=4, column=0)

        btn_modifier_achat = ttk.Button(self.frame_ajout_achat, text="Modifier", command=self.modify_achat)
        btn_modifier_achat.grid(row=4, column=1)

        self.tree_achats = ttk.Treeview(self.frame_ajout_achat, columns=("ID", "Nom", "Quantité", "Prix de Vente", "Prix d'Achat", "Date"), show="headings")
        self.tree_achats.grid(row=5, column=0, columnspan=5, sticky="nsew")
        self.tree_achats.heading("ID", text="ID")
        self.tree_achats.heading("Nom", text="Nom")
        self.tree_achats.heading("Quantité", text="Quantité")
        self.tree_achats.heading("Prix de Vente", text="Prix de Vente")
        self.tree_achats.heading("Prix d'Achat", text="Prix d'Achat")
        self.tree_achats.heading("Date", text="Date")
        self.frame_ajout_achat.grid_columnconfigure(4, weight=1)
        self.frame_ajout_achat.grid_rowconfigure(5, weight=1)

        self.update_achats_listbox()

    def create_inventaire_widgets(self):
        lbl_date_debut = ttk.Label(self.frame_inventaire, text="Date début (YYYY-MM-DD):")
        lbl_date_debut.grid(row=0, column=0, sticky=tk.E)
        self.ent_date_debut = ttk.Entry(self.frame_inventaire)
        self.ent_date_debut.grid(row=0, column=1, sticky=tk.W)

        lbl_date_fin = ttk.Label(self.frame_inventaire, text="Date fin (YYYY-MM-DD):")
        lbl_date_fin.grid(row=1, column=0, sticky=tk.E)
        self.ent_date_fin = ttk.Entry(self.frame_inventaire)
        self.ent_date_fin.grid(row=1, column=1, sticky=tk.W)

        btn_valider_dates = ttk.Button(self.frame_inventaire, text="Valider", command=self.charger_vue_excel)
        btn_valider_dates.grid(row=2, column=0, columnspan=2)

        btn_generer_rapport = ttk.Button(self.frame_inventaire, text="Générer Rapport", command=self.generer_rapport)
        btn_generer_rapport.grid(row=2, column=1, columnspan=2)

        columns = ["id_article", "prix_vente", "prix_achat", "valeur_achat", "valeur_vente", "benefice"]
        self.tree_inventaire = ttk.Treeview(self.frame_inventaire, columns=columns, show="headings")
        self.tree_inventaire.grid(row=3, column=0, columnspan=2, sticky="nsew")
        for col in columns:
            self.tree_inventaire.heading(col, text=col)
        self.frame_inventaire.grid_columnconfigure(1, weight=1)
        self.frame_inventaire.grid_rowconfigure(3, weight=1)

        self.lbl_totaux = ttk.Label(self.frame_inventaire, text="")
        self.lbl_totaux.grid(row=4, column=0, columnspan=2)

    def update_articles_listbox(self,articles=None):
        if articles:
            self.tree_articles.delete(*self.tree_articles.get_children())
            for article in articles:
                self.tree_articles.insert("", tk.END, values=(
                article.id_article, article.nom, article.prix_vente, article.prix_achat, article.stock, article.date))

            return
        self.tree_articles.delete(*self.tree_articles.get_children())
        for article in self.gestion_stock.lister_articles():
            self.tree_articles.insert("", tk.END, values=(
                article.id_article, article.nom, article.prix_vente, article.prix_achat, article.stock, article.date))

    def update_ventes_listbox(self):
        self.tree_ventes.delete(*self.tree_ventes.get_children())
        for vente in self.gestion_stock.lister_ventes():
            article = self.gestion_stock.rechercher_article(vente["id_article"])
            if article:
                self.tree_ventes.insert("", tk.END, values=(
                    article.id_article, article.nom, vente['quantite'], article.prix_vente, article.prix_achat, vente['date']))

    def update_achats_listbox(self):
        self.tree_achats.delete(*self.tree_achats.get_children())
        for achat in self.gestion_stock.lister_achats():
            article = self.gestion_stock.rechercher_article(achat["id_article"])
            if article:
                self.tree_achats.insert("", tk.END, values=(
                    article.id_article, article.nom, achat['quantite'], article.prix_vente, article.prix_achat, achat['date']))

    def add_article(self):
        try:
            nom = self.ent_nom_article.get()
            prix_vente = float(self.ent_prix_vente.get())
            prix_achat = float(self.ent_prix_achat.get())
            if nom and prix_vente >= 0 and prix_achat >= 0:
                result = self.gestion_stock.ajouter_article(nom, prix_vente, prix_achat)
                if result:
                    self.update_articles_listbox()
                    self.ent_nom_article.delete(0, tk.END)
                    self.ent_prix_vente.delete(0, tk.END)
                    self.ent_prix_achat.delete(0, tk.END)
                    messagebox.showinfo("Succès", "Article ajouté avec succès.")
                else:
                    messagebox.showerror("Erreur", "L'article existe déjà.")
            else:
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs correctement.")
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des prix valides.")

    def modify_article(self):
        selected_item = self.tree_articles.selection()
        if not selected_item:
            messagebox.showerror("Erreur", "Veuillez sélectionner un article.")
            return
        try:
            article_id = self.tree_articles.item(selected_item)["values"][0]
            nom = self.ent_nom_article.get()
            prix_vente = float(self.ent_prix_vente.get())
            prix_achat = float(self.ent_prix_achat.get())
            if nom and prix_vente >= 0 and prix_achat >= 0:
                self.gestion_stock.modifier_article(article_id, nom, prix_vente, prix_achat)
                self.update_articles_listbox()
                self.ent_nom_article.delete(0, tk.END)
                self.ent_prix_vente.delete(0, tk.END)
                self.ent_prix_achat.delete(0, tk.END)
                messagebox.showinfo("Succès", "Article modifié avec succès.")
            else:
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs correctement.")
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des prix valides.")

    def modify_vente(self):
        selected_item = self.tree_ventes.selection()
        if not selected_item:
            messagebox.showerror("Erreur", "Veuillez sélectionner une vente.")
            return
        try:
            article_id = self.tree_ventes.item(selected_item)["values"][0]
            date=self.tree_ventes.item(selected_item)["values"][-1]
            quantite=float(self.ent_quantite_va.get())
            if date and article_id:
                self.gestion_stock.modifier_vente(article_id, quantite, date)
                print('ok')
                
                self.update_ventes_listbox()
                self.ent_quantite_va.delete(0, tk.END)
                messagebox.showinfo("Succès", "Ventes modifié avec succès.")
            else:
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs correctement.")
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des quantitées.")

    def modify_achat(self):
        selected_item = self.tree_achats.selection()
        if not selected_item:
            messagebox.showerror("Erreur", "Veuillez sélectionner un achat.")
            return
        try:
            article_id = self.tree_achats.item(selected_item)["values"][0]
            date = self.tree_achats.item(selected_item)["values"][-1]
            quantite = float(self.ent_quantite_aa.get())
            if date and article_id:
                self.gestion_stock.modifier_achat(article_id, quantite, date)
                self.update_achats_listbox()
                self.ent_quantite_aa.delete(0, tk.END)
                messagebox.showinfo("Succès", "Achat modifié avec succès.")
            else:
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs correctement.")
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des quantités.")

    def delete_article(self):
        selected_item = self.tree_articles.selection()
        if not selected_item:
            messagebox.showerror("Erreur", "Veuillez sélectionner un article.")
            return
        article_id = self.tree_articles.item(selected_item)["values"][0]
        if self.gestion_stock.supprimer_article(article_id):
            self.update_articles_listbox()
            messagebox.showinfo("Succès", "Article supprimé avec succès.")
        else:
            messagebox.showerror("Erreur", "Erreur lors de la suppression de l'article.")

    def enregistrer_vente1(self):
        selected_item = self.tree_articles.selection()
        if not selected_item:
            messagebox.showerror("Erreur", "Veuillez sélectionner un article.")
            return
        try:
            article = self.tree_articles.item(selected_item)["values"]
            nom_article = article[1]
            quantite = float(self.ent_quantite_aa1.get())
            prix_vente = float(article[2])
            prix_achat = float(article[3])
            result = self.gestion_stock.enregistrer_vente(nom_article, prix_vente, prix_achat, quantite)
            if result:
                self.update_ventes_listbox()
                self.ent_quantite_aa1.delete(0, tk.END)
                messagebox.showinfo("Succès", "Vente enregistrée avec succès.")
            else:
                messagebox.showerror("Erreur", "Erreur lors de l'enregistrement de la vente.")
        except (ValueError, IndexError):
            messagebox.showerror("Erreur", "Veuillez entrer des données valides.")

    def enregistrer_achat1(self):
        selected_item = self.tree_articles.selection()
        if not selected_item:
            messagebox.showerror("Erreur", "Veuillez sélectionner un article.")
            return
        try:
            article = self.tree_articles.item(selected_item)["values"]
            nom_article = article[1]
            quantite =float(self.ent_quantite_aa1.get())
            prix_vente = float(article[2])
            prix_achat = float(article[3])
            result = self.gestion_stock.enregistrer_achat(nom_article, prix_vente, prix_achat, quantite)
            if result:
                self.update_achats_listbox()
                self.ent_quantite_aa1.delete(0, tk.END)
                messagebox.showinfo("Succès", "Achat enregistré avec succès.")
            else:
                messagebox.showerror("Erreur", "Erreur lors de l'enregistrement de l'achat.")
        except (ValueError, IndexError):
            messagebox.showerror("Erreur", "Veuillez entrer des données valides.")

    def enregistrer_vente(self):
        try:
            nom_article = self.ent_nom_article_va.get()
            quantite = float(self.ent_quantite_va.get())
            prix_vente = float(self.ent_prix_vente_va.get())
            prix_achat = float(self.ent_prix_achat_va.get())
            result = self.gestion_stock.enregistrer_vente(nom_article, prix_vente, prix_achat, quantite)
            if result:
                self.update_ventes_listbox()
                self.ent_nom_article_va.delete(0, tk.END)
                self.ent_quantite_va.delete(0, tk.END)
                self.ent_prix_vente_va.delete(0, tk.END)
                self.ent_prix_achat_va.delete(0, tk.END)
                messagebox.showinfo("Succès", "Vente enregistrée avec succès.")
            else:
                messagebox.showerror("Erreur", "Erreur lors de l'enregistrement de la vente.")
        except (ValueError, IndexError):
            messagebox.showerror("Erreur", "Veuillez entrer des données valides.")

    def enregistrer_achat(self):
        try:
            nom_article = self.ent_nom_article_aa.get()
            quantite = float(self.ent_quantite_aa.get())
            prix_achat = float(self.ent_prix_achat_aa.get())
            prix_vente = float(self.ent_prix_vente_aa.get())
            result = self.gestion_stock.enregistrer_achat(nom_article, prix_vente, prix_achat, quantite)
            if result:
                self.update_achats_listbox()
                self.ent_nom_article_aa.delete(0, tk.END)
                self.ent_quantite_aa.delete(0, tk.END)
                self.ent_prix_achat_aa.delete(0, tk.END)
                self.ent_prix_vente_aa.delete(0, tk.END)
                messagebox.showinfo("Succès", "Achat enregistré avec succès.")
            else:
                messagebox.showerror("Erreur", "Erreur lors de l'enregistrement de l'achat.")
        except (ValueError, IndexError):
            messagebox.showerror("Erreur", "Veuillez entrer des données valides.")

    def charger_vue_excel(self):
        try:
            date_debut = datetime.strptime(self.ent_date_debut.get(), "%Y-%m-%d")
            date_fin = datetime.strptime(self.ent_date_fin.get(), "%Y-%m-%d")
            rapport = self.gestion_stock.rapport_inventaire(date_debut, date_fin)
            self.tree_inventaire.delete(*self.tree_inventaire.get_children())

            total_ventes = 0
            total_achats = 0
            total_benefice = 0
            for id_article, details in rapport.items():
                prix_vente = details["prix_vente"]
                prix_achat = details["prix_achat"]
                valeur_vente = details["valeur_vente"]
                valeur_achat = details["valeur_achat"]
                benefice = valeur_vente - valeur_achat

                self.tree_inventaire.insert("", tk.END, values=(id_article, prix_vente, prix_achat, valeur_achat, valeur_vente, benefice))
                total_ventes += valeur_vente
                total_achats += valeur_achat
                total_benefice += benefice

            self.lbl_totaux.config(text=f"Total Ventes: {total_ventes}, Total Achats: {total_achats}, Total Bénéfice: {total_benefice}")

        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des dates valides.")

    def generer_rapport(self):
        try:
            date_debut = datetime.strptime(self.ent_date_debut.get(), "%Y-%m-%d")
            date_fin = datetime.strptime(self.ent_date_fin.get(), "%Y-%m-%d")
            rapport = self.gestion_stock.rapport_inventaire(date_debut, date_fin)

            filename = f"inventaire_{date_debut.strftime('%Y-%m-%d')}_{date_fin.strftime('%Y-%m-%d')}.csv"

            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["id_article", "prix_vente", "prix_achat", "valeur_achat", "valeur_vente", "benefice"])
                for id_article, details in rapport.items():
                    prix_vente = details["prix_vente"]
                    prix_achat = details["prix_achat"]
                    valeur_vente = details["valeur_vente"]
                    valeur_achat = details["valeur_achat"]
                    benefice = valeur_vente - valeur_achat
                    writer.writerow([id_article, prix_vente, prix_achat, valeur_achat, valeur_vente, benefice])

            messagebox.showinfo("Succès", f"Rapport enregistré dans le fichier '{filename}'.")

        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des dates valides.")




class LoginUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Connexion")

        # Configuration de la grille
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Nom d'utilisateur
        self.lbl_username = tk.Label(self.root, text="Nom d'utilisateur")
        self.lbl_username.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)

        self.ent_username = tk.Entry(self.root)
        self.ent_username.grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)

        # Mot de passe
        self.lbl_password = tk.Label(self.root, text="Mot de passe")
        self.lbl_password.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)

        self.ent_password = tk.Entry(self.root, show="*")
        self.ent_password.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        # Bouton de connexion
        self.btn_login = tk.Button(self.root, text="Connexion", command=self.login)
        self.btn_login.grid(row=2, column=0, columnspan=2, pady=10)

    def login(self):
        username = self.ent_username.get()
        password = self.ent_password.get()

        # Logique de validation de connexion
        if username == "admin" and password == "admin":
            messagebox.showinfo("Succès", "Connexion réussie!")
            self.root.destroy()  # Fermer la fenêtre de connexion
            main_app()
        else:
            messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

def main_app():
    # root = tk.Tk()
    app = StockApp()
    app.mainloop()

def login_app():
    root = tk.Tk()
    app = LoginUI(root)
    root.mainloop()


if __name__ == "__main__":
    login_app()


    # app = StockApp()
    # app.mainloop()

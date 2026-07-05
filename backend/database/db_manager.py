"""
Gestionnaire de base de données (SQLite).

Centralise toutes les opérations de persistance : création des tables et
insertion/lecture des données.
"""

import sqlite3
import os

CHEMIN_DB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                          "reservation_bus.db")


class DBManager:
    def __init__(self, chemin_db: str = CHEMIN_DB):
        self.connexion = sqlite3.connect(chemin_db, check_same_thread=False)
        self.connexion.row_factory = sqlite3.Row
        self.curseur = self.connexion.cursor()
        self._creer_tables()

    def _creer_tables(self):
        self.curseur.executescript("""
        CREATE TABLE IF NOT EXISTS administrateurs (
            identifiant TEXT PRIMARY KEY,
            mot_de_passe TEXT NOT NULL,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            telephone TEXT
        );

        CREATE TABLE IF NOT EXISTS bus (
            immatriculation TEXT PRIMARY KEY,
            marque TEXT NOT NULL,
            nombre_places INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS chauffeurs (
            numero_permis TEXT PRIMARY KEY,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            telephone TEXT,
            immatriculation_bus TEXT,
            FOREIGN KEY (immatriculation_bus) REFERENCES bus(immatriculation)
        );

        CREATE TABLE IF NOT EXISTS passagers (
            numero_piece_identite TEXT PRIMARY KEY,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            telephone TEXT
        );

        CREATE TABLE IF NOT EXISTS trajets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ville_depart TEXT NOT NULL,
            ville_arrivee TEXT NOT NULL,
            date_heure_depart TEXT NOT NULL,
            prix REAL NOT NULL,
            immatriculation_bus TEXT,
            FOREIGN KEY (immatriculation_bus) REFERENCES bus(immatriculation)
        );

        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_piece_identite TEXT NOT NULL,
            trajet_id INTEGER NOT NULL,
            numero_place INTEGER NOT NULL,
            date_reservation TEXT NOT NULL,
            reference_billet TEXT NOT NULL,
            annulee INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (numero_piece_identite) REFERENCES passagers(numero_piece_identite),
            FOREIGN KEY (trajet_id) REFERENCES trajets(id)
        );

        CREATE TABLE IF NOT EXISTS compagnie (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            nom TEXT NOT NULL,
            ville_siege TEXT NOT NULL
        );
        """)
        self.connexion.commit()

    # --- Administrateurs ---
    def ajouter_administrateur(self, identifiant, mot_de_passe, nom, prenom, telephone):
        self.curseur.execute(
            "INSERT OR REPLACE INTO administrateurs VALUES (?, ?, ?, ?, ?)",
            (identifiant, mot_de_passe, nom, prenom, telephone))
        self.connexion.commit()

    def lister_administrateurs(self):
        return self.curseur.execute("SELECT * FROM administrateurs").fetchall()

    # --- Bus ---
    def ajouter_bus(self, immatriculation, marque, nombre_places):
        self.curseur.execute(
            "INSERT OR REPLACE INTO bus VALUES (?, ?, ?)",
            (immatriculation, marque, nombre_places))
        self.connexion.commit()

    def lister_bus(self):
        return self.curseur.execute("SELECT * FROM bus").fetchall()

    def supprimer_bus(self, immatriculation):
        self.curseur.execute("DELETE FROM bus WHERE immatriculation = ?", (immatriculation,))
        self.connexion.commit()

    # --- Chauffeurs ---
    def ajouter_chauffeur(self, numero_permis, nom, prenom, telephone, immatriculation_bus):
        self.curseur.execute(
            "INSERT OR REPLACE INTO chauffeurs VALUES (?, ?, ?, ?, ?)",
            (numero_permis, nom, prenom, telephone, immatriculation_bus))
        self.connexion.commit()

    def lister_chauffeurs(self):
        return self.curseur.execute("SELECT * FROM chauffeurs").fetchall()

    # --- Passagers ---
    def ajouter_passager(self, numero_piece_identite, nom, prenom, telephone):
        self.curseur.execute(
            "INSERT OR REPLACE INTO passagers VALUES (?, ?, ?, ?)",
            (numero_piece_identite, nom, prenom, telephone))
        self.connexion.commit()

    def lister_passagers(self):
        return self.curseur.execute("SELECT * FROM passagers").fetchall()

    # --- Trajets ---
    def ajouter_trajet(self, ville_depart, ville_arrivee, date_heure_depart,
                        prix, immatriculation_bus):
        self.curseur.execute(
            """INSERT INTO trajets
               (ville_depart, ville_arrivee, date_heure_depart, prix, immatriculation_bus)
               VALUES (?, ?, ?, ?, ?)""",
            (ville_depart, ville_arrivee, date_heure_depart, prix, immatriculation_bus))
        self.connexion.commit()
        return self.curseur.lastrowid

    def lister_trajets(self):
        return self.curseur.execute("SELECT * FROM trajets").fetchall()

    # --- Reservations ---
    def ajouter_reservation(self, numero_piece_identite, trajet_id, numero_place,
                             date_reservation, reference_billet):
        self.curseur.execute(
            """INSERT INTO reservations
               (numero_piece_identite, trajet_id, numero_place,
                date_reservation, reference_billet)
               VALUES (?, ?, ?, ?, ?)""",
            (numero_piece_identite, trajet_id, numero_place,
             date_reservation, reference_billet))
        self.connexion.commit()
        return self.curseur.lastrowid

    def lister_reservations(self):
        return self.curseur.execute("SELECT * FROM reservations").fetchall()

    def annuler_reservation(self, id_reservation):
        self.curseur.execute(
            "UPDATE reservations SET annulee = 1 WHERE id = ?", (id_reservation,))
        self.connexion.commit()

    # --- Compagnie ---
    def enregistrer_compagnie(self, nom, ville_siege):
        self.curseur.execute(
            "INSERT OR REPLACE INTO compagnie (id, nom, ville_siege) VALUES (1, ?, ?)",
            (nom, ville_siege))
        self.connexion.commit()

    def charger_compagnie(self):
        return self.curseur.execute("SELECT * FROM compagnie WHERE id = 1").fetchone()

    def fermer(self):
        self.connexion.close()
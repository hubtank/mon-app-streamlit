"""
BiblioUnique.py V2
Fusion des outils personnels : utilhhd, lowORM, sysSauvegarde
"""

"""
F-Strings avancées :
- 2 décimales : f"{nombre:.2f}"
- Séparateur de milliers (français) : f"{format_fr(nombre)}"
- Exemple : f"Résultat : {format_fr(1234567.89)} €" -> Résultat : 1 234 567,89 €

strftime - Formatage des dates :
- "%Y" : Année (ex : 2025)
- "%m" : Mois numérique (01 à 12)
- "%d" : Jour du mois (01 à 31)
- "%H" : Heure (00-23)
- "%M" : Minute (00-59)
- "%S" : Seconde (00-59)
- "%A" : Jour de la semaine (ex : lundi)
- "%B" : Mois en toutes lettres (ex : avril)
- "%W" : Numéro de semaine (01-53)
- "%j" : Jour dans l'année (001-366)
- Pas de format natif pour "trimestre", il faut le calculer :
  trimestre = (mois - 1) // 3 + 1

Autres rappels utiles :
- Type dict : {"clé": valeur}
- Type set : {élément1, élément2}
- Type list : [élément1, élément2]
- Conversion rapide :
    list(mon_set) -> transforme set en liste
    set(ma_liste) -> transforme liste en set (éléments uniques)
    dict(liste_de_tuples) -> transforme [("clé", "valeur")] en dict

Astuce bonus :
- Fusion de dictionnaires : d1 | d2 (Python 3.9+)
"""
"""
Module pour gérer l'état global de l'application
"""

# === Imports ===
from typing import Optional, Union, Literal
from datetime import datetime, date, timedelta
import calendar
import sqlite3
from functools import wraps
import random


def ensure_date(func):
    """
    Décorateur récursif : convertit tous les datetime en date dans les args et kwargs.
    """

    def convertir(obj):
        if isinstance(obj, datetime):
            return obj.date()
        elif isinstance(obj, (list, tuple)):
            return type(obj)(convertir(x) for x in obj)
        elif isinstance(obj, dict):
            return {k: convertir(v) for k, v in obj.items()}
        else:
            return obj

    @wraps(func)
    def wrapper(*args, **kwargs):
        new_args = tuple(convertir(arg) for arg in args)
        new_kwargs = {k: convertir(v) for k, v in kwargs.items()}
        return func(*new_args, **new_kwargs)

    return wrapper


# def ensure_date(func):
#     """
#     Décorateur qui convertit les datetime en date pour les paramètres de la fonction.
#     """

#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         # Convertir les args
#         new_args = []
#         for arg in args:
#             if isinstance(arg, datetime):
#                 new_args.append(arg.date())
#             else:
#                 new_args.append(arg)

#         # Convertir les kwargs
#         new_kwargs = {}
#         for key, value in kwargs.items():
#             if isinstance(value, datetime):
#                 new_kwargs[key] = value.date()
#             else:
#                 new_kwargs[key] = value

#         return func(*new_args, **new_kwargs)

#     return wrapper


# === Constantes ===

MOIS_FRANCE = {
    1: "Janvier",
    2: "Février",
    3: "Mars",
    4: "Avril",
    5: "Mai",
    6: "Juin",
    7: "Juillet",
    8: "Août",
    9: "Septembre",
    10: "Octobre",
    11: "Novembre",
    12: "Décembre",
}

MOIS_FR_ABR = {
    1: "jan.",
    2: "fév.",
    3: "mars",
    4: "avr.",
    5: "mai",
    6: "juin",
    7: "juil.",
    8: "août",
    9: "sept.",
    10: "oct.",
    11: "nov.",
    12: "déc.",
}

JOURS_FRANCE = {
    1: "lundi",
    2: "mardi",
    3: "mercredi",
    4: "jeudi",
    5: "vendredi",
    6: "samedi",
    7: "dimanche",
}

JOURS_FR_ABR = {
    1: "lun.",
    2: "mar.",
    3: "mer.",
    4: "jeu.",
    5: "ven.",
    6: "sam.",
    7: "dim.",
}

# === Constantes ===


def get_police_luciole(taille=14, gras=False):
    import wx

    poids = wx.FONTWEIGHT_BOLD if gras else wx.FONTWEIGHT_NORMAL
    return wx.Font(
        taille, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, poids, False, "Luciole"
    )


MOIS_FRANCE = {
    1: "Janvier",
    2: "Février",
    3: "Mars",
    4: "Avril",
    5: "Mai",
    6: "Juin",
    7: "Juillet",
    8: "Août",
    9: "Septembre",
    10: "Octobre",
    11: "Novembre",
    12: "Décembre",
}
MOIS_FR_ABR = {
    1: "jan",
    2: "fév",
    3: "mar",
    4: "avr",
    5: "mai",
    6: "juin",
    7: "juil",
    8: "aoû",
    9: "sep",
    10: "oct",
    11: "nov",
    12: "déc",
}
JOURS_FRANCE = {
    1: "Lundi",
    2: "Mardi",
    3: "Mercredi",
    4: "Jeudi",
    5: "Vendredi",
    6: "Samedi",
    7: "Dimanche",
}
JOURS_FR_ABR = {
    1: "lun",
    2: "mar",
    3: "mer",
    4: "jeu",
    5: "ven",
    6: "sam",
    7: "dim",
}


# === Classes ===
class VarSetBind:
    def __init__(self):
        self._state = {}
        self._observers = {}

    def set(self, key, value):
        self._state[key] = value
        for cb in self._observers.get(key, []):
            cb(value)

    def get(self, key, default=None):
        return self._state.get(key, default)

    def bind_label(self, key, label):
        def update_label(val):
            label.text = str(val)

        self._observers.setdefault(key, []).append(update_label)
        label.text = str(self.get(key))

    def bind_field(self, key, field):
        def update_field(val):
            field.text = str(val)

        def on_edit(sender):
            self.set(key, int(sender.text))

        self._observers.setdefault(key, []).append(update_field)
        field.action = on_edit
        field.text = str(self.get(key))

    def link(self, key_target, keys_sources, compute_fn):
        def update(_=None):
            vals = [self.get(k) for k in keys_sources]
            self.set(key_target, compute_fn(*vals))

        for k in keys_sources:
            self._observers.setdefault(k, []).append(update)
        update()


vsb = VarSetBind()


import sqlite3
from typing import Optional


class Database:
    def __init__(self, chemin: str):
        self.chemin = chemin

    def table_existe(self, nom_table: str) -> bool:
        with sqlite3.connect(self.chemin) as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
                (nom_table,),
            )
            return cur.fetchone() is not None

    def creer_table(self, nom_table: str, colonnes: dict):
        with sqlite3.connect(self.chemin) as conn:
            cur = conn.cursor()
            colonnes_sql = ", ".join(
                [f"{nom} {type_}" for nom, type_ in colonnes.items()]
            )
            requete = f"CREATE TABLE IF NOT EXISTS {nom_table} ({colonnes_sql})"
            cur.execute(requete)
            conn.commit()

    def insert(self, table: str, valeurs: dict):
        with sqlite3.connect(self.chemin) as conn:
            cur = conn.cursor()
            colonnes = ", ".join(valeurs.keys())
            marqueurs = ", ".join(["?"] * len(valeurs))
            requete = f"INSERT INTO {table} ({colonnes}) VALUES ({marqueurs})"
            cur.execute(requete, tuple(valeurs.values()))
            conn.commit()

    def select(
        self,
        table: str,
        colonnes: Optional[list] = None,
        where: Optional[str] = None,
        params: tuple = (),
    ):
        with sqlite3.connect(self.chemin) as conn:
            cur = conn.cursor()
            colonnes_sql = ", ".join(colonnes) if colonnes else "*"
            requete = f"SELECT {colonnes_sql} FROM {table}"
            if where:
                requete += f" WHERE {where}"
            # Convertir params en liste pour éviter les problèmes avec les tuples
            if isinstance(params, tuple) and len(params) == 1:
                params = [params[0]]
            cur.execute(requete, params)
            return cur.fetchall()

    def DeleteTable(self, table: str):
        with sqlite3.connect(self.chemin) as conn:
            cur = conn.cursor()
            requete = f"DROP TABLE IF EXISTS {table}"
            cur.execute(requete)
            conn.commit()

    def update(self, table: str, valeurs: dict, where: str, params: tuple = ()):
        """
        Met à jour des lignes avec conditions dynamiques.
        exemples : db.update("travail", {"oui_non": 1}, "id = ?", (fichID,)) #1 condition
        exemples : db.update("travail", {"oui_non": 1}, "id = ? AND date = ?", (fichID, date)) #2 conditions
        Usage des guillemets dans les conditions :
        - Pour une égalité simple : {"date": "2025-05-24"}
        - Pour d'autres opérateurs : {"date": "> '2025-05-24'"}

        Exemples :
        - Dates après une date donnée :
          {"date": "> '2025-05-24'"}
        - Dates avant ou égales :
          {"date": "<= '2025-05-24'"}
        - Plusieurs conditions :
          {
              "date": "> '2025-05-24'",
              "oui_non": "1"
          }
        - Valeurs textuelles avec apostrophes :
          {"nom": "O'Connor"}  # Les apostrophes sont automatiquement échappées
        """
        with sqlite3.connect(self.chemin) as conn:
            cur = conn.cursor()
            set_clause = ", ".join([f"{k}=?" for k in valeurs.keys()])
            requete = f"UPDATE {table} SET {set_clause} WHERE {where}"
            cur.execute(requete, tuple(valeurs.values()) + params)
            conn.commit()

    def delete(self, table: str, where: str, params: tuple = ()):
        """
        Supprime des lignes avec conditions dynamiques.
        exemples : db.delete("travail", "id = ?", (fichID,)) #1 condition
        exemples : db.delete("travail", "id = ? AND date = ?", (fichID, date)) #2 conditions
        Usage des guillemets dans les conditions :
        - Pour une égalité simple : {"date": "2025-05-24"}
        - Pour d'autres opérateurs : {"date": "> '2025-05-24'"}

        Exemples :
        - Dates après une date donnée :
          {"date": "> '2025-05-24'"}
        - Dates avant ou égales :
          {"date": "<= '2025-05-24'"}
        - Plusieurs conditions :
          {
              "date": "> '2025-05-24'",
              "oui_non": "1"
          }
        - Valeurs textuelles avec apostrophes :
          {"nom": "O'Connor"}  # Les apostrophes sont automatiquement échappées
        """
        with sqlite3.connect(self.chemin) as conn:
            cur = conn.cursor()
            requete = f"DELETE FROM {table} WHERE {where}"
            cur.execute(requete, params)
            conn.commit()

    def select_where(
        self, table: str, conditions: dict = None, order_by: str = "", limit: int = None
    ):
        """
        Sélectionne des lignes avec conditions dynamiques.

        Usage des guillemets dans les conditions :
        - Pour une égalité simple : {"date": "2025-05-24"}
        - Pour d'autres opérateurs : {"date": "> '2025-05-24'"}

        Exemples :
        - Dates après une date donnée :
          {"date": "> '2025-05-24'"}
        - Dates avant ou égales :
          {"date": "<= '2025-05-24'"}
        - Plusieurs conditions :
          {
              "date": "> '2025-05-24'",
              "oui_non": "1"
          }
        - Valeurs textuelles avec apostrophes :
          {"nom": "O'Connor"}  # Les apostrophes sont automatiquement échappées

        Args:
            table (str): Nom de la table
            conditions (dict, optional): Conditions de sélection
            order_by (str, optional): Clause ORDER BY
            limit (int, optional): Limite du nombre de résultats

        Returns:
            list: Liste des résultats
        """
        with sqlite3.connect(self.chemin) as conn:
            cur = conn.cursor()

            where_clauses = []
            valeurs = []

            if conditions:
                for col, val in conditions.items():
                    if isinstance(val, str) and val.strip().startswith(
                        (">", "<", "=", "!=")
                    ):
                        where_clauses.append(f"{col} {val}")
                    else:
                        where_clauses.append(f"{col} = ?")
                        valeurs.append(val)

        requete = f"SELECT * FROM {table}"
        if where_clauses:
            requete += " WHERE " + " AND ".join(where_clauses)
        if order_by:
            requete += f" ORDER BY {order_by}"
        if limit is not None:
            requete += f" LIMIT {limit}"

        if valeurs:
            cur.execute(requete, valeurs)
        else:
            cur.execute(requete)

        return cur.fetchall()


class AppState:
    _instance = None

    @staticmethod
    def get_instance():
        """Méthode statique pour obtenir l'instance unique"""
        if AppState._instance is None:
            AppState._instance = AppState()
        return AppState._instance

    def __init__(self):
        """Initialisation de l'état"""
        self._state = {"nom": "", "message": ""}
        self._observers = {}

    def set(self, key, value):
        """Mettre à jour une valeur et notifie les observateurs"""
        self._state[key] = value
        if key in self._observers:
            for callback in self._observers[key]:
                callback(value)

    def get(self, key, default=None):
        """Obtenir une valeur avec une valeur par défaut"""
        return self._state.get(key, default)

    def subscribe(self, key, callback):
        """S'abonner aux changements d'une clé"""
        if key not in self._observers:
            self._observers[key] = []
        self._observers[key].append(callback)

    def unsubscribe(self, key, callback):
        """Se désabonner des changements d'une clé"""
        if key in self._observers:
            self._observers[key].remove(callback)
            if not self._observers[key]:
                del self._observers[key]


app_state = AppState.get_instance()


# === Fonctions ===


def nombreFr(valeur: Union[str, float, int], style: str = "float") -> str:
    """
    Formatte un nombre à la française :
    - style="euro"  ➜ 12 345,67 €
    - style="float" ➜ 12 345,67
    - style="int"   ➜ 12 346
    """
    if isinstance(valeur, str):
        try:
            valeur = float(valeur.replace(",", ".").replace(" ", ""))
        except:
            return "—"

    if style == "int":
        entier = round(valeur)
        partie = f"{entier:,}".replace(",", " ").replace("\xa0", " ")
        return partie

    partie = f"{valeur:,.2f}".replace(",", " ").replace(".", ",")
    if style == "euro":
        return partie + " €"
    return partie


def frToNombre(txt: str) -> float:
    """
    Convertit un texte formaté à la française en float :
    - "12 345,67 €" ➜ 12345.67
    - Gère tous les types d'espaces et formats typographiques
    """
    if not txt:
        return 0.0
    try:
        propre = (
            txt.replace("€", "")
            .replace(",", ".")
            .replace("\xa0", "")  # espace insécable classique
            .replace("\u202f", "")  # espace fine insécable (française)
            .replace(" ", "")
        )
        return float(propre)
    except:
        return 0.0


def datefr2iso(text: str) -> Optional[str]:
    """
    Convertit une date au format français en format ISO (YYYY-MM-DD).

    Supporte les formats suivants :
    - "lun. 21 jan. 2025" (abr)
    - "lundi 21 janvier 2025" (long)
    - "janvier" (mois)
    - "jan" (moisAbr)
    - "2025" (an)

    Retourne None si le format n'est pas reconnu.
    """
    try:
        # Extraire les éléments de base
        elements = text.split()

        # Cas "2025" (année seule)
        if len(elements) == 1 and elements[0].isdigit():
            return f"{elements[0]}-01-01"

        # Cas "janvier" ou "jan"
        if len(elements) == 1:
            mois = elements[0].lower()
            for num, moisAbr in MOIS_FR_ABR.items():
                if moisAbr.startswith(mois):
                    return f"2025-{num:02d}-01"
            for num, moisLong in MOIS_FRANCE.items():
                if moisLong.lower().startswith(mois):
                    return f"2025-{num:02d}-01"
            return None

        # Cas "lun. 21 jan. 2025" ou "lundi 21 janvier 2025"
        if len(elements) == 4:
            # Extraire les éléments
            jourAbr = elements[0].lower()
            jour = int(elements[1])
            mois = elements[2].lower()
            annee = int(elements[3])

            # Vérifier le jour
            if jour < 1 or jour > 31:
                return None

            # Trouver le numéro du mois
            for num, moisAbr in MOIS_FR_ABR.items():
                if moisAbr.startswith(mois):
                    return f"{annee:04d}-{num:02d}-{jour:02d}"
            for num, moisLong in MOIS_FRANCE.items():
                if moisLong.lower().startswith(mois):
                    return f"{annee:04d}-{num:02d}-{jour:02d}"
            return None

        return None
    except (ValueError, IndexError):
        return None


@ensure_date
def dateFr(d: date = None, style: str = "abr") -> str:
    """
    Retourne une date formatée à la française sans locale.

    style :
      - "abr"       ➜ lun 21 jan 2025
      - "long"      ➜ lundi 21 janvier 2025
      - "jour"      ➜ lundi
      - "jourAbr"   ➜ lun.
      - "mois"      ➜ janvier
      - "moisAbr"   ➜ jan.
      - "an"        ➜ 2025
      - "iso"      ➜ 2025-01-21
    """
    if d is None:
        d = date.today()
    j = d.isoweekday()
    m = d.month

    if style == "jour":
        return JOURS_FRANCE[j]
    elif style == "jourAbr":
        return JOURS_FR_ABR[j]
    elif style == "mois":
        return MOIS_FRANCE[m]
    elif style == "moisAbr":
        return MOIS_FR_ABR[m]
    elif style == "an":
        return str(d.year)
    elif style == "iso":
        return f"{d.year}-{m:02d}-{d.day:02d}"
    elif style == "long":
        jour = JOURS_FRANCE[j]
        mois = MOIS_FRANCE[m]
        return f"{jour} {d.day:02d} {mois} {d.year}"
    else:
        jour = JOURS_FR_ABR[j]
        mois = MOIS_FR_ABR[m]
        return f"{jour} {d.day:02d} {mois} {d.year}"


def wxSegControl(parent, options: list[str], orient="horizontal"):
    """SegmentedControl exclusif, retour index (ou -1 si rien)

    Args:
        parent : wx.Panel ou wx.Frame parent
        options : liste de libellés (str)
        orient : "horizontal" ou "vertical"

    Returns:
        wx.Panel avec méthodes :
            .get_selection() -> int
            .set_selection(index: int)
    """
    import wx

    class _SegmentedCheckBox(wx.Panel):
        def __init__(self, parent, options, orient):
            super().__init__(parent)

            self.options = options
            self.orientation = orient
            self.box = wx.BoxSizer(
                wx.HORIZONTAL if orient == "horizontal" else wx.VERTICAL
            )
            self.checkboxes = []

            dc = wx.ClientDC(self)
            font = self.GetFont()
            dc.SetFont(font)
            widths = [dc.GetTextExtent(opt)[0] for opt in options]
            max_width = max(widths) + 20

            for label in options:
                cb = wx.CheckBox(self, label=label, size=(max_width, -1))
                cb.Bind(wx.EVT_CHECKBOX, self._on_check)
                self.box.Add(cb, 0, wx.ALL, 2)
                self.checkboxes.append(cb)

            self.SetSizer(self.box)

        def _on_check(self, event):
            clicked = event.GetEventObject()
            if clicked.GetValue():
                for cb in self.checkboxes:
                    if cb != clicked:
                        cb.SetValue(False)

        def get_selection(self) -> int:
            for i, cb in enumerate(self.checkboxes):
                if cb.GetValue():
                    return i
            return -1

        def set_selection(self, index: int):
            for i, cb in enumerate(self.checkboxes):
                cb.SetValue(i == index)

        def reset_selection(self):
            for cb in self.checkboxes:
                cb.SetValue(False)

    return _SegmentedCheckBox(parent, options, orient)


def objToDateFr(date_str: str) -> Optional[date]:
    """
    Convertit une chaîne de date française en objet date.

    Supporte les formats suivants :
    - "lun 21 jan 2025" (abr)
    - "lundi 21 janvier 2025" (long)
    - "janvier" (mois)
    - "jan" (moisAbr)
    - "2025" (an)
    - "2025-01-21" (iso)

    Retourne None si le format n'est pas reconnu.
    """
    try:
        # Gérer le format ISO (YYYY-MM-DD)
        if date_str.count("-") == 2:  # Format ISO
            try:
                return date.fromisoformat(date_str)
            except ValueError:
                pass

        # Gérer le format année seule
        if len(date_str) == 4 and date_str.isdigit():
            return date(int(date_str), 1, 1)

        # Extraire les éléments de base pour les autres formats
        elements = date_str.split()

        # Cas "2025" (année seule)
        if len(elements) == 1 and elements[0].isdigit():
            return date(int(elements[0]), 1, 1)

        # Cas "janvier" ou "jan"
        if len(elements) == 1:
            mois = elements[0].lower()
            for num, moisAbr in MOIS_FR_ABR.items():
                if moisAbr.lower().startswith(mois):
                    return date(datetime.now().year, num, 1)
            for num, moisLong in MOIS_FRANCE.items():
                if moisLong.lower().startswith(mois):
                    return date(datetime.now().year, num, 1)
            return None

        # Cas "lun. 21 jan. 2025" ou "lundi 21 janvier 2025"
        if len(elements) == 4:
            try:
                jour = int(elements[1])
                mois = elements[2].lower()
                annee = int(elements[3])

                # Vérifier le jour
                if jour < 1 or jour > 31:
                    return None

                # Trouver le numéro du mois
                for num, moisAbr in MOIS_FR_ABR.items():
                    if moisAbr.lower().startswith(mois):
                        return date(annee, num, jour)
                for num, moisLong in MOIS_FRANCE.items():
                    if moisLong.lower().startswith(mois):
                        return date(annee, num, jour)
                return None

            except (ValueError, IndexError):
                return None

        return None
    except (ValueError, IndexError):
        return None


def dateSelectorAttach(datepicker, default_date):
    """
    Installe un DatePicker masqué + bouton cliquable.
    - Le bouton affiche la date au format français.
    - À la sélection, le bouton est mis à jour et le DatePicker disparaît.
    - Si `state` est fourni, la valeur est enregistrée dans state[bind_key].
    """

    import ui
    from datetime import datetime
    from BiblioUnique import dateFr

    def show_picker(sender):
        datepicker.hidden = False
        datepicker.bring_to_front()
        print(f"show_picker {datepicker.name}")

        # Créer un bouton de validation
        if not hasattr(datepicker, "valider_button"):
            valider = ui.Button()
            valider.title = "✓"
            valider.font = ("<system>", 20)
            valider.alignment = ui.ALIGN_CENTER
            valider.background_color = "#4CAF50"
            valider.tint_color = "white"
            valider.border_width = 1
            valider.border_color = "#388E3C"
            valider.corner_radius = 5
            valider.action = lambda s: update_label(datepicker)
            datepicker.valider_button = valider
            datepicker.superview.add_subview(valider)

        # Positionner le bouton de validation
        picker_frame = datepicker.frame
        valider = datepicker.valider_button
        valider.frame = (
            picker_frame[0] + picker_frame[2] + 10,
            picker_frame[1],
            40,
            picker_frame[3],
        )
        valider.bring_to_front()

    def update_label(sender):
        # Mettre à jour le bouton avec la nouvelle date
        button.title = dateFr(sender.date)
        button.bring_to_front()
        print(f"update_label {button.title}")

        # Masquer le DatePicker
        datepicker.hidden = True
        print(f"Masquer le DatePicker {datepicker.name}")

        # Masquer le bouton de validation
        if hasattr(datepicker, "valider_button"):
            datepicker.valider_button.hidden = True

    # Préparation du DatePicker
    datepicker.hidden = True
    datepicker.date = default_date

    # Bouton simulant le label
    button = ui.Button()

    # Bouton simulant le label
    button = ui.Button()
    button.name = f"label_for_{datepicker.name}"
    button.title = dateFr(default_date)
    button.font = ("<system>", 16)
    button.alignment = ui.ALIGN_CENTER
    button.frame = datepicker.frame
    button.background_color = "white"
    button.tint_color = "black"
    button.border_width = 0
    button.action = show_picker

    datepicker.label_button = button
    datepicker.superview.add_subview(button)


def choixDateForPython(
    question: str = "Date ?",
    jourDebut: int | None = None,
    moisDebut: int | None = None,
    anneeDebut: int | None = None,
):
    """
    Affiche un calendrier avec sélection jour/mois/année.

    Parameters
    ----------
    question : str
        Texte affiché en haut de la boîte de dialogue, ou None pour "Date ?".
    jourDebut : int, optional
        Jour à pré-sélectionner (1–31), ou None pour utiliser la date courante.
    moisDebut : int, optional
        Mois à pré-sélectionner (1–12), ou None pour utiliser la date courante.
    anneeDebut : int, optional
        Année à pré-sélectionner (≥1900), ou None pour utiliser la date courante.

    Returns
    -------
    tuple
        (True, date) si l'utilisateur valide une date,
        (False, date_initiale) si l'utilisateur annule la sélection.
    """

    try:
        import wx
        from datetime import date
        from calendar import monthrange
    except ImportError:
        raise RuntimeError("wxPython est requis dans l’environnement actuel.")

    jourDebut, moisDebut, anneeDebut = validate_and_fix_date(
        jourDebut, moisDebut, anneeDebut
    )
    ancienne_date = (jourDebut, moisDebut, anneeDebut)

    dialog = wx.Dialog(None, title="Choisir une date")
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(wx.StaticText(dialog, label=question), 0, wx.ALL | wx.CENTER, 10)

    mois_labels = [
        "Jan",
        "Fév",
        "Mar",
        "Avr",
        "Mai",
        "Juin",
        "Juil",
        "Aoû",
        "Sep",
        "Oct",
        "Nov",
        "Déc",
    ]
    month_choice = wx.Choice(dialog, choices=mois_labels)
    month_choice.SetSelection(moisDebut - 1)

    year_text = wx.TextCtrl(
        dialog, value=str(anneeDebut), style=wx.TE_READONLY, size=(60, -1)
    )

    def popup_annee(evt=None):
        dlg = wx.TextEntryDialog(
            dialog, "Entrer une année", "Choisir une année", year_text.GetValue()
        )
        if dlg.ShowModal() == wx.ID_OK:
            try:
                an = int(dlg.GetValue())
                if 1900 <= an <= 2100:
                    year_text.SetValue(str(an))
                    update_days()
            except:
                pass
        dlg.Destroy()

    year_text.Bind(wx.EVT_LEFT_DOWN, popup_annee)
    year_text.Bind(wx.EVT_KILL_FOCUS, popup_annee)

    ligne_haut = wx.BoxSizer(wx.HORIZONTAL)
    ligne_haut.Add(month_choice, 1, wx.ALL, 5)
    ligne_haut.Add(year_text, 0, wx.ALL, 5)
    sizer.Add(ligne_haut, 0, wx.CENTER)

    jours = ["Lu", "Ma", "Me", "Je", "Ve", "Sa", "Di"]
    ligne_jours = wx.BoxSizer(wx.HORIZONTAL)
    for j in jours:
        b = wx.Button(dialog, label=j, size=(40, 30))
        b.Disable()
        ligne_jours.Add(b, 0, wx.ALL, 1)
    sizer.Add(ligne_jours, 0, wx.CENTER)

    panel = wx.Panel(dialog)
    grille = wx.GridSizer(6, 7, 2, 2)
    panel.SetSizer(grille)
    sizer.Add(panel, 0, wx.ALL | wx.CENTER, 5)

    resume = wx.StaticText(dialog, label="")
    sizer.Add(resume, 0, wx.ALL | wx.CENTER, 5)

    selected_day = [jourDebut]
    boutons = []

    def update_resume():
        try:
            dt = date(
                int(year_text.GetValue()),
                month_choice.GetSelection() + 1,
                selected_day[0],
            )
            resume.SetLabel(dt.strftime("%A %d %B %Y").capitalize())
        except:
            resume.SetLabel("")

    def update_days():
        for b in boutons:
            b.Destroy()
        boutons.clear()
        year = int(year_text.GetValue())
        month = month_choice.GetSelection() + 1
        start, count = monthrange(year, month)
        decalage = (start + 6) % 7
        for _ in range(decalage):
            grille.Add(wx.StaticText(panel, label=""))
        for d in range(1, count + 1):
            b = wx.Button(panel, label=str(d), size=(40, 30))

            def on_click(evt, j=d):
                selected_day[0] = j
                update_resume()

            b.Bind(wx.EVT_BUTTON, on_click)
            boutons.append(b)
            grille.Add(b, 0, wx.EXPAND)
        dialog.Layout()

    month_choice.Bind(wx.EVT_CHOICE, lambda e: update_days())
    update_days()

    boutons_bas = wx.StdDialogButtonSizer()
    ok = wx.Button(dialog, wx.ID_OK)
    cancel = wx.Button(dialog, wx.ID_CANCEL)
    boutons_bas.AddButton(ok)
    boutons_bas.AddButton(cancel)
    boutons_bas.Realize()
    sizer.Add(boutons_bas, 0, wx.ALL | wx.EXPAND, 10)

    dialog.SetSizer(sizer)
    sizer.Fit(dialog)
    dialog.Centre()

    resultat = dialog.ShowModal()
    dialog.Destroy()

    if resultat == wx.ID_OK:
        return (
            True,
            date(
                int(year_text.GetValue()),
                month_choice.GetSelection() + 1,
                selected_day[0],
            ),
        )
    else:
        return (
            False,
            date(ancienne_date[2], ancienne_date[1], ancienne_date[0]),
        )


def validate_date(jour: int, mois: int, annee: int) -> bool:
    """Valider une date"""
    try:
        date(annee, mois, jour)  # Ordre correct : année, mois, jour
        return True
    except ValueError:
        return False


def validate_time(heure: int, minute: int, seconde: int) -> bool:
    """Valider une heure"""
    try:
        datetime(
            2023, 1, 1, heure, minute, seconde
        )  # Ordre correct : année, mois, jour, heure, minute, seconde
        return True
    except ValueError:
        return False


def validate_datetime(
    jour: int, mois: int, annee: int, heure: int, minute: int, seconde: int
) -> bool:
    """Valider une date et une heure"""
    try:
        datetime(
            annee, mois, jour, heure, minute, seconde
        )  # Ordre correct : année, mois, jour, heure, minute, seconde
        return True
    except ValueError:
        return False


def validate_and_fix_date(
    jour: int | None, mois: int | None, annee: int | None
) -> tuple[int, int, int]:
    """Valide et corrige une date si nécessaire"""
    now = date.today()
    jour = jour or now.day
    mois = mois or now.month
    annee = annee or now.year

    if not validate_date(jour, mois, annee):
        return now.day, now.month, now.year
    return jour, mois, annee


def validate_and_fix_time(
    heure: int | None, minute: int | None, seconde: int | None
) -> tuple[int, int, int]:
    """Valide et corrige une heure si nécessaire"""
    now = datetime.now()
    heure = heure or now.hour
    minute = minute or now.minute
    seconde = seconde or now.second

    if not validate_time(heure, minute, seconde):
        return now.hour, now.minute, now.second
    return heure, minute, seconde


def wx_to_datetime(wx_date):
    """
    Convertit un objet wx.DateTime en objet datetime.datetime standard.

    ⚠ wx.DateTime utilise un index de mois de 0 à 11 (Janvier = 0),
    contrairement à datetime qui attend 1 à 12. Le mois est donc ajusté avec +1.

    :param wx_date: Objet wx.DateTime (ex. issu d'un DatePickerCtrl)
    :return: Objet datetime.datetime équivalent
    """
    from datetime import datetime
    import wx  # import local pour ne pas alourdir globalement

    return datetime(wx_date.GetYear(), wx_date.GetMonth() + 1, wx_date.GetDay())


def datetime_to_wx(dt_obj):
    """
    Convertit un objet datetime.datetime standard en wx.DateTime.

    ⚠ wx.DateTime attend un mois de 0 à 11, donc on enlève 1 à datetime.month.

    :param dt_obj: Objet datetime.datetime
    :return: Objet wx.DateTime équivalent
    """
    import wx  # import local pour garder la légèreté de la lib

    return wx.DateTime.FromDMY(dt_obj.day, dt_obj.month - 1, dt_obj.year)


def format_euro(valeur: Union[str, float, int]) -> str:
    """
    Formate une valeur en euros à la française.

    - Accepte une chaîne, un entier ou un float (même formatée '1 000,50').
    - Retourne une chaîne comme '1 234,56 €'.
    - Retourne '0,00 €' si la conversion échoue.
    """
    try:
        return f"{textoFloat(valeur):,.2f} €".replace(",", " ").replace(".", ",")
    except:
        return "0,00 €"


def format_fr(nombre: Union[str, float, int]) -> str:
    """
    Formate un nombre en style français avec espaces pour les milliers et virgule pour les décimales.

    - Exemple : 1234567.89 devient '1 234 567,89'
    - Retourne '0,00' si la conversion échoue.
    """
    try:
        return f"{float(nombre):,.2f}".replace(",", " ").replace(".", ",")
    except:
        return "0,00"


def textoFloat(texte: Union[str, float, int]) -> float:
    """
    Convertit une chaîne, un entier ou un float vers un float.

    - Accepte les formats comme '1 000,50' ou '1 000'.
    - Utilise '.' comme séparateur décimal et ignore les espaces.
    - Retourne 0.0 si la conversion échoue.
    """
    try:
        return float(str(texte).replace(",", ".").replace(" ", ""))
    except:
        return 0.0


def sys_date(tdate: datetime) -> Optional[str]:
    """
    Convertit un objet datetime en chaîne au format 'YYYY-MM-DD'.

    - Retourne None en cas d'erreur ou si l'entrée est invalide.
    """
    try:
        return tdate.strftime("%Y-%m-%d")
    except:
        return None


def from_sql_date(s: str) -> Optional[datetime]:
    """
    Convertit une chaîne de type 'YYYY-MM-DD' en objet datetime.

    - Retourne None si la chaîne est mal formée ou vide.
    """
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except (ValueError, TypeError):
        return None


@ensure_date
def ecart_ymd(date1: date, date2: date) -> tuple[int, int, int]:
    """
    Retourne l'écart entre deux dates en années, mois et jours.
    """
    if date1 > date2:
        date1, date2 = date2, date1

    y = date2.year - date1.year
    m = date2.month - date1.month
    d = date2.day - date1.day

    if d < 0:
        m -= 1
        # jours du mois précédent
        prev_month = date2.replace(day=1) - timedelta(days=1)
        d += prev_month.day

    if m < 0:
        y -= 1
        m += 12

    return y, m, d


def prochainJourSemaine(*jours_souhaités, ref=None):
    """
    Retourne les prochaines dates correspondant aux jours demandés.

    - Sans argument : retourne la date du même jour la semaine suivante.
    - Avec un ou plusieurs jours (ex: "lundi", "mardi") : retourne la prochaine occurrence de chacun.
    - Paramètre ref :
        "2sem"  ➜ semaine +1 (soit +14 jours)
        "3sem"  ➜ semaine +2 (soit +21 jours)
        "1mois" ➜ mois +1 (soit +30 jours)

    Retour : liste de datetime
    """
    noms_jours = {
        "lundi": 0,
        "mardi": 1,
        "mercredi": 2,
        "jeudi": 3,
        "vendredi": 4,
        "samedi": 5,
        "dimanche": 6,
    }

    decalages = {
        "2sem": 7,
        "3sem": 14,
        "1mois": 23,
    }

    aujourd_hui = date.today()

    if not jours_souhaités:
        jours_souhaités = [dateFr(aujourd_hui, "jour")]

    resultats = []
    for nom in jours_souhaités:
        cible = noms_jours[nom.lower()]
        ecart = (cible - aujourd_hui.weekday() + 7) % 7
        ecart = ecart or 7  # éviter aujourd’hui
        ecart += decalages.get(ref, 0)
        date_prochaine = aujourd_hui + timedelta(days=ecart)
        resultats.append(date_prochaine)

    resultats.sort()
    return resultats


def sauvegardeAuto(nameProject="auto", LOG_ACTIVE=True, NB_SAUVEGARDE=20):
    """
    Sauvegarde automatiquement le script appelant dans un dossier horodaté.

    📦 Fonctionnement :
    - Crée un sous-dossier dans Historic/<nomProjet>/<horodatage>.
    - Copie le fichier appelant dans ce dossier.
    - Garde uniquement les X dernières versions selon NB_SAUVEGARDE.

    🔧 Paramètres :
    - nameProject (str) : Nom du projet (ou "auto" pour détecter automatiquement).
    - LOG_ACTIVE (bool) : Affiche les messages de log dans le terminal.
    - NB_SAUVEGARDE (int) : Nombre de versions à conserver.

    ✅ Compatible avec tous les fichiers appelant la fonction dans un projet commun.
    """
    import os
    import shutil
    import inspect
    from datetime import datetime

    _CONFIG_SAUVEGARDE = {
        "initialized": False,
        "nameProject": "",
        "log": True,
        "limit": 20,
        "horodatage": datetime.now().strftime("%Y%m%d-%H%M%S"),
    }
    if not _CONFIG_SAUVEGARDE["initialized"]:
        _CONFIG_SAUVEGARDE["nameProject"] = nameProject if nameProject else ""
        _CONFIG_SAUVEGARDE["log"] = LOG_ACTIVE
        _CONFIG_SAUVEGARDE["limit"] = NB_SAUVEGARDE
        _CONFIG_SAUVEGARDE["initialized"] = True

        if _CONFIG_SAUVEGARDE["nameProject"] == "auto":
            _CONFIG_SAUVEGARDE["nameProject"] = os.path.basename(
                inspect.stack()[-1].filename
            ).split(".")[0]

    try:
        frame = inspect.stack()[1]
        caller_file = frame.filename
        if not caller_file.endswith(".py"):
            return

        nom_fichier = os.path.basename(caller_file)
        nom_repertoire = os.path.dirname(caller_file)
        dossier_historique = os.path.join(
            nom_repertoire,
            "Historic",
            _CONFIG_SAUVEGARDE["nameProject"],
            _CONFIG_SAUVEGARDE["horodatage"],
        )

        os.makedirs(dossier_historique, exist_ok=True)
        sauvegarde = os.path.join(dossier_historique, nom_fichier)
        shutil.copy2(caller_file, sauvegarde)

        if _CONFIG_SAUVEGARDE["log"]:
            print(f"✅ Sauvegarde : {sauvegarde}")

        # Nettoyage des anciennes sauvegardes
        dossier_parent = os.path.join(
            nom_repertoire, "Historic", _CONFIG_SAUVEGARDE["nameProject"]
        )
        dossiers = sorted(
            [
                d
                for d in os.listdir(dossier_parent)
                if os.path.isdir(os.path.join(dossier_parent, d))
            ],
            reverse=True,
        )
        for ancien in dossiers[_CONFIG_SAUVEGARDE["limit"] :]:
            shutil.rmtree(os.path.join(dossier_parent, ancien))

    except Exception as e:
        if _CONFIG_SAUVEGARDE["log"]:
            print(f"❌ Erreur sauvegardeAuto: {e}")


def raise_mac_app():
    import os

    script = f"""
    tell application "System Events"
        set frontmost of the first process whose unix id is {os.getpid()} to true
    end tell
    """
    os.system(f"osascript -e '{script}'")


def safe_where_date(col: str, op: str, valeur: str) -> dict:
    """
    Génère une condition sécurisée pour une requête SQL sans injection.
    Exemple :
        safe_where_date("date", ">=", "2025-05-22")
        ➜ {"date": ">= '2025-05-22'"}
    """
    valeur = valeur.replace("'", "''")  # échappe toute apostrophe
    return {col: f"{op} '{valeur}'"}


# Fonction utilitaire pour la confirmation qui utilise soit dialogs soit input
# selon l'environnement
def demander_confirmation(message):
    """
    Demande une confirmation à l'utilisateur.
    exemple :
        demander_confirmation("Voulez-vous vraiment supprimer ce jour ?")

    Args:
        message (str): Message à afficher

    Returns:
        bool: True si confirmation, False sinon
    """
    try:
        import dialogs  # Spécifique à Pythonista
    except ImportError:
        dialogs = None  # Pour Python standard

    if dialogs:
        # Utiliser alert() avec un seul bouton OK
        result = dialogs.alert(message, "Confirmation", "OK")
        # Si l'utilisateur clique sur OK, retourne True, sinon False
        return result == "OK"
    else:
        return input(f"{message} (O/N)").lower() == "o"


# def calendar_png_maker(
#     anMois, jourAencadre, jourEnRouge, texteMultiligneSouscalendrier
# ):
#     """
#     Génère et enregistre une image PNG contenant un calendrier mensuel adapté aux écrans de smartphone.

#     Chaque jour du mois est correctement positionné selon son jour de semaine réel.
#     Les jours spécifiés sont surlignés ou encadrés, et un texte explicatif s'affiche sous le calendrier.

#     Args:
#         anMois (date) : Date (année + mois) utilisée comme base du calendrier.
#         jourAencadre (list[int]) : Liste des jours (numériques) à encadrer en bleu.
#         jourEnRouge (list[int]) : Liste des jours (numériques) à afficher en rouge.
#         texteMultiligneSouscalendrier (str) : Texte multi-ligne à afficher en bas de l’image.

#     Returns:
#         str : Chemin du fichier PNG généré (ex: "2025_05.png").
#     """
#     from PIL import Image, ImageFont, ImageDraw
#     import calendar
#     from io import BytesIO

#     largeur, hauteur = 420, 800
#     cal_img = Image.new("RGB", (largeur, hauteur), "white")
#     draw = ImageDraw.Draw(cal_img)

#     try:
#         font = ImageFont.truetype("Luciole-Regular-Italic.ttf", 24)
#     except IOError:
#         font = ImageFont.load_default()

#     titre = f"{dateFr(anMois, 'mois')} {anMois.year}"
#     draw.text((20, 20), titre, font=font, fill="black")

#     cell_w, cell_h = 55, 60
#     x0, y0 = 20, 70

#     jours_ord = [JOURS_FR_ABR[i] for i in range(1, 8)]
#     for idx, nom_jour in enumerate(jours_ord):
#         x = x0 + idx * cell_w
#         draw.text((x + 10, y0), nom_jour, font=font, fill="black")

#     y0 += cell_h

#     cal = calendar.Calendar(firstweekday=0)
#     mois_jours = cal.itermonthdays(anMois.year, anMois.month)

#     week = 0
#     for idx, jour in enumerate(mois_jours):
#         col = idx % 7
#         if col == 0 and idx > 0:
#             week += 1
#         if jour == 0:
#             continue

#         x = x0 + col * cell_w
#         y = y0 + week * cell_h
#         draw.rectangle([x, y, x + cell_w, y + cell_h], outline="black")

#         fill = "red" if jour in jourEnRouge else "black"
#         draw.text((x + 5, y + 5), str(jour), font=font, fill=fill)

#         if jour in jourAencadre:
#             draw.rectangle(
#                 [x + 2, y + 2, x + cell_w - 2, y + cell_h - 2], outline="blue", width=2
#             )
#     try:
#         font12 = ImageFont.truetype("Luciole-Regular-Italic.ttf", 12)
#     except IOError:
#         font12 = ImageFont.load_default()

#     lines = texteMultiligneSouscalendrier.split("\n")
#     y_text = y0 + (week + 1) * cell_h + 30
#     for line in lines:
#         draw.text((20, y_text), line, font=font12, fill="black")
#         y_text += font12.getbbox(line)[3] + 10

#     nom_fichier = f"{anMois.year}_{dateFr(anMois, 'mois')}.png"
#     with open(nom_fichier, "wb") as f:
#         cal_img.save(f, format="PNG")

#     return nom_fichier


def calendar_png_maker(
    anMois, jourAencadre, jourEnRouge, texteMultiligneSouscalendrier
):
    from PIL import Image, ImageFont, ImageDraw
    import calendar
    from io import BytesIO

    largeur, hauteur = 420, 800
    cal_img = Image.new("RGB", (largeur, hauteur), "#bddac0")
    draw = ImageDraw.Draw(cal_img)

    try:
        font_jour = ImageFont.truetype("Luciole-Regular-Italic.ttf", 24)
        font_titre = ImageFont.truetype("Luciole-Regular-Italic.ttf", 40)
        font_calnum = ImageFont.truetype("Luciole-Regular-Italic.ttf", 26)
        font12 = ImageFont.truetype("Luciole-Regular-Italic.ttf", 12)
    except IOError:
        font_jour = font_titre = font_calnum = font12 = ImageFont.load_default()

    # Titre centré
    titre = f"{dateFr(anMois, 'mois')} {anMois.year}"
    w = draw.textlength(titre, font=font_titre)
    draw.text(((largeur - w) // 2, 20), titre, font=font_titre, fill="black")

    # Entêtes des jours
    cell_w, cell_h = 55, 60
    x0, y0 = 20, 90
    jours_ord = [JOURS_FR_ABR[i] for i in range(1, 8)]
    for idx, nom_jour in enumerate(jours_ord):
        x = x0 + idx * cell_w
        draw.text((x + 5, y0), nom_jour, font=font_jour, fill="black")

    y0 += cell_h

    cal = calendar.Calendar(firstweekday=0)
    mois_jours = list(cal.itermonthdays(anMois.year, anMois.month))

    semaine = 0
    for idx, jour in enumerate(mois_jours):
        col = idx % 7
        if idx > 0 and col == 0:
            semaine += 1
        if jour == 0:
            continue

        x = x0 + col * cell_w
        y = y0 + semaine * cell_h
        txt = str(jour)
        fill = "red" if jour in jourEnRouge else "black"
        draw.text((x + 10, y + 8), txt, font=font_calnum, fill=fill)

        if jour in jourAencadre:
            # Détection fine du centre du texte
            txt = str(jour)
            bbox = draw.textbbox((0, 0), txt, font=font_calnum)
            w_txt = bbox[2] - bbox[0]
            h_txt = bbox[3] - bbox[1]
            decalage_x = -4  # vers la gauche (− = gauche, + = droite)
            decalage_y = -9  # vers le haut (− = haut, + = bas)

            cx = x + (cell_w // 2) + decalage_x
            cy = y + (cell_h // 2) + decalage_y

            base_r = max(w_txt, h_txt) // 2 + 10

            for _ in range(5):
                r = base_r + random.randint(-2, 2)
                dx = random.randint(-2, 2)
                dy = random.randint(-2, 2)
                draw.ellipse(
                    [
                        (cx - r + dx, cy - r + dy),
                        (cx + r + dx, cy + r + dy),
                    ],
                    outline="red",
                    width=1,
                )

    # Texte multi-ligne
    lines = texteMultiligneSouscalendrier.split("\n")
    y_text = y0 + (semaine + 1) * cell_h + 20
    for line in lines:
        draw.text((20, y_text), line, font=font12, fill="black")
        y_text += font12.getbbox(line)[3] + 10

    nom_fichier = f"{anMois.year}_{dateFr(anMois, 'mois')}.png"
    with open(nom_fichier, "wb") as f:
        cal_img.save(f, format="PNG")

    return nom_fichier


def tous_les_jours_du_mois(mois: date):
    """
    Retourne tous les jours d'un mois sous forme de liste d'objets date.

    Args:
        mois (date): Date quelconque du mois (année et mois seront utilisés)

    Returns:
        list: Liste des dates pour chaque jour du mois
    """
    annee = mois.year
    mois_num = mois.month

    # calendar.monthrange retourne (jour de la semaine du premier jour, nombre de jours dans le mois)
    _, nb_jours = calendar.monthrange(annee, mois_num)

    return [date(annee, mois_num, jour) for jour in range(1, nb_jours + 1)]


def lire_jours_feries(moisan: date):
    """
    Lit les jours fériés du mois depuis le fichier CSV.

    Args:
        moisan (date): Date du mois à analyser

    Returns:
        list: Liste des dates complètes des jours fériés
    """
    import csv
    from pathlib import Path

    try:
        # Vérifier que le fichier existe
        if not Path("jours_feries_metropole.csv").exists():
            print("Le fichier jours_feries_metropole.csv n'existe pas")
            return []

        jours_feries = []
        with open("jours_feries_metropole.csv", "r", encoding="utf-8") as f:
            lecteur = csv.DictReader(f)
            for ligne in lecteur:
                # Vérifier que la ligne contient une date valide
                if "date" in ligne and ligne["date"]:
                    try:
                        date_ferie = date.fromisoformat(ligne["date"])
                        if (
                            date_ferie.month == moisan.month
                            and date_ferie.year == moisan.year
                        ):
                            jours_feries.append(date_ferie)
                    except ValueError:
                        print(f"Date invalide dans le fichier: {ligne['date']}")
        return jours_feries
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier jours_feries: {str(e)}")
        return []


def retourneLe1DuMoisAvant(d: date) -> date:
    """
    Retourne le 1er du mois précédent

    Args:
        d (date): Date quelconque

    Returns:
        date: 1er du mois précédent
    """
    if d.month == 1:
        return date(d.year - 1, 12, 1)
    return date(d.year, d.month - 1, 1)


# === Bas de fichier / divers ===
sauvegardeAuto()

if __name__ == "__main__":
    print(retourneLe1DuMoisAvant(date.today()))
    print(retourneLe1DuMoisAvant(date(2025, 1, 1)))

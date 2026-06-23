# Accidents FR — Analyse de l'accidentologie routière française 🚦

> Application web d'analyse et de visualisation des accidents de la route en France (2005–2024), construite avec Python, Streamlit et DuckDB sur le dataset BAAC officiel.

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?logo=streamlit)](https://streamlit.io/)
[![DuckDB](https://img.shields.io/badge/DuckDB-latest-yellow)](https://duckdb.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Aperçu

**Accidents FR** est une application analytique full-stack permettant d'explorer **1 286 097 accidents** recensés sur 20 ans de données BAAC (Bulletin d'Analyse des Accidents Corporels). Elle offre des visualisations interactives, des filtres dynamiques et un espace sécurisé par rôle utilisateur.

### Chiffres clés du dataset

| Indicateur | Valeur |
|---|---|
| Accidents analysés | 1 286 097 |
| Tués sur la période | 77 427 |
| Période couverte | 2005 – 2024 |
| Source | BAAC — data.gouv.fr |

---

## Fonctionnalités

- **Dashboard interactif** — KPIs dynamiques, évolution temporelle, cartographie des accidents par département
- **Filtres multi-dimensionnels** — année, type de route, conditions météo, luminosité, gravité
- **Analyse comparative** — comparaisons annuelles, saisonnières et géographiques
- **Authentification sécurisée** — système de rôles (admin / utilisateur) avec hachage bcrypt (12 rounds)
- **Rate limiting** — protection contre les attaques par force brute
- **Interface responsive** — compatible desktop et mobile avec gestion de session robuste

---

## Stack technique

```
accidents-fr/
├── app/
│   ├── controllers/      # Logique métier (MVC)
│   ├── models/           # Accès données DuckDB + TinyDB
│   ├── views/            # Composants Streamlit
│   └── utils/            # Sécurité, session, helpers
├── data/
│   └── pipeline/         # ETL : CSV bruts → nettoyage → DuckDB
├── tests/
└── requirements.txt
```

| Couche | Technologie | Rôle |
|---|---|---|
| Frontend | Streamlit | Interface utilisateur |
| Backend | Python 3.11 | Logique applicative (MVC) |
| Base de données | DuckDB | Requêtes analytiques rapides |
| Authentification | bcrypt (12 rounds) | Hachage sécurisé des mots de passe |
| Metadata | TinyDB | Stockage utilisateurs et sessions |
| Visualisation | Plotly | Graphiques interactifs |
| Manipulation données | Pandas | ETL et transformations |

---

## Pipeline ETL

```
Fichiers CSV BAAC (data.gouv.fr)
        │
        ▼
Nettoyage & normalisation (Pandas)
  - Gestion des valeurs manquantes
  - Typage des colonnes
  - Fusion des fichiers annuels
        │
        ▼
Chargement DuckDB
  - Indexation pour performances
  - Requêtes analytiques optimisées
        │
        ▼
Visualisation Streamlit / Plotly
```

---

## Sécurité

- Mots de passe hachés avec **bcrypt (cost factor 12)** — migration depuis SHA-256 avec compatibilité ascendante
- **Rate limiting** sur les tentatives de connexion
- Gestion de session avec double fallback (chemins absolus) pour stabilité mobile
- Injection SQL impossible via l'ORM DuckDB paramétré

---

## Installation

```bash
# Cloner le dépôt
git clone https://github.com/datarockstars/accidents-fr.git
cd accidents-fr

# Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Windows : .venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run app/main.py
```

> **Note** : les fichiers de données volumineux (DuckDB, CSV bruts) ne sont pas versionnés. Consulter `data/README.md` pour les instructions de téléchargement.

---

## Captures d'écran

> *(À ajouter : screenshot du dashboard principal, de la carte, et de la page de connexion)*

---

## Modélisation des données

Le projet inclut une modélisation complète **Merise** (MCD, MLD, MPD) documentée dans le rapport technique, ainsi que des diagrammes UML (cas d'utilisation, séquence, classes).

---

## Auteur

**Merwan Laamari**
Concepteur Développeur d'Applications — ITIC Paris (RNCP Niveau 6 / Bac+3)
Transition vers la Data Analytics — disponible à partir de septembre 2025

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Merwan_Laamari-blue?logo=linkedin)](https://linkedin.com/in/TONPROFIL)
[![GitHub](https://img.shields.io/badge/GitHub-datarockstars-black?logo=github)](https://github.com/datarockstars)

---

## Licence

MIT — voir [LICENSE](LICENSE)

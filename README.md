---

## Installation locale

### Prérequis

- Python 3.11+
- pip

### Démarrage

```bash
# 1. Cloner le repo
git clone https://github.com/merwan-crypto/baac-analytics.git
cd baac-analytics

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'application
streamlit run main.py
```

> La base de données DuckDB (~633 Mo) est téléchargée automatiquement depuis la Release GitHub au premier lancement.

### Identifiants de démo

| Rôle | Email | Mot de passe |
|---|---|---|
| Admin | `admin@baac.fr` | `admin123` |

---

## Données

Source officielle : **ONISR** (Observatoire National Interministériel de la Sécurité Routière)  
Fichiers BAAC — open data disponible sur [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2023/)

| Indicateur | Valeur |
|---|---|
| Accidents | 1 286 097 |
| Véhicules impliqués | 2 195 602 |
| Usagers impliqués | 2 884 290 |
| Tués (30 jours) | 77 427 |
| Période | 2005 – 2024 |

---

## Sécurité

- Mots de passe hashés en **bcrypt** (12 rounds) avec migration automatique depuis SHA-256
- Requêtes SQL **paramétrées** (protection injection)
- **Rate limiting** : 5 tentatives max, verrou 60 secondes
- Fichiers sensibles exclus du versioning

---

## Auteur

**Merwan Laamari** — Titre Professionnel Concepteur Développeur d'Applications (Bac+3 RNCP Niveau 6)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-merwan--laamari-0A66C2?logo=linkedin)](https://linkedin.com/in/merwan-laamari)
[![GitHub](https://img.shields.io/badge/GitHub-merwan--crypto-181717?logo=github)](https://github.com/merwan-crypto)

---

## Licence

MIT — voir [LICENSE](LICENSE)
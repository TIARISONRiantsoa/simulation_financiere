# Simulation Financière

Modélisation de l'évolution d'un capital de réserve par résolution numérique
d'une équation différentielle (méthode de **Runge-Kutta 4**), avec stockage
des résultats en base **MySQL** et visualisation **interactive** en Python.

## Fonctionnement

Le projet s'articule en trois étapes :

1. **C# (`csharp/`)** — calcule une suite de valeurs avec la méthode RK4
   et les insère dans la base MySQL (table `echeance`).
2. **MySQL (`database/`)** — stocke le schéma complet d'un système de gestion
   de prêts (clients, prêts, échéances, paiements...), dont la table
   `echeance` utilisée ici.
3. **Python (`python/`)** — relit les données insérées, recalcule la même
   courbe RK4, et l'affiche dans un graphe interactif avec deux curseurs :
   le capital initial (y0) et le pas de temps (h).

## Stack

- C# (.NET 10) — `MySql.Data`
- MySQL
- Python — `matplotlib`, `mysql-connector-python`

## Installation et lancement

### 1. Créer la base de données

```sql
CREATE DATABASE financement;
```

Puis exécuter le script `database/creation_table.sql` sur cette base
(par exemple via phpMyAdmin, ou en ligne de commande) :

```bash
mysql -u root financement < database/creation_table.sql
```

### 2. Lancer le calcul C#

```bash
cd csharp
dotnet run
```

Par défaut, l'application se connecte à `localhost` avec l'utilisateur `root`
sans mot de passe (config type Laragon/XAMPP). Pour utiliser d'autres
identifiants, définir la variable d'environnement `DB_CONNECTION_STRING` :

```bash
export DB_CONNECTION_STRING="Server=localhost;Database=financement;Uid=root;Pwd=motdepasse;"
```

### 3. Lancer la visualisation Python

```bash
cd python
pip install -r requirements.txt
python graphe.py
```

Les identifiants de connexion peuvent aussi être surchargés via les variables
d'environnement `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`.

## Auteur

TIARISON Riantsoa — [GitHub](https://github.com/TIARISONRiantsoa)

# 😎 SQLingo

Entraîne-toi au SQL !

## Comment ça marche

Au lancement, tu sélectionnes les thèmes que tu veux travailler. SQLingo mélange les exercices et te les présente un par un. Si tu réponds correctement, l'exercice disparaît de la queue. Sinon, il revient quelques exercices plus tard. En fin de session, tu vois ton score et la liste des exercices à retravailler.

## Thèmes disponibles

- Cross joins, Inner joins, Left joins, Full outer joins, Self joins
- Group by
- Case when
- Grouping sets

## Stack

- **[Streamlit](https://streamlit.io/)** — interface web interactive en Python
- **[DuckDB](https://duckdb.org/)** — base de données embarquée pour exécuter les requêtes SQL
- **[uv](https://github.com/astral-sh/uv)** — gestion des dépendances

## Choix techniques

**Pas de compte utilisateur.** La progression est gérée entièrement via `st.session_state`. Une queue d'exercices mélangée au démarrage, repositionnée selon les résultats.

**DuckDB comme moteur SQL.** Pas de serveur à configurer, DuckDB tourne directement dans le process Python et exécute des requêtes SQL.

**Une seule source de vérité pour les exercices.** Tous les exercices sont définis dans `exercises.yaml`. Ajouter un exercice ne nécessite pas de toucher au code Python.

**Comparaison order-insensitive.** La vérification des requêtes trie les deux DataFrames avant comparaison — une requête correcte sans `ORDER BY` explicite n'est pas pénalisée.

## Lancer le projet

```bash
make start   # install + init DB + lance l'app
```

Les commandes disponibles :

```bash
make install  # installe les dépendances (uv sync)
make init     # initialise la base de données
make run      # lance l'application
make reset    # repart d'une DB vierge
```

## Structure

```
SQLingo/
├── app.py            # Point d'entrée, routing entre les écrans
├── db.py             # Initialisation DB et connexion partagée
├── utils.py          # Logique SRS, vérification des requêtes, affichage
├── config.py         # Chemins et constantes globales
├── exercises.yaml    # Source de vérité pour tous les exercices
└── Exercices/
    ├── answers/      # Fichiers SQL solution par thème
    └── questions/    # Énoncés Markdown par thème
```

## Ajouter un exercice

1. Ajouter un bloc dans `exercises.yaml`
2. Créer le fichier `Exercices/questions/<theme>/<name>.md`
3. Créer le fichier `Exercices/answers/<theme>/<name>.sql`

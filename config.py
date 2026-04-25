"""Constantes globales pour le projet SQLingo."""

from pathlib import Path

# Paramètres chemin d'accès
DB_PATH = Path("exercices_tables.duckdb")
EXERCICES_PATH = Path("Exercices.yaml")
QUESTIONS_PATH = Path("Exercices/questions")
ANSWERS_PATH = Path("Exercices/answers")

# Paramètres SRS
SRS_CORRECT_DELAY = None
SRS_INCORRECT_DELAY = 3

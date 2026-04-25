"""
utils.py — Fonctions utilitaires de SQLingo.

Ce module contient :
  - Le chargement des exercices depuis exercises.yaml
  - L'initialisation de la session SRS-like
  - La vérification des requêtes utilisateur
  - L'affichage des questions et tables
"""

import random

import pandas as pd
import streamlit as st
import yaml

from config import (
    EXERCISES_PATH,
    ANSWERS_PATH,
    QUESTIONS_PATH,
    SRS_INCORRECT_DELAY,
)


# ------------------------------------------------------------
# CHARGEMENT DES EXERCICES
# ------------------------------------------------------------


def load_exercises() -> list[dict]:
    """Charge la liste des exercices depuis exercises.yaml.

    Returns:
        list[dict]: liste de dicts avec les clés theme, name, tables, answer.
    """
    with EXERCISES_PATH.open("r") as f:
        return yaml.safe_load(f)


# ------------------------------------------------------------
# SESSION SRS-LIKE
# ------------------------------------------------------------


def init_session(themes: list[str] | None = None) -> None:
    """Initialise la session Streamlit avec une queue d'exercices mélangée.

    Args:
        themes: si fourni, filtre les exercices sur ces thèmes uniquement.
                si None, tous les exercices sont inclus.
    """
    exercises = load_exercises()

    if themes:
        exercises = [e for e in exercises if e["theme"] in themes]

    random.shuffle(exercises)

    st.session_state["queue"] = exercises
    st.session_state["score"] = {"correct": 0, "incorrect": 0}
    st.session_state["history"] = []  # liste de (exercise, "correct" | "incorrect")
    st.session_state["session_started"] = True


def get_current_exercise() -> dict | None:
    """Retourne l'exercice en tête de queue, ou None si la session est terminée."""
    queue = st.session_state.get("queue", [])
    return queue[0] if queue else None


def record_result(exercise: dict, correct: bool) -> None:
    """Enregistre le résultat et repositionne l'exercice dans la queue.

    - Bonne réponse  → exercice retiré de la queue (ne revient pas)
    - Mauvaise réponse → exercice réinséré à la position SRS_INCORRECT_DELAY
    """
    queue = st.session_state["queue"]
    result = "correct" if correct else "incorrect"

    st.session_state["history"].append((exercise, result))

    if correct:
        st.session_state["score"]["correct"] += 1
        queue.pop(0)
    else:
        st.session_state["score"]["incorrect"] += 1
        queue.pop(0)
        insert_at = min(SRS_INCORRECT_DELAY, len(queue))
        queue.insert(insert_at, exercise)


# ------------------------------------------------------------
# VÉRIFICATION DE LA REQUÊTE UTILISATEUR
# ------------------------------------------------------------


def check_users_solution(con, solution_df: pd.DataFrame, user_query: str) -> bool:
    """Vérifie que la requête SQL de l'utilisateur produit le bon résultat.

    La comparaison est insensible à l'ordre des lignes : les deux DataFrames
    sont triés avant d'être comparés.

    Args:
        con: connexion DuckDB active
        solution_df: DataFrame de référence (la solution attendue)
        user_query: requête SQL saisie par l'utilisateur

    Returns:
        bool: True si la requête est correcte, False sinon.
    """
    try:
        result = con.execute(user_query).df()
        st.dataframe(result)

        # Colonnes
        if list(result.columns) != list(solution_df.columns):
            st.warning(
                f"Colonnes incorrectes.\n\n"
                f"**Attendu :** {list(solution_df.columns)}\n\n"
                f"**Obtenu :** {list(result.columns)}"
            )
            return False

        # Nombre de lignes
        if len(result) != len(solution_df):
            st.warning(
                f"Nombre de lignes incorrect : "
                f"ta requête retourne **{len(result)}** lignes, "
                f"la solution en attend **{len(solution_df)}**."
            )
            return False

        # Valeurs (order-insensitive)
        result_sorted = result.sort_values(by=list(result.columns)).reset_index(
            drop=True
        )
        solution_sorted = solution_df.sort_values(
            by=list(solution_df.columns)
        ).reset_index(drop=True)  # noqa: E501

        if not result_sorted.equals(solution_sorted):
            st.warning(
                "Les colonnes et le nombre de lignes sont bons, mais certaines valeurs différent."
            )  # noqa: E501
            return False

        st.balloons()
        return True

    except Exception as e:
        st.error(f"Erreur lors de l'exécution de ta requête : {e}")
        return False


# ------------------------------------------------------------
# AFFICHAGE
# ------------------------------------------------------------


def show_question(exercise: dict) -> None:
    """Affiche l'énoncé markdown de l'exercice courant.

    Args:
        exercise: dict d'un exercice chargé depuis exercises.yaml
    """
    theme = exercise["theme"]
    answer = exercise["answer"]
    question_file = QUESTIONS_PATH / theme / f"{answer[:-4]}.md"

    try:
        st.markdown(question_file.read_text())
    except FileNotFoundError:
        st.warning(f"Énoncé introuvable : `{question_file}`")


def show_tables(con, exercise: dict) -> None:
    """Affiche un aperçu des tables nécessaires à l'exercice.

    Args:
        con: connexion DuckDB active
        exercise: dict d'un exercice chargé depuis exercises.yaml
    """
    for table in exercise["tables"]:
        st.markdown(f"**`{table}`**")
        try:
            df = con.execute(f"SELECT * FROM {table} LIMIT 5").df()
            st.dataframe(df)
        except Exception as e:
            st.error(f"Impossible de charger la table `{table}` : {e}")


def load_solution(con, exercise: dict) -> pd.DataFrame:
    """Charge et exécute le fichier SQL solution, retourne le DataFrame résultat.

    Args:
        con: connexion DuckDB active
        exercise: dict d'un exercice chargé depuis exercises.yaml

    Returns:
        pd.DataFrame: résultat de la requête solution.

    Raises:
        FileNotFoundError: si le fichier SQL solution est absent.
    """
    answer_file = ANSWERS_PATH / exercise["theme"] / exercise["answer"]
    sql = answer_file.read_text()
    return con.execute(sql).df()

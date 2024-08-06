# pylint: disable=missing-module-docstring
import os
import sys
import subprocess
import logging

import duckdb
import pandas as pd
import streamlit as st
import functions
from datetime import date

# ------------------------------------------------------------
# SETUP
# ------------------------------------------------------------
# Création du dossier data
if "data" not in os.listdir():
    print("creating folder data")
    logging.error(os.listdir())
    logging.error("creating folder data")
    os.mkdir("data")

# On lance init_db.py pour créer la BDD
if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    # exec(open("init_db.py").read())
    subprocess.run([sys.executable, "init_db.py"])

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# ------------------------------------------------------------
# CONFIG PAGE
# ------------------------------------------------------------
st.set_page_config(
    page_title="SQL_SRS",
    page_icon="😎",
    layout="wide",
)

st.markdown(
    """
                <style>
                .text-font {
                    font-size:20px;
                    text-align: justify;
                }
                </style>
                """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# SETUP
# ------------------------------------------------------------

# Vérifier si le fichier 'exercises_sql_tables.duckdb' n'existe pas dans le répertoire 'data'
if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    result = subprocess.run(["python", "init_db.py"], capture_output=True, text=True)

    # Vérifier si le script s'est exécuté avec succès
    if result.returncode == 0:
        print("Initialisation de la base de données réussie.")
    else:
        print("Erreur lors de l'initialisation de la base de données.")
        print(result.stderr)

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)
memory_df = (
    con.execute("SELECT * FROM memory_state")
    .df()
    .sort_values("last_reviewed")
    .reset_index(drop=True)
)


# --------------------
# Affichage de l'app
# --------------------

with st.sidebar:

    # Forcer le padding de la sidebar pour éviter l'espace blanc en haut
    st.markdown(
        """
    <style>
    .st-emotion-cache-10oheav {
        padding: 1rem 1rem !important;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Titre dans la sidebar
    st.markdown(
        """
        <div style="margin-top: 0px ; text-align: center;">
            <h1>😎 SQLingo 😎</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Sélection du thème
    theme = functions.get_selector_themes(memory_df)

    # Sélection de l'exercice en fonction du thème sélectionné
    exercises_lst = functions.get_selector_exercises(memory_df, theme)

    # Récupérer l'exercice
    exercise, answer_str, answer, solution_df = functions.get_selected_exercise(
        con, theme, exercises_lst
    )


# Affichage des questions dynamiques
st.subheader("Question :")
functions.get_questions(theme, answer_str)

# Saisir la requête
query: str = st.text_area(label="Saisir votre requête SQL :", key="user_input")

# Check de la requête
if query:
    is_solution_correct = functions.check_users_solution(con, solution_df, query)

    # si la solution est ok alors on met à jour la date "last_reviewed"
    if is_solution_correct:
        today = date.today().strftime("%Y-%m-%d")
        exercise_name = exercise.loc[0, "exercise_name"]
        update_query = f"UPDATE memory_state SET last_reviewed = ? WHERE exercise_name = ?"

        with duckdb.connect('data/exercises_sql_tables.duckdb') as conn:
            conn.execute(update_query, (today, exercise_name))
            conn.close()

tab1, tab2 = st.tabs(["Tables", "Solution"])

with tab1:
    exercise_tables: str = exercise.loc[0, "tables"]
    exercise_tables_len: int = len(exercise_tables)
    cols = st.columns(exercise_tables_len)
    for i in range(0, exercise_tables_len):
        cols[i].write(exercise_tables[i])
        df_table = con.execute(f"SELECT * FROM {exercise_tables[i]}").df()
        cols[i].table(df_table)

with tab2:
    st.write(answer)
    st.dataframe(solution_df)

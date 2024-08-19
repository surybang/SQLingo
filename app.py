# pylint: disable=missing-module-docstring
import os
import sys
import subprocess
import logging
from datetime import date, timedelta

import duckdb
import streamlit as st

from functions import (
    get_questions,
    get_selected_exercise,
    get_selector_exercises,
    get_selector_themes,
    check_users_solution,
    query_memory_df,
    signup_user,
    user_auth,
)


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
                        text-align:justify;
                    }
        </style>
    """,
    unsafe_allow_html=True,
)

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
    try:
        subprocess.run([sys.executable, "init_db.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute init_db.py: {e}")

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)
memory_df = query_memory_df(con)
signup_user("guest", "guest")

# ------------------------------------------------------------
# AUTHENT
# ------------------------------------------------------------

user_auth()

if "logged_in" in st.session_state and st.session_state["logged_in"]:
    # --------------------
    # Affichage de l'app
    # --------------------

    with st.sidebar:
        # st.write(f"Bienvenue, {st.session_state['username']}!")

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
        theme = get_selector_themes(memory_df)

        # Sélection de l'exercice en fonction du thème sélectionné
        exercises_lst = get_selector_exercises(memory_df, theme)

        # Récupérer l'exercice
        exercise, answer_str, answer, solution_df = get_selected_exercise(
            con, theme, exercises_lst
        )
        # TODO : Ajuster l'affichage du df en injectant du css pour fixer sa taille

        # user + deconnect
        st.write(f"Vous êtes connecté en tant que {st.session_state['username']}")
        if st.button("Déconnexion"):
            st.session_state["logged_in"] = False
            st.session_state["username"] = None
            st.rerun()
        st.markdown(
            """
            Made with 🍜 by \
            <a href='https://www.linkedin.com/in/fabien-hos/' target='_blank'>Fabien</a>,\
            visitez <a href ='https://fabien-hos.streamlit.app/' target='_blank'>mon site</a> \
            ou mon <a href='https://github.com/surybang' target='_blank'>GitHub</a>.
                    """,
            unsafe_allow_html=True,
        )

    # Affichage des questions dynamiques
    st.subheader("Question :")
    get_questions(theme, answer_str)

    # Saisir la requête
    query = st.text_area(label="Saisir votre requête SQL :", key="user_input")

    # Check de la requête
    if query:
        IS_SOLUTION_CORRECT = check_users_solution(con, solution_df, query)

        # si la solution est ok alors on met à jour la date "last_reviewed"
        if IS_SOLUTION_CORRECT:
            today = date.today()

            # Boutons pour mettre à jour la date de prochaine apparition de la question
            col1, col2, col3 = st.columns(spec=3, gap="small")
            with col1:
                if st.button(label="Revoir dès demain"):
                    next_review_date = today + timedelta(days=1)
            
            with col2:
                if st.button(label="Revoir dans 7 jours"):
                    next_review_date = today + timedelta(days=7)
            
            with col3:
                if st.button(label="Revoir dans 14 jours"):
                    next_review_date = today + timedelta(days=14)

            # Si un bouton a été cliqué, mettre à jour la date
            if 'next_review_date' in locals():
                exercise_name = exercise.loc[0, "exercise_name"]
                UPDATE_QUERY = """
                    UPDATE memory_state SET last_reviewed = ? WHERE exercise_name = ?
                """
                with duckdb.connect("data/exercises_sql_tables.duckdb") as conn:
                    conn.execute(UPDATE_QUERY, (next_review_date.strftime("%Y-%m-%d"), exercise_name))
                    conn.close()
                    # st.rerun()

    tab1, tab2 = st.tabs(["Tables", "Solution"])

    with tab1:
        exercise_tables = exercise.loc[0, "tables"]
        exercise_tables_len = len(exercise_tables)
        cols = st.columns(exercise_tables_len)
        for i in range(0, exercise_tables_len):
            cols[i].write(exercise_tables[i])
            df_table = con.execute(f"SELECT * FROM {exercise_tables[i]}").df()
            cols[i].table(df_table)

    with tab2:
        st.code(answer, language="sql")
        st.dataframe(solution_df)
else:
    st.write("Veuillez vous connecter ou vous inscrire pour continuer.")
    st.write(
        "Si vous ne souhaitez pas vous inscrire \
             vous pouvez utiliser l'identifiant et \
             le mot de passe : guest"
    )

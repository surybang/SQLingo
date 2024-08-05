# pylint: disable=missing-module-docstring
import os
import logging
import subprocess

import duckdb
import pandas as pd
import streamlit as st

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
memory_df = con.execute("SELECT * FROM memory_state").df()

# ------------------ #
# Affichage de l'app #
# ------------------ #

with st.sidebar:
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
    st.markdown(
        """
        <div style="margin-top: 0px ; text-align: center;">
            <h1>😎 SQLingo 😎</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Sélection du thème
    theme = st.selectbox(
        "Sélectionner un thème", options=memory_df["theme"].unique(), index=0
    )

    # Sélection de l'exercice en fonction du thème sélectionné
    filtered_exercises = memory_df[memory_df["theme"] == theme][
        "exercise_name"
    ].to_list()
    exercises_lst = st.selectbox(
        "Sélectionner un exercice", options=filtered_exercises, index=0
    )
    # st.write("Vous avez sélectionné : ", theme)
    exercise = con.execute(
        f"SELECT * FROM memory_state where theme = '{theme}' and exercise_name = '{exercises_lst}'"
    ).df()
    if not exercise.empty:
        st.dataframe(exercise.iloc[:, :-1])  # On affiche pas la colonne réponse
    elif exercise.empty:
        st.write("Il faut sélectionner un thème")
    else:
        st.write("Pas d'exercice disponibles pour le thème sélectionné")


st.subheader('Question :')
query = st.text_area(label="Saisir votre requête SQL :", key="user_input")


if query:
    result = con.execute(query).df()
    st.dataframe(result)

    # try:
    #     result = result[solution_df.columns]
    #     if st.dataframe(result.compare(solution_df)):
    #         st.dataframe(solution_df)
    # except KeyError as e:
    #     st.write("Il manque des colonnes à votre requête")

    # # Comparer le nomnbre de lignes des deux dataframes
    # n_lines_difference = result.shape[0] - solution_df.shape[0]
    # if n_lines_difference != 0:
    #     st.write(
    #         f"Votre requête a {n_lines_difference} lignes différentes de la solution"
    #     )

#     # Comparer les valeurs dans le dataframe


tab2, tab3 = st.tabs(["Tables", "Solution"])
with tab2:
    exercise_tables = exercise.loc[0, "tables"]
    for table in exercise_tables:
        st.write(f"Table : {table}")
        df_tables = con.execute(f"SELECT * from '{table}'").df()
        st.dataframe(df_tables)


# with tab3:
#     answer_str = exercise.loc[0, "answer"]
#     # with open(f"answers/{theme}/{}")
#     st.dataframe(answer_str)

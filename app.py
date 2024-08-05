# pylint: disable=missing-module-docstring
import os
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
    theme = st.selectbox(
        "Sélectionner un thème",
        options=memory_df["theme"].unique(),
        index=0,
        key="theme_selectbox",
    )
    # st.write(f"Vous avez sélectionné :{theme}")

    # Sélection de l'exercice en fonction du thème sélectionné
    filtered_exercises = memory_df[memory_df["theme"] == theme][
        "exercise_name"
    ].to_list()
    exercises_lst = st.selectbox(
        "Sélectionner un exercice",
        options=filtered_exercises,
        index=0,
        key="exercises_selectbox",
    )

    # Récupérer l'exercice
    exercise = con.execute(
        f"SELECT * FROM memory_state where theme = '{theme}' and exercise_name = '{exercises_lst}'"
    ).df()
    # st.write('Vous avez sélectionné', exercise)
    if not exercise.empty:
        st.dataframe(exercise.iloc[:, :-1])  # On affiche pas la colonne réponse
    elif exercise.empty:
        st.write("Il faut sélectionner un thème")
    else:
        st.write("Pas d'exercice disponibles pour le thème sélectionné")

    # Récupérer la solution de l'exercice
    answer_str: str = exercise.loc[0, "answer"]
    try:
        with open(f"answers/{theme}/{answer_str}", "r") as f:
            answer: str = f.read()
            solution_df: pd.DataFrame = con.execute(answer).df()

    except FileNotFoundError:
        st.write("Fichier de réponse non trouvé")

st.subheader("Question :")
query: str = st.text_area(label="Saisir votre requête SQL :", key="user_input")


if query:
    result: pd.DataFrame = con.execute(query).df()
    st.dataframe(result)

    try:
        result = result[solution_df.columns]
        check_valid = result.compare(solution_df)
        if check_valid.empty:
            st.balloons()
        else :
            st.write("Il y a une différences dans votre requête")
    except KeyError as e:
        st.write("Il manque des colonnes à votre requête")

    # Comparer le nomnbre de lignes des deux dataframes
    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(
            f"Votre requête a {n_lines_difference} lignes différentes de la solution"
        )


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

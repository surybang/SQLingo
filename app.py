# pylint: disable=missing-module-docstring
import io

import duckdb
import pandas as pd
import streamlit as st

# --------------------- #
# Récupérer les données #
# --------------------- #
con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)


# ------------------ #
# Affichage de l'app #
# ------------------ #
st.title(":sunglasses: SQLingo :sunglasses:")


with st.sidebar:
    theme = st.selectbox(
        "Que voulez-vous réviser ?",
        (
            "cross_joins",
            "inner_joins",
            "left_joins",
            "full_outer_joins",
            "self_joins",
            "group_by",
            "case_when",
            "grouping_set",
        ),
        index=None,
        placeholder="Sélectionner un thème",
    )
    st.write("Vous avez sélectionné : ", theme)
    exercise = con.execute(f"SELECT * FROM memory_state where theme = '{theme}'").df()
    if not exercise.empty:
        st.write(exercise)
    elif exercise.empty:
        st.write("Il faut sélectionner un thème")
    else:
        st.write("Pas d'exercice disponibles pour le thème sélectionné")

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


with tab3:
    answer_str = exercise.loc[0, "answer"]
    st.dataframe(answer_str)

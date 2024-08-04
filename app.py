# pylint: disable=missing-module-docstring
import io

import duckdb
import pandas as pd
import streamlit as st

# pourquoi check_code_quality bug ?
CSV = """
beverage, price
orange juice, 2.5
Expresso, 2
Tea, 3
"""
beverages : pd.DataFrame = pd.read_csv(io.StringIO(CSV))

CSV2 = """
food_item, food_price
cookie juice, 2.5
chocolatine, 2
muffin, 3
"""
food_items : pd.DataFrame = pd.read_csv(io.StringIO(CSV2))


ANSWER = """
SELECT * FROM beverages
CROSS JOIN food_items
"""

solution_df : pd.DataFrame = duckdb.sql(ANSWER).df()


# ------------------ #
# Affichage de l'app #
# ------------------ #
st.title(":sunglasses: SQLingo :sunglasses:")


with st.sidebar:
    option = st.selectbox(
        "Que voulez-vous réviser ?",
        ("Joins", "Groupby", "Windows Functions"),
        index=None,
        placeholder="Sélectionner un thème",
    )
    st.write("Vous avez sélectionné : ", option)


query = st.text_area(label="Saisir votre requête SQL :", key="user_input")


if query:
    result = duckdb.sql(query).df()
    st.dataframe(result)

    # Comparer le nombre de colonnes des deux dataframes
    if len(result.columns) != len(solution_df.columns):
        st.write("Il manque des colonnes à votre requête")

    try:
        result = result[solution_df.columns]
        if st.dataframe(result.compare(solution_df)):
            st.dataframe(solution_df)
    except KeyError as e:
        st.write("Il manque des colonnes à votre requête")

    # Comparer le nomnbre de lignes des deux dataframes
    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(
            f"Votre requête a {n_lines_difference} lignes différentes de la solution"
        )

    # Comparer les valeurs dans le dataframe


tab2, tab3 = st.tabs(["Tables", "Solution"])
with tab2:
    st.dataframe(beverages)


with tab3:
    st.dataframe(solution_df)

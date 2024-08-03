import streamlit as st 
import pandas as pd 
import duckdb
import os 
import io


csv = '''
beverage, price
orange juice, 2.5
Expresso, 2
Tea, 3
'''
beverages = pd.read_csv(io.StringIO(csv))

csv2 = '''
food_item, food_price
cookie juice, 2.5
chocolatine, 2
muffin, 3
'''
food_items = pd.read_csv(io.StringIO(csv2))


answer = '''
SELECT * FROM beverages
CROSS JOIN food_items
'''

solution = duckdb.sql(answer).df()



# ------------------ #
# Affichage de l'app #
# ------------------ #
st.title('SQLingo')




with st.sidebar:
    option = st.selectbox(
        "Que voulez-vous réviser ?",
        ("Joins", "Groupby", "Windows Functions"),
        index=None,
        placeholder="Sélectionner un thème",
    )
    st.write("Vous avez sélectionné : ", option)


st.header("Saisir votre requête SQL :")
query = st.text_area(label="Juste ici", key="user_input")

if query : 
    result = duckdb.sql(query).df()
    st.dataframe(result)

    # Comparer le nombre de colonnes des deux dataframes
    if len(result.columns) != len(solution.columns):
        st.write("Il manque des colonnes à votre requête")

    # Comparer le nomnbre de lignes des deux dataframes 
    n_lines_difference = result.shape[0] - solution.shape[0]
    if n_lines_difference != 0 : 
        st.write(f"Votre requête a {n_lines_difference} lignes différentes de la solution")



tab2, tab3 = st.tabs (["Tables", "Solution"])

with tab2: 
    st.dataframe(beverages)


with tab3: 
    st.dataframe(solution)
        
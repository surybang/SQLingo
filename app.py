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


# Les onglets
tabs = st.tabs(["Tables", "Solutions"])

# Streamlit version 1.32.2 -> obliger de déclarer ce qu'est tab1 de cette façon 
# au lieu de tab1, tab2 ... = st.tabs(['t1', 't2', ...])
tab1 = tabs[0]
tab2 = tabs[1]

with tab1: 
    sql_query = st.text_area(label="Entrez votre texte")
    
    if sql_query:
        try:
            results = duckdb.sql(sql_query).df()
            st.write(f"La réponse attendue est la suivante : {answer}")
            st.dataframe(results)
        except Exception as e:
            st.error(f"Error executing query: {e}")
        if sql_query == answer:
            st.write("Bravo vous avez la bonne réponse !")
    else:
        st.write("Please enter a SQL query.")

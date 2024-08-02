import streamlit as st 
import pandas as pd 
import duckdb
import numpy as np

st.title('SQLingo')

data = {"a": [1, 2, 3], "b": [4, 5, 6]}
df = pd.DataFrame(data)

# Create a DuckDB connection
conn = duckdb.connect()
# Changement de méthode pour duckdb
# il est maintenant nécessaire de déclarer le nom de la table "logique"
# on ne peut plus utiliser l'objet dataframe df directement
conn.register('data', df)

# Les onglets
tabs = st.tabs(["First tab"])

# Streamlit version 1.32.2 -> obliger de déclarer ce qu'est tab1 de cette façon 
# au lieu de tab1, tab2 ... = st.tabs(['t1', 't2', ...])
tab1 = tabs[0]

with tab1: 
    sql_query = st.text_area(label="Entrez votre texte")
    
    if sql_query:
        try:
            results = conn.execute(sql_query).df()
            st.write(f"La requête saisie est la suivante : {sql_query}")
            st.dataframe(results)
        except Exception as e:
            st.error(f"Error executing query: {e}")
    else:
        st.write("Please enter a SQL query.")

#refaire l'authent github sur wsl 
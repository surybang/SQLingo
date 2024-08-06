import pandas as pd
import streamlit as st

# ------------------------------------------------------------
# FUNCTIONS
# ------------------------------------------------------------
def check_users_solution(con, solution_df: pd.DataFrame, user_query: str) -> bool:
    """
    Checks that user SQL query is correct by :
    1: checking the columns
    2: checking the values
    :param con: connection duckdb
    :param solution_df: THE TRUTH
    :param user_query: string containing the query typed by the user 

    returns : bool indicating wether the user's query matches the solution 
    """
    try:
        # Exécute la requête utilisateur et récupère les résultats dans un DataFrame
        result = con.execute(user_query).df()
        st.dataframe(result)  # Affiche le résultat pour l'utilisateur

        # Vérifie si les colonnes correspondent et dans le bon ordre
        if not result.columns.equals(solution_df.columns):
            st.write("Les colonnes de votre requête ne correspondent pas exactement à celles de la solution.")
            return False

        # Vérifie si le nombre de lignes correspond
        if result.shape[0] != solution_df.shape[0]:
            st.write(f"Votre requête retourne un nombre de lignes différent de la solution attendue ({result.shape[0]} vs {solution_df.shape[0]}).")
            return False

        # Compare les valeurs des deux DataFrames
        if not result.equals(solution_df):
            differences = result.compare(solution_df)
            st.write(f"Il y a des différences dans les valeurs de votre requête : {differences}")
            return False

        st.balloons()  # Affiche des ballons si la requête est correcte
        return True

    except Exception as e:
        # Capture et affiche toute exception survenue lors de l'exécution de la requête ou de la comparaison
        st.write(f"Erreur lors de l'exécution ou de la comparaison des requêtes : {e}")
        return False

 

def get_selector_themes(memory_df : pd.DataFrame) -> str :
    """
    Function to get themes selected by the user
    
    Args:
        memory_df (pd.DataFrame): the memory state df from the database

    Returns:
        str: the theme selected
    """
    theme = st.selectbox(
        "Sélectionner un thème",
        options=memory_df["theme"].unique(),
        index=0,
        key="theme_selectbox",
    )
    
    return theme

def get_selector_exercises(memory_df, theme):
    filtered_exercises = memory_df[memory_df["theme"] == theme][
        "exercise_name"
    ].to_list()
    exercises_lst = st.selectbox(
        "Sélectionner un exercice",
        options=filtered_exercises,
        index=0,
        key="exercises_selectbox",
    )
    
    return exercises_lst

def get_selected_exercise(con, theme, exercises_lst):
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
    return exercise,answer_str,answer,solution_df

def get_questions(theme, answer_str):
    try:
        with open(f"questions/{theme}/{answer_str[:-4]}.txt", "r") as f:
            question: str = f.read()
            st.write(question)
    except FileNotFoundError:
        st.write("Fichier question absent")
        
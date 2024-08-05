import pandas as pd
import streamlit as st

# ------------------------------------------------------------
# FUNCTIONS
# ------------------------------------------------------------
def check_users_solution(con, solution_df: pd.DataFrame, user_query: str) -> None:
    """
    Checks that user SQL query is correct by :
    1: checking the columns
    2: checking the values
    :param con: connection duckdb
    :param solution_df: THE TRUTH
    :param user_query: string containing the query typed by the user 

    returns : nothing 
    """
    result: pd.DataFrame = con.execute(user_query).df()
    st.dataframe(result)

    try:
        result = result[solution_df.columns]
        check_valid = result.compare(solution_df)
        if check_valid.empty:
            st.balloons()
        else:
            st.write("Il y a une différences dans votre requête")
    except KeyError as e:
        st.write("Il manque des colonnes à votre requête")

    # Comparer le nomnbre de lignes des deux dataframes
    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(
            f"Votre requête a {n_lines_difference} lignes différentes de la solution"
        )

def get_selector_themes(memory_df):
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
        
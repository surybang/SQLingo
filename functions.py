import pandas as pd
import streamlit as st
import duckdb
import bcrypt

# ------------------------------------------------------------
# FUNCTIONS
# ------------------------------------------------------------


def hash_password(password: str) -> bytes:
    """Hache un mot de passe en utilisant bcrypt.

    Cette fonction prend un mot de passe en entrée, l'encode en bytes,
    génère un sel aléatoire, et retourne le mdp haché.

    Args:
        password (str): le mot de passe à hacher

    Returns:
        bytes : le mdp haché sous forme de bytes
    """

    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def check_password(hashed_password: bytes, user_password: str) -> bool:
    """Vérifie que le mot de passe est valide.

    Cette fonction prend un mot de passe haché (généré par hash_password) et un mot de passe
    en clair, puis vérifie que le hash du mot de passe en clair correspond au mot de passe haché.

    Args:
        hashed_password (bytes): Le mot de passe haché (résultat de hash_password)
        user_password (str): Le mot de passe en clair à vérifier

    Returns:
        bool: True si le mot de passe est correct, False sinon
    """
    return bcrypt.checkpw(user_password.encode(), hashed_password)


def signup_user(username: str, password: str) -> bool:
    """Inscrit un nouvel utilisateur dans la base de données.

    Cette fonction prend un nom d'utilisateur et un mot de passe, vérifie si l'utilisateur
    existe déjà, et si non, hache le mot de passe et insère ces informations dans la table 'users'.

    Args:
        username (str): Le nom d'utilisateur du nouvel utilisateur.
        password (str): Le mot de passe en clair du nouvel utilisateur.

    Returns:
        bool: True si l'inscription a réussi, False si l'utilisateur existe déjà.

    Raises:
        duckdb.Error: Si une erreur inattendue se produit lors de l'interaction avec la base de données.
    """
    try:
        with duckdb.connect("data/exercises_sql_tables.duckdb") as con:
            # Vérifier si l'utilisateur existe déjà
            result = con.execute(
                "SELECT COUNT(*) FROM users WHERE username = ?", [username]
            ).fetchone()
            if result[0] > 0:
                print(f"L'utilisateur '{username}' existe déjà.")
                return False

            # Si l'utilisateur n'existe pas, procéder à l'inscription
            hashed_password = hash_password(password)
            con.execute(
                """
                INSERT INTO users (username, password) VALUES (?, ?)
            """,
                (username, hashed_password),
            )
            print(f"L'utilisateur '{username}' a été inscrit avec succès.")
            return True
    except duckdb.Error as e:
        print(f"Une erreur s'est produite lors de l'inscription : {e}")
        raise


def login_user(username: str, password: str) -> bool:
    """Vérifie les informations de connexion de l'utilisateur.

    Cette fonction prend un nom d'utilisateur et un mot de passe, vérifie leur validité
    dans la base de données, et retourne True si les informations sont correctes.

    Args:
        username (str): Le nom d'utilisateur à vérifier.
        password (str): Le mot de passe à vérifier.

    Returns:
        bool: True si les informations de connexion sont valides, False sinon.

    Raises:
        duckdb.Error: Si une erreur se produit lors de l'interaction avec la base de données.
    """
    try:
        with duckdb.connect(database="data/exercises_sql_tables.duckdb") as con:
            result = con.execute(
                """
                SELECT password FROM users WHERE username = ?
            """,
                (username,),
            ).fetchone()

            if result:
                hashed_password = result[0].encode()
                return check_password(hashed_password, password)
            return False
    except duckdb.Error as e:
        print(f"Erreur lors de la vérification des informations de connexion : {e}")
        raise


def user_auth() -> None :
    """Affiche le formulaire d'inscription ou de connexion et gère l'authentification de l'utilisateur."""

    # Vérifier si l'utilisateur est déjà connecté
    if st.session_state.get("logged_in", False):
        # st.write(f"Vous êtes connecté en tant que {st.session_state['username']}")
        # if st.button("Déconnexion"):
        #     st.session_state["logged_in"] = False
        #     st.session_state["username"] = None
        #     st.rerun()
        return

    # Initialiser l'état d'inscription s'il n'existe pas
    if "signup" not in st.session_state:
        st.session_state["signup"] = False

    if st.session_state["signup"]:
        st.title("Inscription")
        signup_username = st.text_input("Nom d'utilisateur", key="signup_username")
        signup_password = st.text_input(
            "Mot de passe", type="password", key="signup_password"
        )
        signup_password_confirm = st.text_input(
            "Confirmer le mot de passe", type="password", key="signup_password_confirm"
        )

        if st.button("S'inscrire"):
            if not signup_username or not signup_password:
                st.error("Veuillez remplir tous les champs.")
            elif signup_password != signup_password_confirm:
                st.error("Les mots de passe ne correspondent pas.")
            elif signup_user(signup_username, signup_password):
                st.success(
                    "Inscription réussie. Vous pouvez maintenant vous connecter."
                )
                st.session_state["signup"] = False
            else:
                st.error(
                    "L'utilisateur existe déjà. Essayez un autre nom d'utilisateur."
                )

        if st.button("Retour à la connexion"):
            st.session_state["signup"] = False
    else:
        st.title("Connexion")
        login_username = st.text_input("Nom d'utilisateur", key="login_username")
        login_password = st.text_input(
            "Mot de passe", type="password", key="login_password"
        )

        if st.button("Se connecter"):
            if not login_username or not login_password:
                st.error("Veuillez remplir tous les champs.")
            elif login_user(login_username, login_password):
                st.success("Connexion réussie")
                st.session_state["logged_in"] = True
                st.session_state["username"] = login_username
                st.rerun()
            else:
                st.error("Nom d'utilisateur ou mot de passe incorrect")

        if st.button("S'inscrire"):
            st.session_state["signup"] = True


def query_memory_df(con) -> pd.DataFrame :
    with duckdb.connect(database="data/exercises_sql_tables.duckdb") as con:
        memory_df = (
            con.execute("SELECT * FROM memory_state")
            .df()
            .sort_values("last_reviewed")
            .reset_index(drop=True)
        )

    return memory_df


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
            st.write(
                "Les colonnes de votre requête ne correspondent pas exactement à celles de la solution."
            )
            return False

        # Vérifie si le nombre de lignes correspond
        if result.shape[0] != solution_df.shape[0]:
            st.write(
                f"Votre requête retourne un nombre de lignes différent de la solution attendue ({result.shape[0]} vs {solution_df.shape[0]})."
            )
            return False

        # Compare les valeurs des deux DataFrames
        if not result.equals(solution_df):
            differences = result.compare(solution_df)
            st.write(
                f"Il y a des différences dans les valeurs de votre requête : {differences}"
            )
            return False

        st.balloons()  # Affiche des ballons si la requête est correcte 8)
        return True

    except Exception as e:
        # Capture et affiche toute exception survenue lors de l'exécution de la requête ou de la comparaison
        st.write(f"Erreur lors de l'exécution ou de la comparaison des requêtes : {e}")
        return False


def get_selector_themes(memory_df: pd.DataFrame) -> str:
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


def get_selector_exercises(memory_df: pd.DataFrame, theme: str) -> str:
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


def get_selected_exercise(con, theme: str, exercises_lst: str):
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
    return exercise, answer_str, answer, solution_df


def get_questions(theme: str, answer_str: str) -> None:
    """Récupère les questions depuis un folder

    Args:
        theme (str): thème sélectionné par l'utilisateur
        answer_str (str): nom exercice sélectionné par l'utilisateur
    """
    try:
        with open(f"questions/{theme}/{answer_str[:-4]}.txt", "r") as f:
            question: str = f.read()
            st.write(question)
    except FileNotFoundError:
        st.write("Fichier question absent")

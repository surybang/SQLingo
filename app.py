"""
app.py - Point d'entrée de SQLingo.
"""

import streamlit as st

from db import get_connection, init_db
from utils import (
    check_users_solution,
    get_current_exercise,
    init_session,
    load_exercises,
    load_solution,
    record_result,
    show_question,
    show_tables,
)

# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------

st.set_page_config(
    page_title="SQLingo",
    page_icon="😎",
    layout="wide",
)

# ------------------------------------------------------------
# INITIALISATION DB
# ------------------------------------------------------------

init_db()
con = get_connection()

# ------------------------------------------------------------
# ÉCRAN D'ACCUEIL
# ------------------------------------------------------------


def render_home() -> None:
    st.title("😎 SQLingo")
    st.markdown("Entraîne-toi au SQL avec un système de répétition espacée.")
    st.divider()

    exercises = load_exercises()
    all_themes = sorted({e["theme"] for e in exercises})

    st.subheader("Thèmes")
    selected_themes = []
    cols = st.columns(3)
    for i, theme in enumerate(all_themes):
        with cols[i % 3]:
            if st.checkbox(theme.replace("_", " ").title(), value=True, key=f"theme_{theme}"):
                selected_themes.append(theme)

    st.divider()

    n_selected = sum(1 for e in exercises if e["theme"] in selected_themes)
    st.caption(f"{n_selected} exercice(s) sélectionné(s)")

    if st.button("🚀 Démarrer", disabled=not selected_themes, type="primary"):
        init_session(themes=selected_themes)
        st.rerun()


# ------------------------------------------------------------
# ÉCRAN EXERCICE
# ------------------------------------------------------------

def render_exercise() -> None:
    exercise = get_current_exercise()

    if exercise is None:
        st.session_state["session_started"] = False
        st.session_state["session_finished"] = True
        st.rerun()
        return

    score = st.session_state["score"]
    queue = st.session_state["queue"]
    total = score["correct"] + score["incorrect"] + len(queue)
    done = score["correct"] + score["incorrect"]

    # --- Sidebar ---
    with st.sidebar:
        st.markdown("## 😎 SQLingo")
        st.divider()
        st.metric("✅ Correct", score["correct"])
        st.metric("❌ À revoir", score["incorrect"])
        st.progress(done / total if total else 0)
        st.caption(f"{done} / {total} exercices")
        st.divider()
        if st.button("🏠 Accueil", use_container_width=True):
            st.session_state["session_started"] = False
            st.rerun()

        st.divider()
        st.markdown(
            "Made with 🍜 by "
            "<a href='https://www.linkedin.com/in/fabien-hos/' target='_blank'>Fabien</a>"
            "<br><a href='https://github.com/surybang/SQLingo' target='_blank'>"
            "<img src='https://cdn.simpleicons.org/github' width='16' "
            "style='vertical-align:middle; margin-right:4px;'>Voir sur GitHub</a>",
            unsafe_allow_html=True,
        )

    # --- Contenu principal ---
    theme_label = exercise["theme"].replace("_", " ").title()
    st.markdown(f"**Thème :** {theme_label} · **Exercice :** `{exercise['name']}`")
    st.divider()

    col_question, col_tables = st.columns([3, 2])

    with col_question:
        st.subheader("Question")
        show_question(exercise)

        st.subheader("Ta requête")
        user_query = st.text_area(
            label="Saisir ta requête SQL :",
            height=200,
            key=f"query_{exercise['name']}",
            label_visibility="collapsed",
        )

        if st.button("✅ Valider", type="primary", disabled=not user_query):
            try:
                solution_df = load_solution(con, exercise)
            except FileNotFoundError:
                st.error(f"Fichier solution introuvable pour `{exercise['name']}`.")
                return

            correct = check_users_solution(con, solution_df, user_query)
            record_result(exercise, correct)

            if correct:
                st.success("Bonne réponse ! Exercice suivant →")
                if st.button("Continuer →"):
                    st.rerun()
            else:
                st.error("Pas tout à fait - l'exercice reviendra un peu plus tard.")
                if st.button("Continuer →"):
                    st.rerun()

    with col_tables:
        st.subheader("Tables disponibles")
        show_tables(con, exercise)

    # --- Onglet solution ---
    with st.expander("Voir la solution"):
        try:
            solution_df = load_solution(con, exercise)
            from config import ANSWERS_PATH
            sql = (ANSWERS_PATH / exercise["theme"] / exercise["answer"]).read_text()
            st.code(sql, language="sql")
            st.dataframe(solution_df)
        except FileNotFoundError:
            st.warning("Fichier solution introuvable.")


# ------------------------------------------------------------
# ÉCRAN DE FIN
# ------------------------------------------------------------

def render_end() -> None:
    score = st.session_state["score"]
    history = st.session_state["history"]
    total = score["correct"] + score["incorrect"]

    st.title("🎉 Session terminée !")
    st.divider()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total", total)
    col2.metric("✅ Corrects", score["correct"])
    col3.metric("❌ À revoir", score["incorrect"])

    errors = [(ex, r) for ex, r in history if r == "incorrect"]
    if errors:
        st.divider()
        st.subheader("Exercices à retravailler")
        for ex, _ in errors:
            st.markdown(f"- **{ex['theme']}** · `{ex['name']}`")

    st.divider()
    if st.button("🔄 Recommencer", type="primary"):
        for key in ["session_started", "session_finished", "queue", "score", "history"]:
            st.session_state.pop(key, None)
        st.rerun()


# ------------------------------------------------------------
# ROUTEUR
# ------------------------------------------------------------

if st.session_state.get("session_finished"):
    render_end()
elif st.session_state.get("session_started"):
    render_exercise()
else:
    render_home()

"""
db.py - Initialisation de la base de données et connexion partagée.

Ce module a deux responsabilités :
  1. Créer les tables de données des exercices (à lancer une seule fois).
  2. Exposer get_connection() pour partager une connexion DuckDB dans toute l'app.
"""

import io
import random
import numpy as np
import pandas as pd
import duckdb
import streamlit as st
from pathlib import Path

from config import DB_PATH


# ------------------------------------------------------------
# CONNEXION PARTAGÉE
# ------------------------------------------------------------

@st.cache_resource
def get_connection() -> duckdb.DuckDBPyConnection:
    """Retourne une connexion DuckDB partagée pour toute la session Streamlit."""
    return duckdb.connect(DB_PATH)


# ------------------------------------------------------------
# CRÉATION DES TABLES D'EXERCICES
# ------------------------------------------------------------

def create_cross_joins_exercises(con: duckdb.DuckDBPyConnection) -> None:
    beverages_df = pd.read_csv(io.StringIO("beverage,price\norange juice,2.5\nExpresso,2\nTea,3\n"))
    con.execute("CREATE TABLE IF NOT EXISTS beverages AS SELECT * FROM beverages_df")

    food_items_df = pd.read_csv(io.StringIO("food_item,food_price\ncookie,2.5\ncholatine,2\nmuffin,3\n"))
    con.execute("CREATE TABLE IF NOT EXISTS food_items AS SELECT * FROM food_items_df")

    sizes_df = pd.read_csv(io.StringIO("size\nXS\nM\nL\nXL\n"))
    con.execute("CREATE TABLE IF NOT EXISTS sizes AS SELECT * FROM sizes_df")

    trademarks_df = pd.read_csv(io.StringIO("trademark\nNike\nAsphalte\nAbercrombie\nLewis\n"))
    con.execute("CREATE TABLE IF NOT EXISTS trademarks AS SELECT * FROM trademarks_df")

    hours_df = pd.read_csv(io.StringIO("hour\n08\n09\n10\n11\n12\n"))
    con.execute("CREATE TABLE IF NOT EXISTS hours AS SELECT * FROM hours_df")

    quarters_df = pd.read_csv(io.StringIO("quarter\n00\n15\n30\n45\n"))
    con.execute("CREATE TABLE IF NOT EXISTS quarters AS SELECT * FROM quarters_df")


def create_inner_joins_exercises(con: duckdb.DuckDBPyConnection) -> None:
    salaries_df = pd.read_csv(io.StringIO("salary,employee_id\n2000,1\n2500,2\n2200,3\n"))
    con.execute("CREATE TABLE IF NOT EXISTS salaries AS SELECT * FROM salaries_df")

    seniorities_df = pd.read_csv(io.StringIO("employee_id,seniority\n1,2ans\n2,4ans\n"))
    con.execute("CREATE TABLE IF NOT EXISTS seniorities AS SELECT * FROM seniorities_df")


def create_left_joins_exercises(con: duckdb.DuckDBPyConnection) -> None:
    orders_df = pd.DataFrame({"order_id": [1, 2, 3, 4, 5], "customer_id": [101, 102, 103, 104, 105]})
    con.execute("CREATE TABLE IF NOT EXISTS orders AS SELECT * FROM orders_df")

    customers_df = pd.DataFrame({
        "customer_id": [101, 102, 103, 104, 105, 106],
        "customer_name": ["Toufik", "Daniel", "Tancrède", "Kaouter", "Jean-Nicolas", "David"],
    })
    con.execute("CREATE TABLE IF NOT EXISTS customers AS SELECT * FROM customers_df")

    products_df = pd.DataFrame({
        "product_id": [101, 103, 104, 105],
        "product_name": ["Laptop", "Ipad", "Livre", "Petitos"],
        "product_price": [800, 400, 30, 2],
    })
    con.execute("CREATE TABLE IF NOT EXISTS products AS SELECT * FROM products_df")

    order_details_df = pd.DataFrame({
        "order_id": [1, 2, 3, 4, 5],
        "product_id": [102, 104, 101, 103, 105],
        "quantity": [2, 1, 3, 2, 1],
    })
    con.execute("CREATE TABLE IF NOT EXISTS order_details AS SELECT * FROM order_details_df")


def create_full_outer_joins_exercises(con: duckdb.DuckDBPyConnection) -> None:
    customers_df = pd.DataFrame({
        "customer_id": [11, 12, 13, 14, 15],
        "customer_name": ["Zeinaba", "Tancrède", "Israel", "Kaouter", "Alan"],
    })
    con.execute("CREATE TABLE IF NOT EXISTS df_customers AS SELECT * FROM customers_df")

    stores_df = pd.DataFrame({"store_id": [1, 2, 3, 4], "customer_id": [11, 12, 13, 15]})
    con.execute("CREATE TABLE IF NOT EXISTS df_stores AS SELECT * FROM stores_df")

    store_products_df = pd.DataFrame({
        "store_id": [1, 1, 1, 2, 2, 3, 4],
        "product_id": [101, 103, 105, 101, 103, 104, 105],
    })
    con.execute("CREATE TABLE IF NOT EXISTS df_store_products AS SELECT * FROM store_products_df")

    products_df = pd.DataFrame({
        "product_id": [100, 101, 103, 104],
        "product_name": ["Cherry coke", "Laptop", "Ipad", "Livre"],
        "product_price": [3, 800, 400, 30],
    })
    con.execute("CREATE TABLE IF NOT EXISTS df_products AS SELECT * FROM products_df")


def create_self_joins_exercises(con: duckdb.DuckDBPyConnection) -> None:
    employees_df = pd.DataFrame({
        "employee_id": [11, 12, 13, 14, 15],
        "employee_name": ["Sophie", "Sylvie", "Daniel", "Kaouter", "David"],
        "manager_id": [13, None, 12, 13, 11],
    })
    con.execute("CREATE TABLE IF NOT EXISTS employees AS SELECT * FROM employees_df")

    sales_df = pd.DataFrame({
        "order_id": list(range(1110, 1198)),
        "customer_id": random.choices([11, 12, 13, 14, 15, 11, 12, 13, 14], k=88),
    })
    sales_df["date"] = [d // 3 + 1 for d in range(1, 89)]
    con.execute("CREATE TABLE IF NOT EXISTS sales AS SELECT * FROM sales_df")


def create_group_by_exercises(con: duckdb.DuckDBPyConnection) -> None:
    ventes_immo_df = pd.DataFrame([
        [0, "vieux_lille", 460000], [1, "vieux_lille", 430000], [2, "vieux_lille", 450000],
        [3, float("nan"), 470000],  [4, "vieux_lille", 440000], [10, "gambetta", 336000],
        [11, float("nan"), 333000], [12, "gambetta", 335000],   [13, "gambetta", 337000],
        [14, "gambetta", 334000],   [20, "centre", 356000],     [21, "centre", 353000],
        [22, float("nan"), 355000], [23, "centre", 357000],     [24, "centre", 354000],
        [30, "wazemmes", 260000],   [31, float("nan"), 230000], [32, "wazemmes", 250000],
        [33, "wazemmes", 270000],   [34, "wazemmes", 240000],
    ], columns=["flat_id", "neighborhood", "price"])
    con.execute("CREATE TABLE IF NOT EXISTS ventes_immo AS SELECT * FROM ventes_immo_df")

    clients = ["Oussama", "Julie", "Chris", "Tom", "Jean-Nicolas",
               "Aline", "Ben", "Toufik", "Sylvie", "David"]
    ventes_df = pd.DataFrame(
        [110, 49, 65, 23, 24, 3.99, 29, 48.77, 44, 10, 60, 12, 62, 19, 75] * 2,
        columns=["montant"]
    )
    ventes_df["client"] = clients * 3
    con.execute("CREATE TABLE IF NOT EXISTS ventes AS SELECT * FROM ventes_df")


def create_case_when_exercises(con: duckdb.DuckDBPyConnection) -> None:
    salaires_df = pd.DataFrame({
        "name": ["Toufik", "Jean-Nicolas", "Daniel", "Kaouter", "Sylvie", "Sebastien",
                 "Diane", "Romain", "François", "Anna", "Zeinaba", "Gregory",
                 "Karima", "Arthur", "Benjamin"],
        "wage": [60000, 75000, 55000, 80000, 70000, 90000, 65000, 72000, 68000,
                 85000, 100000, 120000, 95000, 83000, 110000],
        "department": ["IT", "HR", "SALES", "IT", "IT", "HR", "SALES", "IT", "HR",
                       "SALES", "IT", "IT", "HR", "SALES", "CEO"],
    })
    con.execute("CREATE TABLE IF NOT EXISTS salaires AS SELECT * FROM salaires_df")

    discount_df = pd.DataFrame({
        "order_id": [1, 2, 3, 4, 5, 6],
        "product_id": [101, 102, 101, 103, 102, 103],
        "quantity": [5, 3, 2, 4, 6, 2],
        "price_per_unit": [10.0, 25.0, 10.0, 8.0, 25.0, 8.0],
        "discount_code": [None, "DISCOUNT10", "DISCOUNT20", None, None, "UNKNOWN"],
    })
    con.execute("CREATE TABLE IF NOT EXISTS discount AS SELECT * FROM discount_df")


def create_grouping_set_exercises(con: duckdb.DuckDBPyConnection) -> None:
    redbull_df = pd.DataFrame({
        "store_id": ["Armentieres"] * 4 + ["Lille"] * 4 + ["Douai"] * 4,
        "product_name": ["redbull", "chips", "wine", "redbull", "redbull", "chips",
                         "wine", "icecream", "redbull", "chips", "wine", "icecream"],
        "amount": [45, 60, 60, 45, 100, 140, 190, 170, 55, 70, 20, 45],
    })
    con.execute("CREATE TABLE IF NOT EXISTS redbull AS SELECT * FROM redbull_df")

    datapop_df = pd.DataFrame({
        "year": [2016, 2017, 2018, 2019, 2020] * 3,
        "region": ["IDF"] * 5 + ["HDF"] * 5 + ["PACA"] * 5,
        "population": [1010000, 1020000, 1030000, 1040000, 1000000,
                       910000, 920000, 930000, 940000, 900000,
                       810000, 820000, 830000, 840000, 950000],
    })
    con.execute("CREATE TABLE IF NOT EXISTS datapop AS SELECT * FROM datapop_df")


# ------------------------------------------------------------
# POINT D'ENTRÉE
# ------------------------------------------------------------

def init_db() -> None:
    """Crée toutes les tables si elles n'existent pas encore."""

    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(DB_PATH)
    create_cross_joins_exercises(con)
    create_inner_joins_exercises(con)
    create_left_joins_exercises(con)
    create_full_outer_joins_exercises(con)
    create_self_joins_exercises(con)
    create_group_by_exercises(con)
    create_case_when_exercises(con)
    create_grouping_set_exercises(con)
    con.close()


if __name__ == "__main__":
    init_db()
    print("Base de données initialisée.")
    con = duckdb.connect(DB_PATH)

    with con:
        tables = con.execute("SHOW TABLES").fetchall()
        print("Tables créées :", tables)

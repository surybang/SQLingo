"""
Ce module contient les fonctions permettant d'initialiser la base de données de l'application.
"""

import io
import random
import numpy as np
import pandas as pd
import duckdb


def create_memory_state_table(con):
    """
    Créer la table vide des exercices
    """
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS memory_state (
            user_id TEXT,
            theme TEXT,
            exercise_name TEXT,
            tables TEXT[],
            last_reviewed DATE,
            answer TEXT,
            PRIMARY KEY (user_id, exercise_name)
        )
    """
    )


def create_cross_joins_exercises(con):
    beverages_csv = "beverage,price\norange juice,2.5\nExpresso,2\nTea,3\n"
    beverages_df = pd.read_csv(io.StringIO(beverages_csv))
    con.execute("CREATE TABLE IF NOT EXISTS beverages AS SELECT * FROM beverages_df")

    food_items_csv = "food_item,food_price\ncookie juice,2.5\nchocolatine,2\nmuffin,3\n"
    food_items_df = pd.read_csv(io.StringIO(food_items_csv))
    con.execute("CREATE TABLE IF NOT EXISTS food_items AS SELECT * FROM food_items_df")

    sizes_csv = "size\nXS\nM\nL\nXL\n"
    sizes_df = pd.read_csv(io.StringIO(sizes_csv))
    con.execute("CREATE TABLE IF NOT EXISTS sizes AS SELECT * FROM sizes_df")

    trademarks_csv = "trademark\nNike\nAsphalte\nAbercrombie\nLewis\n"
    trademarks_df = pd.read_csv(io.StringIO(trademarks_csv))
    con.execute("CREATE TABLE IF NOT EXISTS trademarks AS SELECT * FROM trademarks_df")

    hours_csv = "hour\n08\n09\n10\n11\n12\n"
    hours_df = pd.read_csv(io.StringIO(hours_csv))
    con.execute("CREATE TABLE IF NOT EXISTS hours AS SELECT * FROM hours_df")

    quarters_csv = "quarter\n00\n15\n30\n45\n"
    quarters_df = pd.read_csv(io.StringIO(quarters_csv))
    con.execute("CREATE TABLE IF NOT EXISTS quarters AS SELECT * FROM quarters_df")


def create_inner_joins_exercises(con):
    salaries_csv = "salary,employee_id\n2000,1\n2500,2\n2200,3\n"
    salaries_df = pd.read_csv(io.StringIO(salaries_csv))
    con.execute("CREATE TABLE IF NOT EXISTS salaries AS SELECT * FROM salaries_df")

    seniorities_csv = "employee_id,seniority\n1,2ans\n2,4ans\n"
    seniorities_df = pd.read_csv(io.StringIO(seniorities_csv))
    con.execute(
        "CREATE TABLE IF NOT EXISTS seniorities AS SELECT * FROM seniorities_df"
    )


def create_left_joins_exercises(con):
    orders_data = {
        "order_id": [1, 2, 3, 4, 5],
        "customer_id": [101, 102, 103, 104, 105],
    }
    df_orders = pd.DataFrame(orders_data)
    con.execute("CREATE TABLE IF NOT EXISTS orders AS SELECT * FROM df_orders")

    customers_data = {
        "customer_id": [101, 102, 103, 104, 105, 106],
        "customer_name": [
            "Toufik",
            "Daniel",
            "Tancrède",
            "Kaouter",
            "Jean-Nicolas",
            "David",
        ],
    }
    df_customers = pd.DataFrame(customers_data)
    con.execute("CREATE TABLE IF NOT EXISTS customers AS SELECT * FROM df_customers")

    products_data = {
        "product_id": [101, 103, 104, 105],
        "product_name": ["Laptop", "Ipad", "Livre", "Petitos"],
        "product_price": [800, 400, 30, 2],
    }
    df_products = pd.DataFrame(products_data)
    con.execute("CREATE TABLE IF NOT EXISTS products AS SELECT * FROM df_products")

    order_details_data = {
        "order_id": [1, 2, 3, 4, 5],
        "product_id": [102, 104, 101, 103, 105],
        "quantity": [2, 1, 3, 2, 1],
    }
    df_order_details = pd.DataFrame(order_details_data)
    con.execute(
        "CREATE TABLE IF NOT EXISTS order_details AS SELECT * FROM df_order_details"
    )


def create_full_outer_joins_exercises(con):
    customers_data = {
        "customer_id": [11, 12, 13, 14, 15],
        "customer_name": ["Zeinaba", "Tancrède", "Israel", "Kaouter", "Alan"],
    }
    customers_df = pd.DataFrame(customers_data)
    con.execute("CREATE TABLE IF NOT EXISTS df_customers AS SELECT * FROM customers_df")

    stores_data = {"store_id": [1, 2, 3, 4], "customer_id": [11, 12, 13, 15]}
    stores_df = pd.DataFrame(stores_data)
    con.execute("CREATE TABLE IF NOT EXISTS df_stores AS SELECT * FROM stores_df")

    store_products_data = {
        "store_id": [1, 1, 1, 2, 2, 3, 4],
        "product_id": [101, 103, 105, 101, 103, 104, 105],
    }
    store_products_df = pd.DataFrame(store_products_data)
    con.execute(
        "CREATE TABLE IF NOT EXISTS df_store_products AS SELECT * FROM store_products_df"
    )

    products_data = {
        "product_id": [100, 101, 103, 104],
        "product_name": ["Cherry coke", "Laptop", "Ipad", "Livre"],
        "product_price": [3, 800, 400, 30],
    }
    products_df = pd.DataFrame(products_data)
    con.execute("CREATE TABLE IF NOT EXISTS df_products AS SELECT * FROM products_df")


def create_self_joins_exercises(con):
    employees_data = {
        "employee_id": [11, 12, 13, 14, 15],
        "employee_name": ["Sophie", "Sylvie", "Daniel", "Kaouter", "David"],
        "manager_id": [13, None, 12, 13, 11],
    }
    employees_df = pd.DataFrame(employees_data)
    con.execute("CREATE TABLE IF NOT EXISTS employees AS SELECT * FROM employees_df")

    sales_data = {
        "order_id": list(range(1110, 1198)),
        "customer_id": random.choices([11, 12, 13, 14, 15, 11, 12, 13, 14], k=88),
    }
    sales_df = pd.DataFrame(sales_data)
    sales_df["date"] = [d // 3 + 1 for d in range(1, 89)]
    con.execute("CREATE TABLE IF NOT EXISTS sales AS SELECT * FROM sales_df")


def create_group_by_exercises(con):
    ventes_immo_data = [
        [0, "vieux_lille", 460000],
        [1, "vieux_lille", 430000],
        [2, "vieux_lille", 450000],
        [3, np.NaN, 470000],
        [4, "vieux_lille", 440000],
        [10, "gambetta", 336000],
        [11, np.NaN, 333000],
        [12, "gambetta", 335000],
        [13, "gambetta", 337000],
        [14, "gambetta", 334000],
        [20, "centre", 356000],
        [21, "centre", 353000],
        [22, np.NaN, 355000],
        [23, "centre", 357000],
        [24, "centre", 354000],
        [30, "wazemmes", 260000],
        [31, np.NaN, 230000],
        [32, "wazemmes", 250000],
        [33, "wazemmes", 270000],
        [34, "wazemmes", 240000],
    ]
    ventes_immo_df = pd.DataFrame(
        ventes_immo_data, columns=["flat_id", "neighborhood", "price"]
    )
    con.execute(
        "CREATE TABLE IF NOT EXISTS ventes_immo AS SELECT * FROM ventes_immo_df"
    )

    clients = [
        "Oussama",
        "Julie",
        "Chris",
        "Tom",
        "Jean-Nicolas",
        "Aline",
        "Ben",
        "Toufik",
        "Sylvie",
        "David",
    ]
    ventes_data = [110, 49, 65, 23, 24, 3.99, 29, 48.77, 44, 10, 60, 12, 62, 19, 75] * 2
    ventes_df = pd.DataFrame(ventes_data, columns=["montant"])
    ventes_df["client"] = clients * 3
    con.execute("CREATE TABLE IF NOT EXISTS ventes AS SELECT * FROM ventes_df")


def create_case_when_exercises(con):
    salaires_data = {
        "name": [
            "Toufik",
            "Jean-Nicolas",
            "Daniel",
            "Kaouter",
            "Sylvie",
            "Sebastien",
            "Diane",
            "Romain",
            "François",
            "Anna",
            "Zeinaba",
            "Gregory",
            "Karima",
            "Arthur",
            "Benjamin",
        ],
        "wage": [
            60000,
            75000,
            55000,
            80000,
            70000,
            90000,
            65000,
            72000,
            68000,
            85000,
            100000,
            120000,
            95000,
            83000,
            110000,
        ],
        "department": [
            "IT",
            "HR",
            "SALES",
            "IT",
            "IT",
            "HR",
            "SALES",
            "IT",
            "HR",
            "SALES",
            "IT",
            "IT",
            "HR",
            "SALES",
            "CEO",
        ],
    }
    salaires_df = pd.DataFrame(salaires_data)
    con.execute("CREATE TABLE IF NOT EXISTS salaires AS SELECT * FROM salaires_df")

    discount_data = {
        "order_id": [1, 2, 3, 4, 5, 6],
        "product_id": [101, 102, 101, 103, 102, 103],
        "quantity": [5, 3, 2, 4, 6, 2],
        "price_per_unit": [10.0, 25.0, 10.0, 8.0, 25.0, 8.0],
        "discount_code": [None, "DISCOUNT10", "DISCOUNT20", None, None, "UNKNOWN"],
    }
    discount_df = pd.DataFrame(discount_data)
    con.execute("CREATE TABLE IF NOT EXISTS discount AS SELECT * FROM discount_df")


def create_grouping_set_exercises(con):
    redbull_data = {
        "store_id": ["Armentieres"] * 4 + ["Lille"] * 4 + ["Douai"] * 4,
        "product_name": [
            "redbull",
            "chips",
            "wine",
            "redbull",
            "redbull",
            "chips",
            "wine",
            "icecream",
            "redbull",
            "chips",
            "wine",
            "icecream",
        ],
        "amount": [45, 60, 60, 45, 100, 140, 190, 170, 55, 70, 20, 45],
    }
    redbull_df = pd.DataFrame(redbull_data)
    con.execute("CREATE TABLE IF NOT EXISTS redbull AS SELECT * FROM redbull_df")

    datapop_data = {
        "year": [2016, 2017, 2018, 2019, 2020] * 3,
        "region": ["IDF"] * 5 + ["HDF"] * 5 + ["PACA"] * 5,
        "population": [
            1010000,
            1020000,
            1030000,
            1040000,
            1000000,
            910000,
            920000,
            930000,
            940000,
            900000,
            810000,
            820000,
            830000,
            840000,
            950000,
        ],
    }
    datapop_df = pd.DataFrame(datapop_data)
    con.execute("CREATE TABLE IF NOT EXISTS datapop AS SELECT * FROM datapop_df")


def create_users_table(con):
    con.execute("CREATE SEQUENCE IF NOT EXISTS user_id_seq")
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INT DEFAULT nextval('user_id_seq') PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """
    )


def main():
    con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

    create_memory_state_table(con)
    create_cross_joins_exercises(con)
    create_inner_joins_exercises(con)
    create_left_joins_exercises(con)
    create_full_outer_joins_exercises(con)
    create_self_joins_exercises(con)
    create_group_by_exercises(con)
    create_case_when_exercises(con)
    create_grouping_set_exercises(con)
    create_users_table(con)

    con.close()


if __name__ == "__main__":
    main()

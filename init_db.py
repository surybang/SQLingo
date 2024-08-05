import io

import random
import numpy as np
import pandas as pd
import duckdb

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

# ------------------------------------------------------------
# EXERCISES LIST
# ------------------------------------------------------------

data = {
    "theme": [
        "cross_joins",
        "cross_joins",
        "cross_joins",
        "inner_joins",
        "left_joins",
        "left_joins",
        "left_joins",
        "full_outer_joins",
        "self_joins",
        "self_joins",
        "group_by",
        "group_by",
        "group_by",
        "case_when",
        "case_when",
        "case_when",
        "case_when",
        "grouping_set",
        "grouping_set",
        "grouping_set",
        "grouping_set",
        "grouping_set",
        "grouping_set",
    ],
    "exercise_name": [
        "cross_joins_1",
        "cross_joins_2",
        "cross_joins_3",
        "inner_joins_1",
        "left_joins_1",
        "left_joins_2",
        "left_joins_3",
        "full_outer_joins_1",
        "self_joins_1",
        "self_joins_2",
        "group_by_1",
        "group_by_2",
        "group_by_3",
        "case_when_1",
        "case_when_2",
        "case_when_3",
        "case_when_4",
        "grouping_set_1",
        "grouping_set_2",
        "grouping_set_3",
        "grouping_set_4",
        "grouping_set_5",
        "grouping_set_6",
    ],
    "tables": [
        ["beverages", "food_items"],
        ["sizes", "trademarks"],
        ["hours", "quarters"],
        ["salaries", "seniorities"],
        ["orders", "customers", "products", "order_details"],
        ["orders", "customers", "products", "order_details"],
        ["orders", "customers", "products", "order_details"],
        ["df_customers", "df_stores", "df_store_products", "df_products"],
        ["employees"],
        ["sales"],
        ["ventes_immo"],
        ["ventes"],
        ["ventes"],
        ["orders_df"],
        ["salaires"],
        ["discount"],
        ["salaires"],
        ["redbull"],
        ["datapop"],
        ["redbull"],
        ["redbull"],
        ["sante"],
        ["sante"],
    ],
    "last_reviewed": [
        "1970-01-01",
        "1970-01-01",
        "1970-01-01",
        "1970-01-01",
        "1970-01-01",
        "1970-01-01",
        "1970-01-01",
        "1970-01-01",
        "1970-01-01",
        "1970-01-01",
        "1970-01-01",
        "1970-01-01",
        "1970-01-01",
        "1970-01-01",
        "1970-01-01",
        "1970-01-01",
        "1970-01-01",
        "1970-01-01",
        "1970-01-01",
        "1970-01-01",
        "1970-01-01",
        "1970-01-01",
        "1970-01-01",
    ],
    "answer": [
        "cross_joins_1.sql",
        "cross_joins_2.sql",
        "cross_joins_3.sql",
        "inner_joins_1.sql",
        "left_joins_1.sql",
        "left_joins_2.sql",
        "left_joins_3.sql",
        "full_outer_joins_1.sql",
        "self_joins_1.sql",
        "self_joins_2.sql",
        "group_by_1.sql",
        "group_by_2.sql",
        "group_by_3.sql",
        "case_when_1.sql",
        "case_when_2.sql",
        "case_when_3.sql",
        "case_when_4.sql",
        "grouping_set_1.sql",
        "grouping_set_2.sql",
        "grouping_set_3.sql",
        "grouping_set_4.sql",
        "grouping_set_5.sql",
        "grouping_set_6.sql",
    ],
}
memory_state_df: pd.DataFrame = pd.DataFrame(data)
con.execute("CREATE TABLE IF NOT EXISTS memory_state AS SELECT * FROM memory_state_df")


# ------------------------------------------------------------
# CROSS JOIN EXERCISES
# ------------------------------------------------------------
csv = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""
beverages: pd.DataFrame = pd.read_csv(io.StringIO(csv))
con.execute("CREATE TABLE IF NOT EXISTS beverages AS SELECT * FROM beverages")

csv2 = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""
food_items: pd.DataFrame = pd.read_csv(io.StringIO(csv2))
con.execute("CREATE TABLE IF NOT EXISTS food_items AS SELECT * FROM food_items")


sizes = """
size
XS
M
L
XL
"""
sizes: pd.DataFrame = pd.read_csv(io.StringIO(sizes))
con.execute("CREATE TABLE IF NOT EXISTS sizes AS SELECT * FROM sizes")

trademarks = """
trademark
Nike
Asphalte
Abercrombie
Lewis
"""
trademarks: pd.DataFrame = pd.read_csv(io.StringIO(trademarks))
con.execute("CREATE TABLE IF NOT EXISTS trademarks AS SELECT * FROM trademarks")


hours = """
hour
08
09
10
11
12
"""
hours: pd.DataFrame = pd.read_csv(io.StringIO(hours))
con.execute("CREATE TABLE IF NOT EXISTS hours AS SELECT * FROM hours")


quarters = """
quarter
00
15
30
45
"""
quarters: pd.DataFrame = pd.read_csv(io.StringIO(quarters))
con.execute("CREATE TABLE IF NOT EXISTS quarters AS SELECT * FROM quarters")

# ------------------------------------------------------------
# INNER JOIN EXERCISES
# ------------------------------------------------------------
salaries = """
salary,employee_id
2000,1
2500,2
2200,3
"""
salaries: pd.DataFrame = pd.read_csv(io.StringIO(salaries))
con.execute("CREATE TABLE IF NOT EXISTS salaries AS SELECT * FROM salaries")

seniorities = """
employee_id,seniority
1,2ans
2,4ans
"""
seniorities: pd.DataFrame = pd.read_csv(io.StringIO(seniorities))
con.execute("CREATE TABLE IF NOT EXISTS seniorities AS SELECT * FROM seniorities")


# ------------------------------------------------------------
# LEFT JOIN EXERCISES
# ------------------------------------------------------------
orders_data = {"order_id": [1, 2, 3, 4, 5], "customer_id": [101, 102, 103, 104, 105]}
df_orders: pd.DataFrame = pd.DataFrame(orders_data)
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
df_customers: pd.DataFrame = pd.DataFrame(customers_data)
con.execute("CREATE TABLE IF NOT EXISTS customers AS SELECT * FROM df_customers")

products_data = {
    "product_id": [101, 103, 104, 105],
    "product_name": ["Laptop", "Ipad", "Livre", "Petitos"],
    "product_price": [800, 400, 30, 2],
}
df_products: pd.DataFrame = pd.DataFrame(products_data)
con.execute("CREATE TABLE IF NOT EXISTS products AS SELECT * FROM df_products")

order_details_data = {
    "order_id": [1, 2, 3, 4, 5],
    "product_id": [102, 104, 101, 103, 105],
    "quantity": [2, 1, 3, 2, 1],
}
df_order_details: pd.DataFrame = pd.DataFrame(order_details_data)
con.execute(
    "CREATE TABLE IF NOT EXISTS order_details AS SELECT * FROM df_order_details"
)


# ------------------------------------------------------------
# FULL OUTER JOIN EXERCISES
# ------------------------------------------------------------
customers_data = {
    "customer_id": [11, 12, 13, 14, 15],
    "customer_name": ["Zeinaba", "Tancrède", "Israel", "Kaouter", "Alan"],
}
customers_data: pd.DataFrame = pd.DataFrame(customers_data)
con.execute("CREATE TABLE IF NOT EXISTS df_customers AS SELECT * FROM customers_data")

stores_data = {"store_id": [1, 2, 3, 4], "customer_id": [11, 12, 13, 15]}
stores_data: pd.DataFrame = pd.DataFrame(stores_data)
con.execute("CREATE TABLE IF NOT EXISTS df_stores AS SELECT * FROM stores_data")

store_products_data = {
    "store_id": [1, 1, 1, 2, 2, 3, 4],
    "product_id": [101, 103, 105, 101, 103, 104, 105],
}
store_products_data: pd.DataFrame = pd.DataFrame(store_products_data)
con.execute(
    "CREATE TABLE IF NOT EXISTS df_store_products AS SELECT * FROM store_products_data"
)

p_names = [
    "Cherry coke",
    "Laptop",
    "Ipad",
    "Livre",
]
products_data = {
    "product_id": [100, 101, 103, 104],
    "product_name": p_names,
    "product_price": [3, 800, 400, 30],
}
products_data: pd.DataFrame = pd.DataFrame(products_data)
con.execute("CREATE TABLE IF NOT EXISTS df_products AS SELECT * FROM products_data")

# ------------------------------------------------------------
# SELF JOIN EXERCISES
# ------------------------------------------------------------
employees = {
    "employee_id": [11, 12, 13, 14, 15],
    "employee_name": ["Sophie", "Sylvie", "Daniel", "Kaouter", "David"],
    "manager_id": [13, None, 12, 13, 11],
}
employees: pd.DataFrame = pd.DataFrame(employees)
con.execute("CREATE TABLE IF NOT EXISTS employees AS SELECT * FROM employees")


sales = {
    "order_id": list(range(1110, 1198)),
    "customer_id": random.choices([11, 12, 13, 14, 15, 11, 12, 13, 14], k=88),
}

sales: pd.DataFrame = pd.DataFrame(sales)
sales["date"] = [d // 3 + 1 for d in range(1, 89)]
con.execute("CREATE TABLE IF NOT EXISTS sales AS SELECT * FROM sales")

# ------------------------------------------------------------
# GROUP BY EXERCISES
# ------------------------------------------------------------
dates = [f"2023-08-{str(x).zfill(2)}" for x in range(7, 21)]
ventes_immo_df: pd.DataFrame = pd.DataFrame(
    [
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
)

ventes_immo_df.columns = ["flat_id", "neighborhood", "price"]
con.execute("CREATE TABLE IF NOT EXISTS ventes_immo AS SELECT * FROM ventes_immo_df")


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
ventes_df = [110, 49, 65, 23, 24, 3.99, 29, 48.77, 44, 10, 60, 12, 62, 19, 75] * 2
ventes_df = pd.DataFrame(ventes_df)
ventes_df.columns = ["montant"]
ventes_df["client"] = clients * 3

con.execute("CREATE TABLE IF NOT EXISTS ventes AS SELECT * FROM ventes_df")


# ------------------------------------------------------------
# CASE WHEN EXERCISES
# ------------------------------------------------------------
orders_df = {
    "order_id": [1, 2, 3, 4, 5],
    "order_date": [
        "2023-01-15",
        "2023-02-20",
        "2023-03-05",
        "2023-04-10",
        "2023-05-18",
    ],
    "order_amount": [120, 450, 800, 60, 1500],
}
orders_df: pd.DataFrame = pd.DataFrame(orders_df)

con.execute("CREATE TABLE IF NOT EXISTS orders_df AS SELECT * FROM orders_df")


salaires_df = {
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

salaires_df: pd.DataFrame = pd.DataFrame(salaires_df)
con.execute("CREATE TABLE IF NOT EXISTS salaires AS SELECT * FROM salaires_df")


discount_df = {
    "order_id": [1, 2, 3, 4, 5, 6],
    "product_id": [101, 102, 101, 103, 102, 103],
    "quantity": [5, 3, 2, 4, 6, 2],
    "price_per_unit": [10.0, 25.0, 10.0, 8.0, 25.0, 8.0],
    "discount_code": [None, "DISCOUNT10", "DISCOUNT20", None, None, "UNKNOWN"],
}

discount_df: pd.DataFrame = pd.DataFrame(discount_df)
con.execute("CREATE TABLE IF NOT EXISTS discount AS SELECT * FROM discount_df")


# ------------------------------------------------------------
# GROUPING SETS EXERCISES
# ------------------------------------------------------------
redbull_df = {
    "store_id": [
        "Armentieres",
        "Armentieres",
        "Armentieres",
        "Armentieres",
        "Lille",
        "Lille",
        "Lille",
        "Lille",
        "Douai",
        "Douai",
        "Douai",
        "Douai",
    ],
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
redbull_df: pd.DataFrame = pd.DataFrame(redbull_df)
con.execute("CREATE TABLE IF NOT EXISTS redbull AS SELECT * FROM redbull_df")


df_pop = {
    "year": [2016, 2017, 2018, 2019, 2020] * 3,
    "region": (["IDF"] * 5) + (["HDF"] * 5) + (["PACA"] * 5),
    "population": [1010000, 1020000, 1030000, 1040000, 1000000]
    + [910000, 920000, 930000, 940000, 900000]
    + [810000, 820000, 830000, 840000, 950000],
}
df_pop: pd.DataFrame = pd.DataFrame(df_pop)
con.execute("CREATE TABLE IF NOT EXISTS datapop AS SELECT * FROM df_pop")


random.seed(42)
num_samples = 1000

contrats = ["senior", "jeunes", "expat", "famille", "salarié"]
sexe = ["homme", "femme"]
type_acte = {
    "pharmacie": 15,
    "consultation_generaliste": 25,
    "hospitalisation": 2800,
    "biologie": 150,
    "radio": 1300,
    "maternite": 1700,
}
groupe_age = ["18-25", "25-45", "45-65", "65+"]
annee = [2017, 2018, 2019]

# Initialize empty lists to store the data
contrats_data = []
sexe_data = []
type_acte_data = []
groupe_age_data = []
annee_data = []
cost_data = []

# Generate random data for each category
for _ in range(num_samples):
    contrats_data.append(random.choice(contrats))
    sexe_data.append(random.choice(sexe))
    if sexe_data == "femme":
        type_acte_choice = random.choice(list(type_acte.keys()))
    else:
        type_acte_options = list(type_acte.keys())
        type_acte_options.remove("maternite")
        type_acte_choice = random.choice(type_acte_options)

    type_acte_data.append(type_acte_choice)
    cost_mean = type_acte[type_acte_choice]
    cost_data.append(
        np.random.normal(cost_mean, cost_mean // 3.5)
    )  # Assuming a standard deviation of 50 for costs
    groupe_age_data.append(random.choice(groupe_age))
    annee_data.append(random.choice(annee))

# Create a DataFrame to store the dataset
sante_df: pd.DataFrame = pd.DataFrame(
    {
        "type_contrat": contrats_data,
        "sexe": sexe_data,
        "type_acte": type_acte_data,
        "groupe_age": groupe_age_data,
        "annee": annee_data,
        "montant_rembourse": cost_data,
    }
)
con.execute("CREATE TABLE IF NOT EXISTS sante AS SELECT * FROM sante_df")


con.close()


# black init_db.py
# python init_db.py


# if __name__ == "__main__":
#     print(memory_state_df)
# #    #con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)
# #    #print(con.execute("SELECT * FROM orders").df())
# #    #con.close()

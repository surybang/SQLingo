.PHONY: install init run start reset
 
install:
	uv sync
 
init:
	uv run db.py
 
run:
	uv run streamlit run app.py
 
start: install init run
 
reset:
	rm -f data/exercises_sql_tables.duckdb
	uv run db.py
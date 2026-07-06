from pathlib import Path
import duckdb
import pandas as pd

project_root = Path(__file__).resolve().parents[2]
db_path = project_root / "database" / "books.duckdb"

con = duckdb.connect(str(db_path))

def create_table(table_name: str, csv_path: Path):
    '''
    NOTES: 
    1. duckDB has a strict csv parser so its better to use pandas( which is
    more forgiving) to first read the csv as dataframe before registering
    in duckDB.
    2. in deployment, it is usually good to drop table first to get the
    latest version of source data.
    '''

    df = pd.read_csv(
        csv_path,
        sep=";",
        encoding="latin-1",
        low_memory=False,
        on_bad_lines="skip"
    )

    con.register("temp_df", df)

    con.execute(f"""
        DROP TABLE IF EXISTS {table_name};

        CREATE TABLE {table_name} AS
        SELECT *
        FROM temp_df;
    """)

    con.unregister("temp_df")

def main():
    print("Loading tables into DuckDB...")
    create_table("books", project_root / "data/raw/BX-Books.csv")
    create_table("users", project_root / "data/raw/BX-Users.csv")
    create_table("ratings", project_root / "data/raw/BX-Book-Ratings.csv")

    con.sql("SHOW TABLES").show()

if __name__ == "__main__":
    main()
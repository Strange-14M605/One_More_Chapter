from pathlib import Path
import duckdb

project_root = Path(__file__).resolve().parents[2]
db_path = project_root / "database" / "books.duckdb"

con = duckdb.connect(str(db_path))

def preprocess_books():
    """
    Cleaned books table:
    1. remove image URL columns
    2. missing author and publisher names logged as 'Unknown'

    To do: remove/fix weird Year_Of_Publication values
    """

    con.execute("""
        DROP TABLE IF EXISTS books_clean;

        CREATE TABLE books_clean AS
        SELECT
            ISBN,
            "Book-Title",
            COALESCE("Book-Author", 'Unknown') AS Book_Author,
            "Year-Of-Publication",
            COALESCE("Publisher", 'Unknown') AS Publishers
        FROM books;
    """)

    # print(con.sql("SELECT * FROM books LIMIT 1").fetchdf())
    # print(con.sql("SELECT * FROM books_clean LIMIT 1").fetchdf())

    raw = con.sql("SELECT COUNT(*) FROM books").fetchone()[0]
    clean = con.sql("SELECT COUNT(*) FROM books_clean").fetchone()[0]

    print(f"Books   : {raw:,} → {clean:,}")

def preprocess_users():
    """
    Cleaned users table:
    1. missing locations logged as 'Unknown'
    2. only country taken in location feature
    3. age is between 5 and 100 
    """

    con.execute("""
        DROP TABLE IF EXISTS users_clean;

        CREATE TABLE users_clean AS
        SELECT DISTINCT
            "User-ID" AS User_ID,
            CASE
                WHEN Location IS NULL THEN 'Unknown'
                ELSE TRIM(list_extract(string_split(Location, ','), -1))
            END AS Country,
            Age
        FROM users
        WHERE Age BETWEEN 5 AND 100;
    """)

    raw = con.sql("SELECT COUNT(*) FROM users").fetchone()[0]
    clean = con.sql("SELECT COUNT(*) FROM users_clean").fetchone()[0]

    print(f"Users   : {raw:,} → {clean:,}")



def preprocess_ratings():
    """
    Cleaned ratings table:
    1. only keep ratings > 0 (i.e. remove implicit ratings)

    To do: 
    """

    con.execute("""
        DROP TABLE IF EXISTS ratings_clean;

        CREATE TABLE ratings_clean AS
        SELECT DISTINCT
            "User-ID" AS User_ID,
            ISBN,
            "Book-Rating" AS Book_Rating
        FROM ratings
        WHERE Book_Rating > 0;
    """)

    raw = con.sql("SELECT COUNT(*) FROM ratings").fetchone()[0]
    clean = con.sql("SELECT COUNT(*) FROM ratings_clean").fetchone()[0]

    print(f"Ratings : {raw:,} → {clean:,}")

def export_parquet(table_name):
    output = project_root / "data" / "processed" / f"{table_name}.parquet"

    con.execute(f"""
        COPY {table_name}
        TO '{output}'
        (FORMAT PARQUET);
    """)

    print(f"Exported {table_name} → {output.name}")


def main():
    preprocess_books()
    preprocess_users()
    preprocess_ratings()

    export_parquet("books_clean")
    export_parquet("users_clean")
    export_parquet("ratings_clean")

    print("✅ Preprocessing complete.")

if __name__ == "__main__":
    main()
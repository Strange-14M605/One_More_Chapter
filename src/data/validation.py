from datetime import datetime
from pathlib import Path

import duckdb
import great_expectations as gx


def run_validation():
    """Validate the cleaned DuckDB tables using Great Expectations."""
    project_root = Path(__file__).resolve().parents[2]
    db_path = project_root / "database" / "books.duckdb"

    con = duckdb.connect(str(db_path))

    table_queries = {
        "books_clean": """
            SELECT
                ISBN AS isbn,
                "Book-Title" AS book_title,
                TRY_CAST("Year-Of-Publication" AS INTEGER) AS year_of_publication
            FROM books_clean
        """,
        "users_clean": """
            SELECT
                "User_ID" AS user_id,
                Age AS age
            FROM users_clean
        """,
        "ratings_clean": """
            SELECT
                "User_ID" AS user_id,
                ISBN AS isbn,
                "Book_Rating" AS book_rating
            FROM ratings_clean
        """,
    }

    all_tables_passed = True

    context = gx.get_context()

    for table_name, query in table_queries.items():
        df = con.execute(query).fetchdf()
        validator = context.sources.pandas_default.read_dataframe(df)

        if table_name == "books_clean":
            expectations = [
                validator.expect_column_values_to_not_be_null("isbn"),
                validator.expect_column_values_to_be_unique("isbn"),
                validator.expect_column_values_to_not_be_null("book_title"),
            ]
        elif table_name == "users_clean":
            expectations = [
                validator.expect_column_values_to_not_be_null("user_id"),
                validator.expect_column_values_to_be_unique("user_id"),
                validator.expect_column_values_to_be_between("age", min_value=5, max_value=100, mostly=1.0),
            ]
        else:
            expectations = [
                validator.expect_column_values_to_not_be_null("user_id"),
                validator.expect_column_values_to_not_be_null("isbn"),
                validator.expect_column_values_to_be_between(
                    "book_rating", min_value=0, max_value=10
                ),
            ]

        passed_count = sum(1 for result in expectations if result.success)
        failed_count = len(expectations) - passed_count

        print(f"Table: {table_name}")
        print(f"  Passed expectations: {passed_count}")
        print(f"  Failed expectations: {failed_count}")

        for result in expectations:
            status = "PASS" if result.success else "FAIL"
            expectation_name = result.expectation_config.expectation_type
            print(f"  - {expectation_name}: {status}")

        if failed_count > 0:
            all_tables_passed = False

    con.close()

    if not all_tables_passed:
        raise ValueError("Data validation failed.")

    print("All data validation checks passed.")

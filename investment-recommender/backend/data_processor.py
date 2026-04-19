import pandas as pd
import psycopg2

from db import get_db_connection


def load_investments(conn):
    """Load all investment rows from PostgreSQL into a pandas DataFrame.

    Args:
        conn: Open psycopg2 database connection.

    Returns:
        pandas.DataFrame with columns: id, fund_name, risk_level, returns,
        min_investment, category.
    """
    query = """
        SELECT id, fund_name, risk_level, returns, min_investment, category
        FROM investments
    """
    with conn.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    print(f"Loaded {len(rows)} investment records from database.")

    columns = ["id", "fund_name", "risk_level", "returns", "min_investment", "category"]
    return pd.DataFrame(rows, columns=columns)


def clean_investments(df):
    """Clean investment records for reliable recommendation filtering.

    Args:
        df: Raw investment DataFrame from load_investments.

    Returns:
        Cleaned pandas.DataFrame with normalized risk levels, numeric return and
        minimum investment fields, and duplicate funds removed.
    """
    cleaned_df = df.copy()

    cleaned_df = cleaned_df.dropna(
        subset=["fund_name", "risk_level", "returns", "min_investment"]
    )

    cleaned_df["risk_level"] = cleaned_df["risk_level"].astype(str).str.strip().str.lower()

    cleaned_df["returns"] = pd.to_numeric(cleaned_df["returns"], errors="coerce")
    cleaned_df["min_investment"] = pd.to_numeric(cleaned_df["min_investment"], errors="coerce")

    cleaned_df = cleaned_df.dropna(subset=["returns", "min_investment"])

    cleaned_df["returns"] = cleaned_df["returns"].astype(float)
    cleaned_df["min_investment"] = cleaned_df["min_investment"].astype(int)

    cleaned_df = cleaned_df.drop_duplicates(subset=["fund_name"])

    return cleaned_df


def filter_investments(df, risk_level, budget):
    """Filter investments by risk level and user budget.

    Args:
        df: Cleaned investment DataFrame.
        risk_level: Risk label to match (low, medium, high).
        budget: Maximum investment budget value.

    Returns:
        pandas.DataFrame containing investments matching risk and budget.
    """
    normalized_risk = str(risk_level).strip().lower()
    budget_value = int(budget)

    filtered_df = df[(df["risk_level"] == normalized_risk) & (df["min_investment"] <= budget_value)]
    return filtered_df


def rank_investments(df):
    """Rank filtered investments by annual return and return top 5 rows.

    Args:
        df: Filtered investment DataFrame.

    Returns:
        pandas.DataFrame containing the top five highest-return investments.
    """
    ranked_df = df.sort_values(by="returns", ascending=False)
    return ranked_df.head(5)


if __name__ == "__main__":
    connection = None
    try:
        connection = get_db_connection()

        investments_df = load_investments(connection)
        cleaned_df = clean_investments(investments_df)
        filtered_df = filter_investments(cleaned_df, risk_level="medium", budget=5000)
        top_recommendations = rank_investments(filtered_df)

        print("Top 5 recommendations:")
        print(top_recommendations.to_string(index=False))
    except psycopg2.Error as exc:
        print(f"Database unavailable. Could not fetch investment data: {exc}")
    finally:
        if connection is not None:
            connection.close()

import psycopg2

from data_processor import (
    clean_investments,
    filter_investments,
    load_investments,
    rank_investments,
)
from db import get_db_connection


def get_recommendations(risk_level, budget):
    normalized_risk = str(risk_level).strip().lower()
    if normalized_risk not in {"low", "medium", "high"}:
        raise ValueError("Invalid risk level. Must be low, medium, or high.")

    if isinstance(budget, bool) or not isinstance(budget, int) or budget <= 0:
        raise ValueError("Budget must be a positive integer.")

    connection = None
    try:
        connection = get_db_connection()
        investments_df = load_investments(connection)
        cleaned_df = clean_investments(investments_df)
        filtered_df = filter_investments(cleaned_df, normalized_risk, budget)
        ranked_df = rank_investments(filtered_df)
        if ranked_df.empty:
            return []
        return ranked_df.to_dict(orient="records")
    finally:
        if connection is not None:
            connection.close()


def format_recommendations(recommendations):
    if not recommendations:
        return []

    formatted = []
    for item in recommendations:
        formatted.append(
            {
                "fund_name": item.get("fund_name"),
                "returns": item.get("returns"),
                "min_investment": item.get("min_investment"),
                "category": item.get("category"),
                "risk_level": item.get("risk_level"),
            }
        )
    return formatted


if __name__ == "__main__":
    try:
        recommendations = get_recommendations(risk_level="high", budget=10000)
        formatted_recommendations = format_recommendations(recommendations)

        for recommendation in formatted_recommendations:
            print(recommendation)
    except ValueError as exc:
        print(f"Input validation error: {exc}")
    except psycopg2.Error as exc:
        print(f"Database connection error: {exc}")

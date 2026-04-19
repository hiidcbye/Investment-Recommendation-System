def save_recommendation_history(conn, risk_level, budget, recommendations):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO users (risk_level, budget)
                VALUES (%s, %s)
                RETURNING id
                """,
                (risk_level, budget),
            )
            user_id = cursor.fetchone()[0]

            for recommendation in recommendations:
                fund_name = recommendation.get("fund_name")
                if not fund_name:
                    continue

                cursor.execute(
                    "SELECT id FROM investments WHERE fund_name = %s",
                    (fund_name,),
                )
                investment_row = cursor.fetchone()
                if not investment_row:
                    continue

                investment_id = investment_row[0]
                cursor.execute(
                    """
                    INSERT INTO recommendation_history (user_id, investment_id)
                    VALUES (%s, %s)
                    """,
                    (user_id, investment_id),
                )

        conn.commit()
    except Exception:
        conn.rollback()
        raise


def get_recommendation_history(conn, limit=10):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                rh.id AS history_id,
                i.fund_name,
                u.risk_level,
                u.budget,
                i.returns,
                i.min_investment,
                i.category,
                rh.recommended_at
            FROM recommendation_history rh
            JOIN users u ON rh.user_id = u.id
            JOIN investments i ON rh.investment_id = i.id
            ORDER BY rh.recommended_at DESC
            LIMIT %s
            """,
            (limit,),
        )
        rows = cursor.fetchall()

    history = []
    for row in rows:
        history.append(
            {
                "history_id": row[0],
                "fund_name": row[1],
                "risk_level": row[2],
                "budget": row[3],
                "returns": row[4],
                "min_investment": row[5],
                "category": row[6],
                "recommended_at": row[7].strftime("%Y-%m-%d %H:%M") if row[7] else "",
            }
        )

    return history

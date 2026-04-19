import psycopg2
import time
from flask import Flask, jsonify, request
from flask_cors import CORS

from db import get_db_connection
from history import get_recommendation_history, save_recommendation_history
from recommender import format_recommendations, get_recommendations

app = Flask(__name__)
CORS(
    app,
    resources={
        r"/recommend": {"origins": "http://localhost:5173"},
        r"/history": {"origins": "http://localhost:5173"},
    },
)


@app.get("/health")
def health_check():
    return jsonify({"status": "ok"}), 200


@app.post("/recommend")
def recommend():
    start_time = time.time()

    def timed_json_response(payload, status_code):
        elapsed = time.time() - start_time
        if elapsed > 2:
            print(f"WARNING: /recommend took {elapsed:.2f}s — exceeds 2s SRS requirement")
        return jsonify(payload), status_code

    try:
        data = request.get_json(silent=True)

        if not data or "risk" not in data or "budget" not in data:
            return timed_json_response(
                {"error": "Missing required fields: risk and budget"},
                400,
            )

        risk = str(data["risk"]).strip()
        budget = data["budget"]

        if len(risk) > 20:
            return timed_json_response(
                {"error": "Risk value must not exceed 20 characters."},
                400,
            )

        if isinstance(budget, str):
            return timed_json_response(
                {"error": "Budget must be an integer, not a string."},
                400,
            )

        recommendations = get_recommendations(risk_level=risk, budget=budget)
        formatted_recommendations = format_recommendations(recommendations)

        history_conn = None
        try:
            history_conn = get_db_connection()
            save_recommendation_history(history_conn, risk, budget, formatted_recommendations)
        except Exception as exc:
            print(f"Failed to save recommendation history: {exc}")
        finally:
            if history_conn is not None:
                history_conn.close()

        return timed_json_response(formatted_recommendations, 200)
    except ValueError as exc:
        return timed_json_response({"error": str(exc)}, 400)
    except psycopg2.Error:
        return timed_json_response(
            {"error": "Database unavailable. Please try again later."},
            503,
        )
    except Exception as exc:
        print(f"Unexpected /recommend error: {exc}")
        return timed_json_response({"error": "Internal server error."}, 500)


@app.get("/history")
def history():
    try:
        limit_param = request.args.get("limit", default=10)
        try:
            limit = int(limit_param)
        except (TypeError, ValueError):
            limit = 10

        if limit < 1:
            limit = 10
        if limit > 50:
            limit = 50

        conn = None
        try:
            conn = get_db_connection()
            history_rows = get_recommendation_history(conn, limit=limit)
            return jsonify(history_rows), 200
        finally:
            if conn is not None:
                conn.close()
    except psycopg2.Error:
        return jsonify({"error": "Database unavailable."}), 503
    except Exception as exc:
        print(f"Unexpected /history error: {exc}")
        return jsonify({"error": "Internal server error."}), 500


if __name__ == "__main__":
    app.run(debug=True)

# Investment Recommendation System

A full-stack web application that provides personalized investment recommendations
based on user risk tolerance and budget.

## Tech Stack

- Frontend: React (Vite)
- Backend: Python (Flask)
- Database: PostgreSQL
- Data Processing: Python (Pandas)

## Project Structure

- backend/ - Flask API, recommendation engine, data processing, DB layer
- frontend/ - React UI with form, results table, and history view

## Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL 14+
- npm 9+

## Getting Started

### 1. Clone the repository

```bash
git clone <repo-url>
cd investment-recommender
```

### 2. Backend Setup

- Create and activate a virtual environment
- Install dependencies from requirements.txt
- Copy .env.example to .env and fill in your PostgreSQL credentials
- Run init_db.py to initialize and seed the database
- Start the Flask server with flask run

### 3. Frontend Setup

- Navigate to frontend/
- Run npm install
- Run npm run dev
- Open http://localhost:5173 in your browser

## API Endpoints

| Method | Endpoint   | Description                     | Request Body / Params                   |
| ------ | ---------- | ------------------------------- | --------------------------------------- |
| GET    | /health    | Health check                    | None                                    |
| POST   | /recommend | Get investment recommendations  | {"risk": string, "budget": int}         |
| GET    | /history   | Get past recommendation history | ?limit=N (optional, default 10, max 50) |

## Environment Variables

| Variable | Description       | Example      |
| -------- | ----------------- | ------------ |
| DB_HOST  | PostgreSQL host   | localhost    |
| DB_PORT  | PostgreSQL port   | 5432         |
| DB_NAME  | Database name     | investdb     |
| DB_USER  | Database username | postgres     |
| DB_PASS  | Database password | yourpassword |

## Non-Functional Requirements

- Response time target: under 2 seconds for POST /recommend
- Input validation enforced on both frontend and backend
- All endpoints return clean JSON errors - no raw tracebacks exposed
- DB initialization is idempotent - safe to run init_db.py multiple times

## Future Enhancements

- Machine learning-based recommendations
- Real-time market data integration
- User authentication system
- Portfolio tracking

import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [risk, setRisk] = useState("medium");
  const [budget, setBudget] = useState("");
  const [recommendations, setRecommendations] = useState([]);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadHistory = async () => {
      try {
        const response = await axios.get("http://localhost:5000/history");
        if (Array.isArray(response.data)) {
          setHistory(response.data);
        }
      } catch {
        // Ignore history errors for a non-blocking initial page experience.
      }
    };

    loadHistory();
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();

    const parsedBudget = Number.parseInt(budget, 10);
    if (!budget || !Number.isInteger(parsedBudget) || parsedBudget <= 0) {
      setError("Please enter a valid positive budget amount.");
      return;
    }

    setLoading(true);
    setError("");
    setRecommendations([]);

    try {
      const response = await axios.post("http://localhost:5000/recommend", {
        risk,
        budget: parsedBudget,
      });
      setRecommendations(Array.isArray(response.data) ? response.data : []);
    } catch (err) {
      const message =
        err?.response?.data?.error || "Something went wrong. Please try again.";
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="app-container">
      <h1>Investment Recommender</h1>
      <h2>Find Your Investment Match</h2>
      <p>
        Enter your risk tolerance and budget to get personalized investment
        suggestions.
      </p>

      <form className="recommend-form" onSubmit={handleSubmit}>
        <label htmlFor="risk">Risk Level</label>
        <select
          id="risk"
          value={risk}
          onChange={(event) => setRisk(event.target.value)}
        >
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>

        <label htmlFor="budget">Budget Amount</label>
        <input
          id="budget"
          type="number"
          min="1"
          step="1"
          placeholder="Enter your budget (e.g. 5000)"
          value={budget}
          onChange={(event) => setBudget(event.target.value)}
        />

        <button type="submit" disabled={loading}>
          Get Recommendations
        </button>
      </form>

      {loading && <p>Loading...</p>}
      {error && <p className="error-text">{error}</p>}

      {!loading && !error && (
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Fund Name</th>
                <th>Category</th>
                <th>Risk Level</th>
                <th>Min Investment</th>
                <th>Returns (%)</th>
              </tr>
            </thead>
            <tbody>
              {recommendations.length > 0 ? (
                recommendations.map((item, index) => (
                  <tr key={`${item.fund_name}-${index}`}>
                    <td>{item.fund_name}</td>
                    <td>{item.category}</td>
                    <td>{item.risk_level}</td>
                    <td>{`₹${item.min_investment}`}</td>
                    <td>{`${Number(item.returns).toFixed(2)}%`}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="5">Submit the form to see recommendations</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}

      <section>
        <h2>Past Recommendations</h2>
        {history.length > 0 ? (
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Fund Name</th>
                  <th>Category</th>
                  <th>Risk Level</th>
                  <th>Budget (₹)</th>
                  <th>Returns (%)</th>
                </tr>
              </thead>
              <tbody>
                {history.map((item) => (
                  <tr key={item.history_id}>
                    <td>{item.recommended_at}</td>
                    <td>{item.fund_name}</td>
                    <td>{item.category}</td>
                    <td>{item.risk_level}</td>
                    <td>{`₹${item.budget}`}</td>
                    <td>{`${Number(item.returns).toFixed(2)}%`}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p>No history yet.</p>
        )}
      </section>
    </main>
  );
}

export default App;

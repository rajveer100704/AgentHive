import React, { useState } from "react";

function QueryForm({ onSubmit }) {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) {
      setError("Query cannot be empty");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      await onSubmit(query);
    } catch (err) {
      setError("Error fetching results");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter your query..."
      />
      <button type="submit" disabled={loading}>
        {loading ? "Loading..." : "Submit"}
      </button>
      {error && <p style={{ color: "red" }}>{error}</p>}
    </form>
  );
}

export default QueryForm;

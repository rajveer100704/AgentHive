import React, { useState } from "react";
import QueryForm from "./components/QueryForm";
import ResultsList from "./components/ResultsList";
import axios from "axios";

function App() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleQuery = async (query) => {
    setLoading(true);
    try {
      const response = await axios.post("http://localhost:8000/query", { query });
      setResults(response.data.results || []);
    } catch (error) {
      console.error("API Error:", error);
      setResults([{ text: "Error fetching results", meta: {} }]);
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>AgentHive Research Assistant</h1>
      <QueryForm onSubmit={handleQuery} />
      {loading ? <p>Loading...</p> : <ResultsList results={results} />}
    </div>
  );
}

export default App;

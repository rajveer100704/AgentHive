import React from "react";

function ResultsList({ results }) {
  if (!results || results.length === 0) return <p>No results found.</p>;

  return (
    <ul>
      {results.map((res, idx) => (
        <li key={idx} style={{ marginBottom: "1rem", borderBottom: "1px solid #ccc", paddingBottom: "0.5rem" }}>
          <p><strong>Text:</strong> {res.text}</p>
          {res.meta && Object.keys(res.meta).length > 0 && (
            <p><strong>Meta:</strong> {JSON.stringify(res.meta)}</p>
          )}
        </li>
      ))}
    </ul>
  );
}

export default ResultsList;

"use client";

import { useState } from "react";

export default function HomePage() {
  const [category, setCategory] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any[]>([]);
  const [error, setError] = useState("");

  async function generateVocab() {
    setLoading(true);
    setError("");
    setResult([]);

    try {
      const res = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ category }),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.error || "Failed to generate vocabulary");
        setLoading(false);
        return;
      }

      if (data.vocab && Array.isArray(data.vocab)) {
        setResult(data.vocab);
      } else {
        setError("Invalid response from server");
      }
    } catch (err) {
      setError("Error calling API");
    }

    setLoading(false);
  }

  function copyToClipboard() {
    if (result.length > 0) {
      navigator.clipboard.writeText(JSON.stringify(result, null, 2));
      alert("Copied to clipboard!");
    }
  }

  return (
    <main className="p-8 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Vocabulary Generator</h1>

      <input
        type="text"
        placeholder="Enter category"
        value={category}
        onChange={(e) => setCategory(e.target.value)}
        className="border p-2 mb-4 w-full"
      />

      <button
        onClick={generateVocab}
        disabled={loading || !category.trim()}
        className="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50"
      >
        {loading ? "Generating..." : "Generate Vocabulary"}
      </button>

      {error && <p className="text-red-600 mt-4">{error}</p>}

      {result.length > 0 && (
        <div className="mt-6">
          <strong>Generated Vocabulary (copy-paste ready):</strong>
          <pre className="bg-gray-100 p-4 rounded overflow-x-auto whitespace-pre-wrap">
            {JSON.stringify(result, null, 2)}
          </pre>
          <button
            onClick={copyToClipboard}
            className="mt-2 bg-green-600 text-white px-4 py-2 rounded"
          >
            Copy to Clipboard
          </button>
        </div>
      )}
    </main>
  );
}

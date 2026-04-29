import React, { useEffect, useState } from "react";

export function ViewBatches() {
  const [batches, setBatches] = useState([]);
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  useEffect(() => {
    fetch("http://localhost:5000/batches_list")
      .then((res) => res.json())
      .then((data) => {
        console.log("API DATA:", data);
        setBatches(data);
      })
      .catch((err) => console.error("Error:", err));
  }, []);

  const handleExport = async () => {
    const token = localStorage.getItem("token");
    const response = await fetch("http://localhost:5000/export_batches", {
      headers: { "Authorization": `Bearer ${token}` }
    });
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "batches.xlsx";
    document.body.appendChild(a);
    a.click();
    a.remove();
  };

  // Filter batches client-side by date range
  const filteredBatches = batches.filter((bat) => {
    const created = new Date(bat.date_created);
    const start = startDate ? new Date(startDate) : null;
    const end = endDate ? new Date(endDate) : null;
    if (start && created < start) return false;
    if (end && created > end) return false;
    return true;
  });

  const handleClearFilters = () => {
    setStartDate("");
    setEndDate("");
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>View Batches</h1>

      {/* Filter controls */}
      <div style={{ marginBottom: "1rem", display: "flex", gap: "0.5rem", alignItems: "center", marginLeft:"36rem" }}>
        <label style={{ fontSize: "0.85rem" }}>
          From:{" "}
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            style={{ fontSize: "0.8rem", padding: "2px 4px" }}
          />
        </label>
        <label style={{ fontSize: "0.85rem" }}>
          To:{" "}
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            style={{ fontSize: "0.8rem", padding: "2px 4px" }}
          />
        </label>
        <button onClick={handleClearFilters}>Clear</button>
        <span style={{ color: "#666", fontSize: "0.9rem" }}>
          Showing {filteredBatches.length} of {batches.length} batches
        </span>
      </div>

      <h2>Batches</h2>
      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>BatchID</th>
            <th>Batch Number</th>
            <th>Flavor Name</th>
            <th>User Name</th>
            <th>Bottles</th>
            <th>Date Created</th>
          </tr>
        </thead>
        <tbody>
          {filteredBatches.map((bat) => (
            <BatchIDRow key={bat.batchid} batches={bat} />
          ))}
        </tbody>
      </table>

      <button onClick={handleExport} style={{ marginTop: "1rem", padding: "0.5rem 0.8rem" }}>
        Export
      </button>
    </div>
  );
}

function BatchIDRow({ batches }) {
  return (
    <tr>
      <td>{batches.batchid}</td>
      <td>{batches.batchnumber}</td>
      <td>{batches.flavorname}</td>
      <td>{batches.user_name}</td>
      <td>{batches.bottles}</td>
      <td>{batches.date_created}</td>
    </tr>
  );
}
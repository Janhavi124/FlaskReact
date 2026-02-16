import React, { useEffect, useState } from "react";

function MakeFlavor() {
  const [flavors, setFlavors] = useState([]);
  const [selectedFlavor, setSelectedFlavor] = useState("");
  const [bottles, setBottles] = useState("");
  const [result, setResult] = useState(null);
  const [batchSaved, setBatchSaved] = useState(false);

  // Fetch available flavors from Flask
  useEffect(() => {
    fetch("https://flaskreact-production-d646.up.railway.app/flavors")
    //fetch("http://localhost:5000/flavors")
      .then((res) => res.json())
      .then((data) => setFlavors(data))
      .catch((err) => console.error("Error fetching flavors:", err));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");
    const res = await fetch("https://flaskreact-production-d646.up.railway.app/calculate_flavor", {
    //const res = await fetch("http://localhost:5000/calculate_flavor", {
      method: "POST",
      headers: { "Content-Type": "application/json" , "Authorization": `Bearer ${token}`},
      body: JSON.stringify({ flavorname: selectedFlavor, bottles }),
    });
    const data = await res.json();
    setResult(data);
    setBatchSaved(false);

};
    const handleSaveBatch = async () => {
  const token= localStorage.getItem("token");
  const res = await fetch("https://flaskreact-production-d646.up.railway.app/save_batch", {
    //const res = await fetch("http://localhost:5000/save_batch", {
   
    method: "POST",
    headers: { "Content-Type": "application/json" ,  "Authorization": `Bearer ${token}`},
    body: JSON.stringify({ flavorname: selectedFlavor, bottles }),
  });
  const data = await res.json();
  if (data.success) {
    alert(`✅ ${data.message}`);
    setBatchSaved(true);
  }  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>Flavor Calculator</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Select Flavor:{" "}
          <select
            value={selectedFlavor}
            onChange={(e) => setSelectedFlavor(e.target.value)}
            required
          >
            <option value="">--Choose--</option>
            {flavors.map((f) => (
              <option key={f.id} value={f.name}>
                {f.name}
              </option>
            ))}
          </select>
        </label>

        <br />
        <label>
          Number of bottles:{" "}
          <input
          type="number"
          value={bottles}
          onChange={(e) => setBottles(e.target.value)}
          min="10"
          required
        />
        </label>

        <br />
        <button type="submit">Calculate</button>
      </form>

      {result  && result.ingredients && (
        
        <div style={{ marginTop: "2rem" }}>
          <h2>
            {result.flavor} ({result.bottles} bottles)
          </h2>
          <table border="1" cellPadding="8">
            <thead>
              <tr>
                <th>Ingredient</th>
                <th>Amount</th>
              </tr>
            </thead>
            <tbody>
              {result.ingredients.map((ing, i) => (
                <tr key={i}>
                  <td>{ing.ingredient_name}</td>
                  <td>{ing.amount.toFixed(2)} {ing.unit}</td>
                </tr>
                
                
              ))}
            </tbody>
          </table>
          
          <button 
  onClick={handleSaveBatch}
  disabled={batchSaved || !result.can_produce}
  style={{ 
    marginTop: '1rem', 
    padding: '0.5rem 1rem', 
    cursor: (batchSaved || !result.can_produce) ? 'not-allowed' : 'pointer',
    opacity: (batchSaved || !result.can_produce) ? 0.5 : 1
  }}
>
  {batchSaved ? 'Batch Saved ✓' : 'Made Batch'}
</button>

{result.insufficient_stock && result.insufficient_stock.length > 0 && (
  <div style={{ marginTop: '1rem', color: 'red', fontWeight: 'bold' }}>
    ⚠️ Insufficient Stock:
    <ul>
      {result.insufficient_stock.map((item, i) => (
        <li key={i}>
          {item.ingredient}: Need {item.needed.toFixed(2)}g, Have {item.available.toFixed(2)}g
        </li>
      ))}
    </ul>
  </div>
)}
        </div>
        
      )
      }
    </div>
  );
}

export default MakeFlavor;
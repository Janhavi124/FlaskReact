/*import React, { useState , useEffect} from 'react';

function App() {
  const [num1, setNum1] = useState('');
  const [operation, setOperation] = useState('lemonlime');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleCalculate = async () => {
    setError('');
    setResult(null);
    try {
      const response = await fetch('http://localhost:5000/calculate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ num1, operation }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || 'Something went wrong');
      } else {
        setResult({
        message: data.message,
        formula: data.formula
      });
      }
    } catch (err) {
      setError('Error connecting to backend');
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h2>React + Flask Calculator</h2>

      <select value={operation} onChange={(e) => setOperation(e.target.value)}>
        <option value="lemonlime">Lemon-Lime</option>
        <option value="mango">Mango</option>
        <option value="guava">Guava</option>
        <option value="orange">Orange</option>
      </select>
      <br /><br />
      
      <input
        type="number"
        value={num1}
        onChange={(e) => setNum1(e.target.value)}
        placeholder="Number of bottles"
      />
      <br /><br />
      
      <button onClick={handleCalculate}>Calculate Formula</button>
      <br /><br />

      {error && <p style={{ color: 'red' }}>{error}</p>}
      {result !== null && <p>Result: {result && (
 <div>
  <p>{result.message}</p>
  
  <h3>Formula:</h3>
  <ul>
    {Array.isArray(result.formula) &&
      result.formula.map((item, idx) => (
        <li key={idx}>
  {item.ingredient}: {item.quantity.toFixed(2)}
</li>
      ))}
  </ul>
</div>
)}</p>}
    </div>
  );
}

export default App;*/


import React, { useEffect, useState } from "react";

function App() {
  const [flavors, setFlavors] = useState([]);
  const [selectedFlavor, setSelectedFlavor] = useState("");
  const [bottles, setBottles] = useState("");
  const [result, setResult] = useState(null);

  // Fetch available flavors from Flask
  useEffect(() => {
    fetch("http://localhost:5000/flavors")
      .then((res) => res.json())
      .then((data) => setFlavors(data))
      .catch((err) => console.error("Error fetching flavors:", err));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await fetch("http://localhost:5000/calculate_flavor", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ flavorname: selectedFlavor, bottles }),
    });
    const data = await res.json();
    setResult(data);
  };

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
            required
          />
        </label>

        <br />
        <button type="submit">Calculate</button>
      </form>

      {result && result.ingredients && (
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
        </div>
      )}
    </div>
  );
}

export default App;


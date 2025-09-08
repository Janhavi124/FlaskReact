import React, { useState , useEffect} from 'react';

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

export default App;

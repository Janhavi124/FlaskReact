import React, { useState , useEffect} from 'react';

function App() {
  const [num1, setNum1] = useState('');
  const [num2, setNum2] = useState('');
  const [operation, setOperation] = useState('add');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleCalculate = async () => {
    setError('');
    try {
      const response = await fetch('http://localhost:5000/calculate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ num1, num2, operation }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || 'Something went wrong');
      } else {
        setResult(data.result);
      }
    } catch (err) {
      setError('Error connecting to backend');
    }
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h2>React + Flask Calculator</h2>

      <select value={operation} onChange={(e) => setOperation(e.target.value)}>
        <option value="add">Add</option>
        <option value="subtract">Subtract</option>
        <option value="multiply">Multiply</option>
        <option value="divide">Divide</option>
      </select>
      <br /><br />
      
      <input
        type="number"
        value={num1}
        onChange={(e) => setNum1(e.target.value)}
        placeholder="Number 1"
      />
      <br /><br />
      <input
        type="number"
        value={num2}
        onChange={(e) => setNum2(e.target.value)}
        placeholder="Number 2"
      />
      <br /><br />
      
      <button onClick={handleCalculate}>Calculate</button>
      <br /><br />

      {error && <p style={{ color: 'red' }}>{error}</p>}
      {result !== null && <p>Result: {result}</p>}
    </div>
  );
}

export default App;

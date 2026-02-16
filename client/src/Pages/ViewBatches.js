import React, { useEffect, useState } from "react";

export function ViewBatches() {
  const [batches, setBatches] = useState([]);
 
  // Fetch ingredients on load
   useEffect(() => {
  fetch("https://flaskreact-production-d646.up.railway.app/batches_list")
  //fetch("http://localhost:5000/batches_list")
    .then((res) => res.json())
    .then((data) => {
      console.log("API DATA:", data); 
      setBatches(data);
    })
    .catch((err) => console.error("Error:", err));
}, []);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>View Batches</h1>

      <h2>Batches</h2>
      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>BatchID</th>
            <th>Batch Number</th>
            <th>Flavor ID</th>
            <th>Flavor Name</th>
            <th>User id</th>
            <th>Bottles</th>
            <th>Date Created</th>
          </tr>
        </thead>

        <tbody>
          {batches.map((bat) => (
            <BatchIDRow
              key={bat.batchid}
              batches={bat}
            />
          ))}
        </tbody>
      </table>

    </div>
  );
}

function BatchIDRow({ batches }) {
  /*const [newQty, setNewQty] = useState("");*/

  return (
    <tr>
      <td>{batches.batchid}</td>
      <td>{batches.batchnumber}</td>
      <td>{batches.flavorid}</td>
      <td>{batches.flavorname}</td>
      <td>{batches.user_id}</td>
      <td>{batches.bottles}</td>
      <td>{batches.date_created}</td>
      
    </tr>
  );
}
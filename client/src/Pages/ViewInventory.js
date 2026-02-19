import React, { useEffect, useState } from "react";

export function ViewInventory() {
  const [ingredients, setIngredients] = useState([]);
  const [bottles, setBottles] = useState(null);

  // Fetch ingredients on load
  useEffect(() => {
    fetch("https://flaskreact-production-d646.up.railway.app/ingredients_inventory")
      .then((res) => res.json())
      .then((data) => setIngredients(data))
      .catch((err) => console.error("Error:", err));

    // Fetch bottle count
    fetch("https://flaskreact-production-d646.up.railway.app/bottles_inventory")
      .then((res) => res.json())
      .then((data) => setBottles(data))
      .catch((err) => console.error("Error:", err));
  }, []);

const handleExport = async () => {
  const token = localStorage.getItem("token");

  const response = await fetch("https://flaskreact-production-d646.up.railway.app/export_inventory", {
    headers: {
      "Authorization": `Bearer ${token}`
    }
  });

  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = "inventory.xlsx";
  document.body.appendChild(a);
  a.click();
  a.remove();
};


  return (
    <div style={{ padding: "2rem" }}>
      <h1>Update Inventory</h1>

      <h2>Ingredients</h2>
      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>Ingredient</th>
            <th>Current Stock (g)</th>
          </tr>
        </thead>
        <tbody>
          {ingredients.map((ing) => (
            <IngredientRow
              key={ing.id}
              ingredient={ing}
            />
          ))}
        </tbody>
      </table>

      <h2>Bottles</h2>
      {bottles && (
        <BottleRow bottle={bottles} />
      )}

          <button
  onClick={handleExport}
  style={{
    marginTop: "1rem",
    padding: "0.5rem 0.8rem"
  }}
>
  Export
</button>
    </div>
  );
}

function IngredientRow({ ingredient, onUpdate }) {
  /*const [newQty, setNewQty] = useState("");*/

  return (
    <tr>
      <td>{ingredient.name}</td>
      <td>{ingredient.available}</td>
      
    </tr>
  );
}

function BottleRow({ bottle, onUpdate }) {
  /*const [newCount, setNewCount] = useState("");*/

  return (
    <div>
      <p>Current Bottles: {bottle.count}</p>
    </div>
  );
}
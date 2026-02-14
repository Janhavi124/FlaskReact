import React, { useEffect, useState } from "react";

export function UpdateInventory() {
  const [ingredients, setIngredients] = useState([]);
  const [bottles, setBottles] = useState(null);

  // Fetch ingredients on load
  useEffect(() => {
    fetch("flaskreact-production-d646.up.railway.app/ingredients_inventory")
      .then((res) => res.json())
      .then((data) => setIngredients(data))
      .catch((err) => console.error("Error:", err));

    // Fetch bottle count
    fetch("flaskreact-production-d646.up.railway.app/bottles_inventory")
      .then((res) => res.json())
      .then((data) => setBottles(data))
      .catch((err) => console.error("Error:", err));
  }, []);

  const updateIngredient = async (ingredientId, newQuantity) => {
    await fetch("flaskreact-production-d646.up.railway.app/update_ingredient", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ingredientId, newQuantity }),
    });
    alert("Ingredient updated!");
  };

  const updateBottles = async (newCount) => {
    await fetch("flaskreact-production-d646.up.railway.app/update_bottles", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ newCount }),
    });
    alert("Bottles updated!");
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
            <th>New Amount</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {ingredients.map((ing) => (
            <IngredientRow
              key={ing.id}
              ingredient={ing}
              onUpdate={updateIngredient}
            />
          ))}
        </tbody>
      </table>

      <h2>Bottles</h2>
      {bottles && (
        <BottleRow bottle={bottles} onUpdate={updateBottles} />
      )}
    </div>
  );
}

function IngredientRow({ ingredient, onUpdate }) {
  const [newQty, setNewQty] = useState("");

  return (
    <tr>
      <td>{ingredient.name}</td>
      <td>{ingredient.available}</td>
      <td>
        <input
          type="number"
          value={newQty}
          onChange={(e) => setNewQty(e.target.value)}
          placeholder="Enter new amount"
          min="10"
        />
      </td>
      <td>
        <button onClick={() => {
        if (parseFloat(newQty) >= 0) {
            onUpdate(ingredient.id, parseFloat(newQty))
        } else {
            alert("Please enter a valid amount")
        }
        }}>
        Update
        </button>
      </td>
    </tr>
  );
}

function BottleRow({ bottle, onUpdate }) {
  const [newCount, setNewCount] = useState("");

  return (
    <div>
      <p>Current Bottles: {bottle.count}</p>
      <input
        type="number"
        value={newCount}
        onChange={(e) => setNewCount(e.target.value)}
        placeholder="Enter new count"
         min="10"
      />
      <button onClick={() => {
        if (parseFloat(newCount) >= 0) {
            onUpdate(parseFloat(newCount))
        } else {
            alert("Please enter a valid amount")
        }
        }}>
        Update
        </button>
    </div>
  );
}
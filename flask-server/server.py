from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

universal_total_quantity=180
universal_carbonated_water=135

def formula_lemon_lime(bottles):
    total_liquid=universal_total_quantity*bottles
    total_syrup_quantity=total_liquid*0.25
    return [
        {"ingredient": "Invert Sugar,75 Brix", "quantity":total_syrup_quantity*0.6411},
        {"ingredient": "Citric Acid Solution 20%", "quantity": total_syrup_quantity*0.055},
        {"ingredient": "Sodium Benzoate, Food Grade", "quantity": total_syrup_quantity*0.0015},
        {"ingredient": "Potassium Sorbate, Food Grade", "quantity": total_syrup_quantity*0.0006},
        {"ingredient": "Glycerine, Food Grade", "quantity": total_syrup_quantity*0.04},
        {"ingredient": "Yellow Synthetic 500-636 ", "quantity": total_syrup_quantity*0.0004},
        {"ingredient": "blue 500-634", "quantity": total_syrup_quantity*0.00004},
        {"ingredient": "Still Water ", "quantity": total_syrup_quantity*0.2534},
        {"ingredient": "Lemon Lime Flavor ", "quantity": total_syrup_quantity*0.008},
        {"ingredient": "Carbonated Water ", "quantity": total_liquid *0.75}
    ]

def formula_mango(bottles):
     total_liquid=universal_total_quantity*bottles
     total_syrup_quantity=total_liquid*0.25
     return [
        {"ingredient": "Invert Sugar,75 Brix", "quantity":total_syrup_quantity*0.6411},
        {"ingredient": "Citric Acid Solution 20%", "quantity": total_syrup_quantity*0.05},
        {"ingredient": "Sodium Benzoate, Food Grade", "quantity": total_syrup_quantity*0.0015},
        {"ingredient": "Potassium Sorbate, Food Grade", "quantity": total_syrup_quantity*0.0006},
        {"ingredient": "Glycerine, Food Grade", "quantity": total_syrup_quantity*0.04},
        {"ingredient": "Yellow Synthetic 500-636 ", "quantity": total_syrup_quantity*0.0008},
        {"ingredient": "Still Water ", "quantity": total_syrup_quantity*0.2508},
        {"ingredient": "Mango, AF104357 ", "quantity": total_syrup_quantity*0.002},
        {"ingredient": "Mango AF 106116 ", "quantity": total_syrup_quantity*0.006},
        {"ingredient": "Carbonated Water ", "quantity": total_liquid *0.75}
    ]

def formula_guava(bottles):
    total_liquid=universal_total_quantity*bottles
    total_syrup_quantity=total_liquid*0.25
    return [
        {"ingredient": "Invert Sugar,75 Brix", "quantity":total_syrup_quantity*0.6411},
        {"ingredient": "Citric Acid Solution 20%", "quantity": total_syrup_quantity*0.05},
        {"ingredient": "Sodium Benzoate, Food Grade", "quantity": total_syrup_quantity*0.0015},
        {"ingredient": "Potassium Sorbate, Food Grade", "quantity": total_syrup_quantity*0.00015},
        {"ingredient": "Glycerine, Food Grade", "quantity": total_syrup_quantity*0.04},
        {"ingredient": "Exberry Fruit Yellow 459377 Color ", "quantity": total_syrup_quantity*0.0008},
        {"ingredient": "15330021 Exberry Vivid Red ", "quantity": total_syrup_quantity*0.0028},
        {"ingredient": "Still Water", "quantity": total_syrup_quantity*0.2549},
        {"ingredient": "Guava 600554", "quantity": total_syrup_quantity*0.0088},
        {"ingredient": "Carbonated Water ", "quantity": total_liquid *0.75}
    ]

def formula_orange(bottles):
   total_liquid=universal_total_quantity*bottles
   total_syrup_quantity=total_liquid*0.25
   return [
        {"ingredient": "Invert Sugar,75 Brix", "quantity":total_syrup_quantity*0.6411},
        {"ingredient": "Citric Acid Solution 20%", "quantity": total_syrup_quantity*0.05},
        {"ingredient": "Sodium Benzoate, Food Grade", "quantity": total_syrup_quantity*0.0015},
        {"ingredient": "Potassium Sorbate, Food Grade", "quantity": total_syrup_quantity*0.0006},
        {"ingredient": "Glycerine, Food Grade", "quantity": total_syrup_quantity*0.04},
        {"ingredient": "Orange 500-635 ", "quantity": total_syrup_quantity*0.006},
        {"ingredient": "Orange, 210635 ", "quantity": total_syrup_quantity*0.008},
        {"ingredient": "Still Water", "quantity": total_syrup_quantity*0.2528},
        {"ingredient": "Carbonated Water ", "quantity": total_liquid *0.75}
    ]

flavors = {
    "lemonlime": formula_lemon_lime,
    "mango": formula_mango,
    "guava": formula_guava,
    "orange": formula_orange,

}

@app.route("/calculate" , methods=['POST'])
def calculate():
     data = request.get_json()
     num1 = data.get('num1')
     operation = data.get('operation')

     try:
        num1 = float(num1)
     except (ValueError, TypeError):
        return jsonify({'error': 'Invalid number inputs'}), 400
     formula_func = flavors.get(operation.lower())
     if not formula_func:
        return jsonify({'error': f"Flavor '{operation}' not supported"}), 400

     formula = formula_func(num1)
     result = {
        "message": f"You want to make {num1} bottles of {operation}.",
        "formula": formula
    }

     return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:FlavorFormula@localhost/Reviv'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) #instantiate db object

class Flavor(db.Model):
   __tablename__ = 'flavors'
   flavorid = db.Column(db.Integer, primary_key=True)
   flavorname = db.Column(db.String(100))
   quantity = db.relationship('Quantity', back_populates='flavor', cascade='all, delete-orphan')

class Ingredient(db.Model):
   __tablename__ = 'ingredients'
   ingredientid = db.Column(db.Integer, primary_key=True)
   ingredientname = db.Column(db.String(400))
   quantity = db.relationship('Quantity', back_populates='ingredient', cascade='all, delete-orphan')


class Quantity(db.Model):
    __tablename__ = 'quantity'
    id = db.Column(db.Integer, primary_key=True)
    flavorid = db.Column(db.Integer, db.ForeignKey('flavors.flavorid'))
    ingredientid = db.Column(db.Integer, db.ForeignKey('ingredients.ingredientid'))
    baseamount = db.Column(db.Float)
    unit =db.Column(db.String(10))

    # Relationships (many-to-one)
    flavor = db.relationship('Flavor', back_populates='quantity')
    ingredient = db.relationship('Ingredient', back_populates='quantity')


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

@app.route('/flavors')
def get_flavors():
    data = db.session.query(Flavor).all()
    result = [{"id": f.flavorid, "name": f.flavorname} for f in data]
    return jsonify(result)

@app.route('/ingredients')
def get_ingredients():
    data=db.session.query(Ingredient).all()
    result=[{"id": i.ingredientid, "name": i.ingredientname} for i in data]
    return jsonify(result)

@app.route('/flavor/<string:flavorname>/<int:bottles>', methods=['GET'])
def get_flavor_details(flavorname,bottles):
    # 1️⃣ Find the flavor by name (case-insensitive)
    flavor = Flavor.query.filter(Flavor.flavorname.ilike(flavorname)).first()

    if not flavor:
        return jsonify({"error": f"Flavor '{flavorname}' not found"}), 404

    
    ingredients = []
    for q in flavor.quantity:
        ingredients.append({
            "ingredient_name": q.ingredient.ingredientname,
            "amount": q.baseamount*45*bottles,
            "unit": q.unit
            
        })

    # 3️⃣ Return JSON
    return jsonify({
        "flavor": flavor.flavorname,
        "ingredients": ingredients,
        "unit": q.unit
    })

@app.route('/calculate_flavor', methods=['POST'])
def calculate_flavor():
    data = request.get_json()
    flavorname = data.get('flavorname')
    bottles = data.get('bottles')

    try:
        bottles = float(bottles)
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid number of bottles'}), 400

    flavor = Flavor.query.filter(Flavor.flavorname.ilike(flavorname)).first()
    if not flavor:
        return jsonify({'error': f"Flavor '{flavorname}' not found"}), 404

    ingredients = []
    for q in flavor.quantity:
        ingredients.append({
            "ingredient_name": q.ingredient.ingredientname,
            "amount": float(q.baseamount)*45*bottles,
            "unit": q.unit
        })

    return jsonify({
        "flavor": flavor.flavorname,
        "bottles": bottles,
        "ingredients": ingredients
    })



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
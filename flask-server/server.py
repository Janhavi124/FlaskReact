from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:FlavorFormula@localhost/Reviv'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) #instantiate db object

class Flavor(db.Model):
   __tablename__ = 'flavors'
   flavorid = db.Column(db.Integer, primary_key=True)
   flavorname = db.Column(db.String(100))
   date_added = db.Column(db.Date)
   quantity = db.relationship('Quantity', back_populates='flavor', cascade='all, delete-orphan')

class Ingredient(db.Model):
   __tablename__ = 'ingredients'
   ingredientid = db.Column(db.Integer, primary_key=True)
   ingredientname = db.Column(db.String(400))
   availablequantity = db.Column(db.Float)
   date_added = db.Column(db.Date)
   quantity = db.relationship('Quantity', back_populates='ingredient', cascade='all, delete-orphan')


class Quantity(db.Model):
    __tablename__ = 'quantity'
    id = db.Column(db.Integer, primary_key=True)
    flavorid = db.Column(db.Integer, db.ForeignKey('flavors.flavorid'))
    ingredientid = db.Column(db.Integer, db.ForeignKey('ingredients.ingredientid'))
    date_added = db.Column(db.Date)
    date_updated = db.Column(db.Date)
    baseamount = db.Column(db.Float)
    unit =db.Column(db.String(10))

    # Relationships (many-to-one)
    flavor = db.relationship('Flavor', back_populates='quantity')
    ingredient = db.relationship('Ingredient', back_populates='quantity')

class batches(db.Model):
    __tablename__ = 'batches'
    batchid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    batchnumber = db.Column(db.String(100), unique=True)
    flavorid = db.Column(db.Integer, db.ForeignKey('flavors.flavorid'))
    bottles = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    flavor = db.relationship('Flavor', backref='batches')

universal_total_quantity=180
universal_carbonated_water=135

def generate_batch_number(flavorname, date_created):
    # Format: DATE-FLAVOR-SERIAL (e.g., 20250203-Strawberry-001)
    date_str = date_created.strftime('%Y%m%d')
    
    # Count batches for this flavor on this date
    count = batches.query.filter(
        db.func.date(batches.date_created) == date_created.date(),
        batches.flavorid == Flavor.query.filter(Flavor.flavorname.ilike(flavorname)).first().flavorid
    ).count()
    
    serial = str(count + 1).zfill(6)  # 001, 002, etc.
    
    return f"{date_str}-{flavorname}-{serial}"



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
    insufficient_stock=[]
    for q in flavor.quantity:
        availablequantity = q.ingredient.availablequantity
        needquantity =  float(q.baseamount)*45*bottles
        print(f"Checking {q.ingredient.ingredientname}: need {needquantity}, have {availablequantity}")  # ADD THIS
        ingredients.append({
            "ingredient_name": q.ingredient.ingredientname,
            "amount": needquantity,
            "unit": q.unit
        })
  
    
        if availablequantity < needquantity:
                insufficient_stock.append({
                    "ingredient": q.ingredient.ingredientname,
                    "needed": needquantity,
                    "available": availablequantity
                })
    return jsonify({
            "flavor": flavor.flavorname,
            "bottles": bottles,
            "ingredients": ingredients,
            "can_produce": len(insufficient_stock) == 0,
            "insufficient_stock": insufficient_stock
        })


@app.route('/save_batch', methods=['POST'])
def save_batch():
    data = request.get_json()
    flavorname = data.get('flavorname')
    bottles = data.get('bottles')

    try:
        bottles = int(bottles)
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid number of bottles'}), 400

    flavor = Flavor.query.filter(Flavor.flavorname.ilike(flavorname)).first()
    if not flavor:
        return jsonify({'error': f"Flavor '{flavorname}' not found"}), 404

    # Check stock again before saving
    for q in flavor.quantity:
        needed_amount = float(q.baseamount) * 45 * bottles
        available = q.ingredient.availablequantity or 0
        if available < needed_amount:
            return jsonify({
                'error': f'Insufficient stock for {q.ingredient.ingredientname}'
            }), 400

    # Deduct inventory
    for q in flavor.quantity:
        needed_amount = float(q.baseamount) * 45 * bottles
        q.ingredient.availablequantity -= needed_amount

    # Create and save batch
    now = datetime.utcnow()
    batch_number = generate_batch_number(flavorname, now)
    
    new_batch = batches(
        batchnumber=batch_number,
        flavorid=flavor.flavorid,
        bottles=bottles,
        date_created=now.date()
    )
    
    db.session.add(new_batch)
    db.session.commit()

    return jsonify({
        "success": True,
        "batch_number": batch_number,
        "message": f"Batch {batch_number} saved successfully"
    })

if __name__ == "__main__":
    app.run(debug=True)
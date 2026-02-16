import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
#from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps
from models import db, User, Containers, Quantity, Flavor, batches, Ingredient
import pandas as pd
from flask import send_file
from io import BytesIO

load_dotenv()



app = Flask(__name__)

CORS(app, resources={
    r"/*": {
        "origins": ["https://resplendent-trust-production.up.railway.app", "http://localhost:3000"],
        "allow_headers": ["Content-Type", "Authorization"],
        "methods": ["GET", "POST", "OPTIONS"]
    }
})

database_url = os.getenv("DATABASE_PUBLIC_URL")
database_secret_key = os.getenv("SECRET_KEY")

# Fix Railway's postgres:// to postgresql://
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SECRET_KEY'] = database_secret_key
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = True  # Required for HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # Required for cross-origin


#db = SQLAlchemy(app) #instantiate db object
db.init_app(app)

# JWT HELPER
def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            
            if not current_user:
                return jsonify({'error': 'Invalid token'}), 401
                
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated

# AUTH ROUTES
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user_name = data.get('user_name')
    user_email = data.get('user_email')
    password = data.get('password')
    
    if User.query.filter_by(user_name=user_name).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(user_email=user_email).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    new_user = User(user_name=user_name, user_email=user_email)
    new_user.set_password(password)
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'User registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_name = data.get('user_name')
    password = data.get('password')
    
    user = User.query.filter_by(user_name=user_name).first()
    
    if user and user.check_password(password):
        token = generate_token(user.user_id)
        return jsonify({
            'success': True,
            'token': token,
            'user_name': user.user_name
        })
    
    return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/check_auth', methods=['GET'])
@token_required
def check_auth(current_user):
    return jsonify({
        'authenticated': True,
        'user_name': current_user.user_name
    })

# Keep all your other routes below (flavors, ingredients, etc.)


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
    bottle_record = Containers.query.first()
    bottlesavailable = bottle_record.availablecount
    bottlesneeded = int(bottles)

    for q in flavor.quantity:
        availablequantity = q.ingredient.availablequantity
        needquantity =  float(q.baseamount)*45*bottles
       
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
    if bottlesavailable < bottlesneeded:
        insufficient_stock.append({
                    "ingredient": "Bottles",
                    "needed": bottlesneeded,
                    "available": bottlesavailable
                })
    return jsonify({
            "flavor": flavor.flavorname,
            "bottles": bottles,
            "ingredients": ingredients,
            "can_produce": len(insufficient_stock) == 0,
            "insufficient_stock": insufficient_stock
        })


@app.route('/save_batch', methods=['POST'])
@token_required
def save_batch(current_user):
    print("Inside save_batch, current_user:", current_user)
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
    
    #Deduct containers
    bottle_record = Containers.query.first()  # Assuming you have one row tracking total bottles
    if bottle_record:
        bottle_record.availablecount -= bottles

    # Create and save batch
    now = datetime.utcnow()
    batch_number = generate_batch_number(flavorname, now)
    
    new_batch = batches(
        batchnumber=batch_number,
        flavorid=flavor.flavorid,
        bottles=bottles,
        user_id= current_user.user_id,
        date_created=now.date()
    )
    
    db.session.add(new_batch)
    db.session.commit()

    return jsonify({
        "success": True,
        "batch_number": batch_number,
        "message": f"Batch {batch_number} saved successfully"
    })

@app.route('/batches_list', methods=['GET'])
def get_batches_list():
    
    data = db.session.query(batches,Flavor).join(Flavor).all()
    result = []
    for batch, flavor in data:
        result.append({
            "batchid": batch.batchid,
            "batchnumber": batch.batchnumber,
            "flavorid": batch.flavorid,
            "flavorname": flavor.flavorname,
            "user_id": batch.user_id,
            "bottles": batch.bottles,
            "date_created": batch.date_created
        })
    return jsonify(result)

@app.route('/ingredients_inventory', methods=['GET'])
def get_ingredients_inventory():
    data = db.session.query(Ingredient).all()
    result = [{"id": i.ingredientid, "name": i.ingredientname, "available": i.availablequantity} for i in data]
    return jsonify(result)

@app.route('/bottles_inventory', methods=['GET'])
def get_bottles_inventory():
    bottle = Containers.query.first()
    return jsonify({"count": bottle.availablecount if bottle else 0})

@app.route('/update_ingredient', methods=['POST'])
def update_ingredient():
    data = request.get_json()
    ingredient_id = data.get('ingredientId')
    new_quantity = data.get('newQuantity')
    
    ingredient = Ingredient.query.get(ingredient_id)
    if ingredient:
        ingredient.availablequantity = new_quantity
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"error": "Ingredient not found"}), 404

@app.route('/update_bottles', methods=['POST'])
def update_bottles():
    data = request.get_json()
    new_count = data.get('newCount')
    
    bottle = Containers.query.first()
    if bottle:
        bottle.availablecount = new_count
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"error": "Bottle record not found"}), 404

@app.route("/export_batches", methods=["GET"])
def export_batches():
    batchesList = db.session.query(batches).all()

    data = []
    for batch in batchesList:
        data.append({
            "Batch ID": batch.batchid,
            "Batch Number": batch.batchnumber,
            "Flavor ID": batch.flavorid,
            "Flavor": batch.flavor.flavorname,
            "User": batch.user.user_id,
            "Bottles": batch.bottles,
            "Date Created": batch.date_created
        })

    
    df = pd.DataFrame(data)

    output = BytesIO()
    df.to_excel(output, index=False, engine="openpyxl")
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="batches.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


@app.route("/export_inventory", methods=["GET"])
def export_inventory():
    ingredientList = db.session.query(Ingredient).all()

    data = []
    for ing in ingredientList:
        data.append({
            "Ingredient": ing.ingredientname,
            "Quantity": ing.availablequantity
        })

    
    df = pd.DataFrame(data)

    output = BytesIO()
    df.to_excel(output, index=False, engine="openpyxl")
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="ingredients.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


if __name__ == "__main__":
    app.run(debug=True)
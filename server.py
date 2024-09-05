from flask import request, jsonify, Flask
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from flask import send_file
import io
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///warehouse.db'
db = SQLAlchemy(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(20), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    sold = db.Column(db.String(20), nullable=False)
    dateOfLoad = db.Column(db.String(20), nullable=False)

class warehouse(db.Model):
    id = id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer,db.ForeignKey('product.id'),nullable=False)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = UserModel.query.filter_by(username=data['username'], password=data['password']).first()
    if user:
        return jsonify({'message': 'Login successful', 'role': user.role}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/addproduct', methods=['POST'])
def addproduct():
    data = request.json
    
    # Check if the product code already exists
    if Product.query.filter_by(code=data['productcode']).first():
        return jsonify({'message': 'Product code already exists'}), 400
    
    # Create a new product
    new_product = Product(
        code=data['productcode'],
        sold=data['sold'],
        dateOfLoad=data['dateofloading']
    )
    
    try:
        # Add the product to the database and commit to generate the ID
        db.session.add(new_product)
        db.session.commit()

        # If the product is not sold, add it to the warehouse
        if new_product.sold == '0':
            new_warehouse = warehouse(product_id=new_product.id)
            db.session.add(new_warehouse)
            db.session.commit()

        return jsonify({'message': 'Product added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500


@app.route('/deleteproduct', methods=['DELETE'])
def deleteproduct():
    data = request.json
    product_code = data.get('productcode')

    # Check if the product exists
    product = Product.query.filter_by(code=product_code).first()
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    try:
        # Check if the product exists in the warehouse table
        warehouse_entry = warehouse.query.filter_by(product_id=product.id).first()
        if warehouse_entry:
            # Delete the entry from the warehouse table
            db.session.delete(warehouse_entry)
        
        # Delete the product from the Product table
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({'message': 'Product and its warehouse entry deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

@app.route('/updateproduct', methods=['PUT'])
def editproduct():
    data = request.json
    product_code = data.get('productcode')

    # Check if the product exists
    product = Product.query.filter_by(code=product_code).first()
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    try:
        # If the product is being updated as sold and was previously unsold, remove it from the warehouse
        if product.sold == '0' and data.get('sold') != '0':
            warehouse_entry = warehouse.query.filter_by(product_id=product.id).first()
            if warehouse_entry:
                db.session.delete(warehouse_entry)

        # Update the product details
        product.sold = data.get('sold', product.sold)  # Update if provided, else keep existing
        product.dateOfLoad = data.get('dateofloading', product.dateOfLoad)  # Update if provided, else keep existing
        
        db.session.commit()
        return jsonify({'message': 'Product updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500


@app.route('/viewproduct', methods=['GET'])
def viewproduct():
    product_code = request.args.get('productcode')

    # Check if the product code is provided
    if not product_code:
        return jsonify({'message': 'Product code is required'}), 400

    # Retrieve the product with the given code
    product = Product.query.filter_by(code=product_code).first()
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    # Return the product details
    return jsonify({
        'productcode': product.code,
        'sold': product.sold,
        'dateofloading': product.dateOfLoad
    }), 200


@app.route('/adduser', methods=['POST'])
def adduser():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    # Check if the username already exists
    if UserModel.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400

    # Create a new user
    new_user = UserModel(
        username=username,
        password=password,
        role=role
    )

    # Add the user to the database
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

@app.route('/deleteuser', methods=['DELETE'])
def deleteuser():
    data = request.json
    username = data.get('username')

    # Check if the user exists
    user = UserModel.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Delete the user
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500
from flask import send_file
import io

@app.route('/exportwarehouse', methods=['GET'])
def export_warehouse():
    try:
        # Query the warehouse table to get all products available
        warehouse_entries = warehouse.query.all()

        # Prepare data for DataFrame
        data = []
        for entry in warehouse_entries:
            product = Product.query.get(entry.product_id)
            data.append({
                'Product Code': product.code,
                'Date of Loading': product.dateOfLoad
            })
        print(data)

        # Create a DataFrame
        df = pd.DataFrame(data)

        # Create a BytesIO buffer to hold the Excel file
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Warehouse Products')

        # Set buffer's current position to the start
        buffer.seek(0)

        # Send the file as a response
        return send_file(
            buffer,
            as_attachment=True,
            download_name='warehouse_products.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        ), 200
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)}), 500

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

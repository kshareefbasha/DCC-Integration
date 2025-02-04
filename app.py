from flask import Flask, jsonify, request, send_from_directory
import sqlite3
import os

app = Flask(__name__)

# Initialize the database
def init_db():
    try:
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL
        )
        ''')
        conn.commit()
        conn.close()
        print("Database initialized successfully.")
    except sqlite3.Error as e:
        print(f"Database initialization failed: {e}")

# Add an item to the inventory
def add_inventory_item(name, quantity):
    try:
        with sqlite3.connect('inventory.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO inventory (name, quantity) VALUES (?, ?)', (name, quantity))
            conn.commit()
    except sqlite3.Error as e:
        return str(e)
    return "Item added successfully!"

# Fetch all inventory items
def get_inventory_items():
    try:
        with sqlite3.connect('inventory.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT name, quantity FROM inventory')
            items = cursor.fetchall()

        # Convert items to a list of dictionaries
        inventory_list = [{"name": item[0], "quantity": item[1]} for item in items]
        return inventory_list
    except sqlite3.Error as e:
        return str(e)

@app.route('/')
def home():
    return "Welcome to the Inventory Management System! Use /inventory to view inventory and /add_item to add new items."

# Inventory management routes
@app.route('/inventory', methods=['GET'])
def get_inventory():
    items = get_inventory_items()
    if isinstance(items, list):
        return jsonify(items)
    else:
        return jsonify({"message": f"Error: {items}"}), 500

@app.route('/add_item', methods=['POST'])
def add_item():
    item_data = request.get_json()
    name = item_data.get('name')
    quantity = item_data.get('quantity')

    if name and isinstance(quantity, int) and quantity > 0:
        response = add_inventory_item(name, quantity)
        if "successfully" in response:
            return jsonify({"message": response}), 201
        else:
            return jsonify({"message": f"Error: {response}"}), 500
    return jsonify({"message": "Invalid data!"}), 400

# Helper function to generate detailed transformation response
def generate_transformation_response(transformation_type, data):
    # Detailed explanations for each transformation type
    explanations = {
        "translation": f"The object has been translated by {data.get('dx')} units along the x-axis, {data.get('dy')} units along the y-axis, and {data.get('dz')} units along the z-axis.",
        "rotation": f"The object has been rotated by {data.get('angle')} degrees around the {data.get('axis')} axis.",
        "scale": f"The object has been scaled by a factor of {data.get('scale_factor')} along the {data.get('axis')} axis.",
        "combined transformation": f"The object has undergone a combination of transformations: {data.get('translation')} for translation, {data.get('rotation')} for rotation, and {data.get('scaling')} for scaling."
    }
    
    # Explanation for the given transformation type
    explanation = explanations.get(transformation_type, "Unknown transformation type.")
    
    return jsonify({
        "status": "success",
        "transformation": transformation_type,
        "data": data,
        "explanation": explanation
    }), 200

# Transformation-related routes
@app.route('/translation', methods=['POST'])
def translation():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400
    print(f"Received translation data: {data}")  # Log the transformation
    return generate_transformation_response("translation", data)

@app.route('/rotation', methods=['POST'])
def rotation():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400
    print(f"Received rotation data: {data}")  # Log the transformation
    return generate_transformation_response("rotation", data)

@app.route('/scale', methods=['POST'])
def scale():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400
    print(f"Received scale data: {data}")  # Log the transformation
    return generate_transformation_response("scale", data)

@app.route('/transform', methods=['POST'])
def transform():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400
    print(f"Received full transform data: {data}")  # Log the transformation
    return generate_transformation_response("combined transformation", data)

# Route for favicon to prevent 404 errors
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

if __name__ == '__main__':
    init_db()  # Initialize the database when the server starts
    app.run(debug=True)

from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# SQLite database setup for inventory
def get_db_connection():
    conn = sqlite3.connect('inventory.db')
    conn.row_factory = sqlite3.Row
    return conn

# Inventory Management Routes
@app.route('/inventory/add', methods=['POST'])
def add_item():
    data = request.get_json()
    item_name = data.get('item_name')
    quantity = data.get('quantity')

    if not item_name or quantity is None:
        return jsonify({"status": "error", "message": "Missing item_name or quantity"}), 400

    conn = get_db_connection()
    conn.execute("INSERT INTO inventory (item_name, quantity) VALUES (?, ?)", (item_name, quantity))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": f"Item {item_name} added with quantity {quantity}"}), 201

@app.route('/inventory/update', methods=['POST'])
def update_item():
    data = request.get_json()
    item_name = data.get('item_name')
    new_quantity = data.get('new_quantity')

    if not item_name or new_quantity is None:
        return jsonify({"status": "error", "message": "Missing item_name or new_quantity"}), 400

    conn = get_db_connection()
    conn.execute("UPDATE inventory SET quantity = ? WHERE item_name = ?", (new_quantity, item_name))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": f"Quantity for {item_name} updated to {new_quantity}"}), 200

@app.route('/inventory/remove', methods=['POST'])
def remove_item():
    data = request.get_json()
    item_name = data.get('item_name')

    if not item_name:
        return jsonify({"status": "error", "message": "Missing item_name"}), 400

    conn = get_db_connection()
    conn.execute("DELETE FROM inventory WHERE item_name = ?", (item_name,))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": f"Item {item_name} removed"}), 200

@app.route('/inventory/purchase', methods=['POST'])
def purchase_item():
    data = request.get_json()
    item_name = data.get('item_name')
    quantity = data.get('quantity')

    if not item_name or quantity is None:
        return jsonify({"status": "error", "message": "Missing item_name or quantity"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT quantity FROM inventory WHERE item_name = ?", (item_name,))
    item = cur.fetchone()

    if not item:
        return jsonify({"status": "error", "message": f"Item {item_name} not found"}), 404

    current_quantity = item['quantity']
    if current_quantity < quantity:
        return jsonify({"status": "error", "message": f"Not enough stock for {item_name}"}), 400

    new_quantity = current_quantity - quantity
    conn.execute("UPDATE inventory SET quantity = ? WHERE item_name = ?", (new_quantity, item_name))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": f"Purchased {quantity} of {item_name}. New stock: {new_quantity}"}), 200

@app.route('/inventory/return', methods=['POST'])
def return_item():
    data = request.get_json()
    item_name = data.get('item_name')
    quantity = data.get('quantity')

    if not item_name or quantity is None:
        return jsonify({"status": "error", "message": "Missing item_name or quantity"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT quantity FROM inventory WHERE item_name = ?", (item_name,))
    item = cur.fetchone()

    if not item:
        return jsonify({"status": "error", "message": f"Item {item_name} not found"}), 404

    current_quantity = item['quantity']
    new_quantity = current_quantity + quantity
    conn.execute("UPDATE inventory SET quantity = ? WHERE item_name = ?", (new_quantity, item_name))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": f"Returned {quantity} of {item_name}. New stock: {new_quantity}"}), 200

# Transformation Routes
@app.route('/transform', methods=['POST'])
def transform():
    data = request.get_json()
    print(f"Received Transform data: {data}")
    return jsonify({"status": "success", "message": "All transformations applied successfully"}), 200

@app.route('/translation', methods=['POST'])
def translation():
    data = request.get_json()
    print(f"Received Translation data: {data}")
    return jsonify({"status": "success", "message": "Translation applied successfully"}), 200

@app.route('/rotation', methods=['POST'])
def rotation():
    data = request.get_json()
    print(f"Received Rotation data: {data}")
    return jsonify({"status": "success", "message": "Rotation applied successfully"}), 200

@app.route('/scale', methods=['POST'])
def scale():
    data = request.get_json()
    print(f"Received Scale data: {data}")
    return jsonify({"status": "success", "message": "Scale applied successfully"}), 200

@app.route('/file-path', methods=['POST'])
def file_path():
    data = request.get_json()
    file_path = data.get('file_path', '')
    print(f"Received File Path: {file_path}")
    return jsonify({"status": "success", "message": "File path received successfully", "file_path": file_path}), 200

# Initialize the database if it doesn't exist
def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            item_name TEXT PRIMARY KEY,
            quantity INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()  # Initialize database before starting the server
    app.run(debug=True, host='localhost', port=5000)

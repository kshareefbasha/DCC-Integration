from flask import Flask, request, jsonify
import sqlite3
import logging
import time

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

DATABASE = 'inventory.db'

# Initialize the database
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS inventory (name TEXT, quantity INTEGER)''')
    conn.commit()
    conn.close()

# Delay function to simulate the 10-second delay
def simulate_delay():
    time.sleep(10)

# Common log function for requests
def log_request(endpoint, data):
    logging.info(f"Request to {endpoint} with data: {data}")

# Routes for Transformations
@app.route('/transform', methods=['POST'])
def transform():
    data = request.json
    log_request('/transform', data)
    simulate_delay()
    return jsonify({"status": "success", "data": data}), 200

@app.route('/translation', methods=['POST'])
def translation():
    data = request.json
    log_request('/translation', data)
    simulate_delay()
    return jsonify({"status": "success", "position": data}), 200

@app.route('/rotation', methods=['POST'])
def rotation():
    data = request.json
    log_request('/rotation', data)
    simulate_delay()
    return jsonify({"status": "success", "rotation": data}), 200

@app.route('/scale', methods=['POST'])
def scale():
    data = request.json
    log_request('/scale', data)
    simulate_delay()
    return jsonify({"status": "success", "scale": data}), 200

# Routes for Inventory Management
@app.route('/add-item', methods=['POST'])
def add_item():
    data = request.json
    name = data.get('name')
    quantity = data.get('quantity')
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO inventory (name, quantity) VALUES (?, ?)", (name, quantity))
    conn.commit()
    conn.close()
    logging.info(f"Added item: {name}, Quantity: {quantity}")
    return jsonify({"status": "success", "item": name}), 200

@app.route('/remove-item', methods=['POST'])
def remove_item():
    data = request.json
    name = data.get('name')
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM inventory WHERE name = ?", (name,))
    conn.commit()
    conn.close()
    logging.info(f"Removed item: {name}")
    return jsonify({"status": "success", "item": name}), 200

@app.route('/inventory', methods=['GET'])
def get_inventory():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM inventory")
    items = c.fetchall()
    conn.close()
    logging.info(f"Fetched inventory: {items}")
    return jsonify(items), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

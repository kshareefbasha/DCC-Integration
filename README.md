# Blender-Flask-Inventory

This project integrates a Blender plugin with a Flask server for managing inventory data. The Flask server stores and manages items using an SQLite database, while the Blender plugin sends transformation data to the server. A PyQt5 UI allows users to interact with the inventory.

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-username/Blender-Flask-Inventory.git
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the Flask server:
   ```
   python flask_server/server.py
   ```

4. Install the Blender plugin by placing `plugin.py` in the Blender add-ons folder.

5. Run the PyQt UI:
   ```
   python inventory_ui/ui.py
   ```

## Project Structure
- `blender_plugin/` - Blender plugin code.
- `flask_server/` - Flask server and API code.
- `inventory_ui/` - PyQt UI for inventory management.

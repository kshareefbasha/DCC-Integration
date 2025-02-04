# Blender-Flask-Inventory 📦✨

Welcome to the **Blender-Flask-Inventory** project! This repository integrates a Blender plugin with a Flask server to manage inventory data and send transformation data from Blender. The project includes three main components:

## Project Components 🔧

### Blender Plugin 🎮
- **Transforms:** Position, Rotation, and Scale of the selected object.
- **Server Interaction:** Send data such as position/rotation/scale to the Flask server based on user selection.
- **UI:** A user-friendly panel in Blender to control transformations and submit data.

### Flask Server 🖥️
The Flask server manages all inventory-related operations and listens for incoming data from Blender. It stores inventory items in an SQLite database.

- **Endpoints:**
  - `/transform`: Receive position, rotation, and scale data.
  - `/translation`: Handle only position data.
  - `/rotation`: Handle only rotation data.
  - `/scale`: Handle only scale data.
  - `/add-item`: Add a new item to the inventory.
  - `/remove-item`: Remove an item from the inventory.
  - `/update-quantity`: Update the quantity of an item in the inventory.
  - `/file-path`: Get the path of the DCC file or project folder.

### PyQt UI 📱
The PyQt UI allows you to view and interact with the inventory, including adding, removing, and updating items and quantities.

---

## Setup Instructions 📦

### 1. Clone the Repository 🧑‍💻
Clone the repository to your local machine using the following command:

```bash
git clone https://github.com/kshareefbasha/Blender-Flask-Inventory.git
2. Install Dependencies 🔌
Make sure you have Python installed. Then, install the required dependencies using:

bash
Copy
Edit
pip install -r requirements.txt
This will install Flask, PyQt5, and other necessary libraries.

3. Run the Flask Server 🚀
Navigate to the flask_server directory and run the Flask server with:

bash
Copy
Edit
python flask_server/server.py
This will start the Flask server at http://localhost:5000.

4. Install the Blender Plugin 🖌️
Open Blender. Go to Edit > Preferences > Add-ons. Click Install and select the plugin.py file from the cloned repository. Enable the plugin by checking the box next to it in the Add-ons list.

5. Run the PyQt UI 🖥️
Navigate to the inventory_ui directory and run the UI with:

bash
Copy
Edit
python inventory_ui/ui.py
The PyQt UI will open, allowing you to interact with the inventory and perform actions like adding, removing, and updating items.

How to Use the Blender Plugin 🌟
Select an Object: In Blender, select an object whose transformation data you want to send to the server.
Choose Transformation Type: In the plugin panel, choose one of the following transformation types:
Translation: Send position data.
Rotation: Send rotation data.
Scale: Send scale data.
Transform: Send all transformation data (position, rotation, and scale).
Click "Send Transform Data": After selecting the transformation type, click the button to send the data to the Flask server.
Server Endpoints 🛠️
The Flask server exposes several endpoints to interact with the inventory and transformation data:

POST /transform: Sends all transformation data (position, rotation, scale).
POST /translation: Sends position data (x, y, z).
POST /rotation: Sends rotation data (x, y, z).
POST /scale: Sends scale data (x, y, z).
POST /add-item: Adds an item to the inventory (name, quantity).
POST /remove-item: Removes an item by name.
POST /update-quantity: Updates the quantity of an item by name.
GET /file-path: Returns the path of the DCC file or the project folder path.
Notes 📝
Delay: All server responses have a 10-second delay to simulate real-time processing.
Logging: The server logs all received requests in the terminal.
Contribution Guidelines 🚀
Feel free to contribute to this project! Here's how:

Fork the repository: Create a personal copy of the project.
Make changes: Work on your changes locally.
Submit a pull request: Once you're happy with your changes, submit a PR with a description of what was changed.
License 📄
This project is licensed under the MIT License. See the LICENSE file for more details.

Special Thanks 🙏
Blender: For providing an amazing 3D creation suite.
Flask: For creating a lightweight and easy-to-use web framework.
PyQt5: For offering a flexible UI framework.
SQLite: For providing a reliable database solution.
Blender-Flask-Inventory 📦✨
Welcome to the Blender-Flask-Inventory project! This repository integrates a Blender plugin with a Flask server to manage inventory data and send transformation data from Blender. The project includes three main components:

Blender Plugin: Sends object transformation data (position, rotation, scale) to the Flask server.
Flask Server: Manages inventory data stored in an SQLite database.
PyQt UI: A simple user interface to interact with the inventory and display item details.
Project Components 🔧
1. Blender Plugin 🎮
The plugin is a Blender add-on that allows you to interact with the Blender scene and send transformation data (e.g., position, rotation, scale) of selected objects to the Flask server.

Transforms: Position, Rotation, and Scale of the selected object.
Server Interaction: Send data such as position/rotation/scale to the Flask server based on user selection.
UI: An easy-to-use panel in Blender's UI to control transformations and submit data.
2. Flask Server 🖥️
The Flask server manages all inventory-related operations and listens for incoming data from Blender. The server uses SQLite to store inventory items and their quantities.

Endpoints:
/transform: Receive position, rotation, and scale data.
/translation: Handle position data only.
/rotation: Handle rotation data only.
/scale: Handle scale data only.
/add-item: Add a new item to the inventory.
/remove-item: Remove an item from the inventory.
/update-quantity: Update the quantity of an item in the inventory.
/file-path: Get the path of the DCC file or project folder.
3. PyQt UI 📱
The PyQt UI lets you view the current inventory, and update it by adding or removing items, as well as adjusting item quantities. The UI communicates with the Flask server to reflect these changes.

📦 Setup Instructions
Follow these simple steps to get the project up and running:

1. Clone the Repository 🧑‍💻
Clone the project to your local machine using the command:

bash
Copy
Edit
git clone https://github.com/kshareefbasha/Blender-Transform-Data-Sender-Plugin.git
2. Install Dependencies 🔌
Make sure you have Python installed. Then, install the required dependencies using the command:

bash
Copy
Edit
pip install -r requirements.txt
This will install Flask, PyQt5, and other necessary libraries.

3. Run the Flask Server 🚀
To start the Flask server, navigate to the flask_server directory and run the server:

bash
Copy
Edit
python flask_server/server.py
This will start the Flask server on http://localhost:5000.

4. Install the Blender Plugin 🖌️
Open Blender.
Go to Edit > Preferences > Add-ons.
Click Install and select the plugin.py file from the cloned repository.
Enable the add-on by checking the box next to the plugin in the add-ons list.
5. Run the PyQt UI 🖥️
Navigate to the inventory_ui directory and run the UI:

bash
Copy
Edit
python inventory_ui/ui.py
The UI will open, allowing you to interact with the inventory and perform actions like adding, removing, and updating items.

🌟 How to Use the Blender Plugin
Select an Object: In Blender, select an object whose transformation data you want to send to the server.
Choose Transformation Type: In the plugin panel, select one of the following server functions:
Translation: Send position data.
Rotation: Send rotation data.
Scale: Send scale data.
Transform: Send all transformation data (position, rotation, and scale).
Click "Send Transform Data": After selecting the transformation type, click the button to send the data to the Flask server.
🛠️ Server Endpoints
The Flask server exposes several endpoints to interact with the inventory and transformation data. Here’s a quick rundown:

POST /transform: Sends all transformation data (position, rotation, scale).
POST /translation: Sends only position data (x, y, z).
POST /rotation: Sends only rotation data (x, y, z).
POST /scale: Sends only scale data (x, y, z).
POST /add-item: Adds an item to the inventory (name, quantity).
POST /remove-item: Removes an item by name.
POST /update-quantity: Updates the quantity of an item by name.
GET /file-path: Returns the path of the DCC file or the project folder path.
🛑 Notes
Delay: All server responses have a 10-second delay to simulate real-time processing.
Logging: The server logs all received requests in the terminal.
🚀 Contribution Guidelines
Feel free to contribute to this project! Here's how:

Fork the repository: Create a personal copy of the project.
Make changes: Work on your changes locally.
Submit a pull request: Once you’re happy with your changes, submit a PR with a description of what was changed.
📄 License
This project is licensed under the MIT License. See the LICENSE file for more details.

🙏 Special Thanks
Blender: For providing a powerful 3D creation suite.
Flask: For creating an amazing lightweight web framework.
PyQt5: For providing a flexible UI framework.
SQLite: For being a reliable database solution.

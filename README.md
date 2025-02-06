# Blender-Transform-Data-Sender-Plugin

This project integrates **Blender** with a **Flask server** to send object transformation data (position, rotation, scale) from Blender to a web server. It also manages inventory items using a **PyQt5** graphical interface and stores data in an **SQLite** database.

By running the project, you will be able to:
- Send object transformation data from Blender to a server.
- View and manage inventory data using an easy-to-use interface.
- Have a running web server to store and retrieve object transformations and inventory items.

---

## 🛠️ How This Project Works

### **1. Blender Plugin**
The plugin sends 3D object transformation data from Blender to a Flask server. When you select a 3D object in Blender and change its position, rotation, or scale, the plugin sends that data to the server for processing.

#### Output
- When the transformation data is sent, it will be stored in the server and can be accessed through the Flask API.
- The **Flask server** then stores this data in the SQLite database and returns a success message.

### **2. Flask Server**
The Flask server listens for incoming requests from the Blender plugin. Once it receives transformation data (position, rotation, or scale), it processes that data and stores it in an **SQLite database**. It also manages inventory items by handling various API endpoints.

#### Output
- **Stored Data**: The transformation data (position, rotation, and scale) will be saved to the SQLite database.
- **Inventory**: The server stores inventory items in the database. This data can be viewed and managed through the **Inventory UI**.

### **3. Inventory UI (User Interface)**
The **PyQt5 UI** provides a graphical interface for managing inventory items. You can view, add, or update inventory data, which is stored in the SQLite database. This interface is simple and user-friendly for anyone interacting with the project.

#### Output
- **Inventory Management**: When you run the Inventory UI, you can add, update, or view inventory items stored in the SQLite database.
- The changes are reflected immediately in the interface.

---

## 🧰 What You’ll Need

- **Python**: Python 3.x installed on your computer.
- **Blender**: Version 2.8 or higher.
- **SQLite**: A lightweight database that will be used to store inventory data.
- **Git** :git is used for version control
---

## 🔧 Setup Instructions

### **1. Clone the Project**

First, download the project to your computer by cloning the GitHub repository:


git clone https://github.com/kshareefbasha/Blender-Transform-Data-Sender-Plugin.git
cd Blender-Transform-Data-Sender-Plugin
2. Install Dependencies
Make sure you have Python installed. Then, install the necessary libraries that the project uses:


pip install -r requirements.txt
This will install libraries like Flask, SQLite, and PyQt5 needed to run the project.

3. Run the Flask Server
The Flask server listens for data from Blender. To start the server, run this command:

python flask_server/server.py
The server will run locally and listen on a specified port (usually http://127.0.0.1:5000). It will process requests from Blender and store the data in the database.

🎨 How to Use the Blender Plugin
1. Install the Plugin in Blender
Download the plugin.py file from the project.
Place it in your Blender add-ons folder:
Windows: C:\Users\<YourUsername>\AppData\Roaming\Blender Foundation\Blender\<version>\scripts\addons
Mac: /Users/<YourUsername>/Library/Application Support/Blender/<version>/scripts/addons
Linux: /home/<YourUsername>/.config/blender/<version>/scripts/addons
2. Enable the Plugin in Blender
Open Blender, go to Edit > Preferences > Add-ons.
Click Install, select plugin.py, and click Install Add-on.
Enable the add-on by checking the box next to it.
3. Using the Plugin
Open a Blender project and select a 3D object.
Choose a transformation (move, rotate, or scale) from the dropdown menu.
Click Send Transform Data to send the data (position, rotation, scale) to the Flask server.
🖥️ Managing Inventory with the PyQt5 UI
To interact with the inventory, you need to run the Inventory UI.

To Run the Inventory UI:
Navigate to the inventory_ui folder.
Run the following command:
python inventory_ui/ui.py
What You Can Do in the UI:
View Inventory: The UI will show a list of all inventory items stored in the database.
Add New Items: Add new inventory items by filling in the form in the UI.
Update Existing Items: Modify existing items in the database.
Output
Inventory Items: You will see a list of all inventory items along with their details.
Any changes (adding or updating inventory items) will be reflected in the database immediately.


📂 Project Folder Structure
Here’s a breakdown of the files and folders in this project:

Blender-Transform-Data-Sender-Plugin/
│
├── blender_plugin/            # Blender plugin files
│   └── plugin.py              # Plugin that sends data to the server
│
├── flask_server/              # Files for the web server
│   └── server.py              # Web server that stores data
│
├── inventory_ui/              # User interface for managing inventory
│   └── ui.py                  # Code for the inventory UI
│
├── requirements.txt           # List of libraries used in the project
└── README.md                  # This file (you’re reading it!)

🛠️ Technologies Used
Blender API (Python): Used to interact with Blender and manipulate 3D objects.
Flask: A Python web framework that allows the server to communicate with Blender and manage inventory.
SQLite: A lightweight database used to store inventory data.
PyQt5: A Python library for creating the graphical interface to manage inventory.
🤝 How to Contribute
We welcome anyone who wants to help improve the project! Here’s how you can contribute:

Fork the repository to your GitHub account.
Create a new branch: git checkout -b feature/YourFeature
Make changes and commit them: git commit -m 'Add a feature'
Push the changes to your fork: git push origin feature/YourFeature
Submit a pull request to propose your changes.
📜 License
This project is licensed under the MIT License. You can freely use, modify, and distribute the code.

🔗 Connect with Me
LinkedIn
GitHub
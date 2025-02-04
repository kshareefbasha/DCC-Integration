from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QLabel
from PyQt5.QtCore import QThread, pyqtSignal
import requests
import sys

class Worker(QThread):
    result_signal = pyqtSignal(list)  # Keep it as list

    def run(self):
        response = requests.get('http://localhost:5000/inventory')
        try:
            data = response.json()
            if isinstance(data, list):
                self.result_signal.emit(data)  # Emit the list of items
            else:
                print("Invalid response format: Expected a list")
        except ValueError:
            print("Error decoding JSON response from the server.")

class InventoryUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventory Management")
        self.layout = QVBoxLayout()

        # Create the fields for adding a new item
        self.name_label = QLabel("Item Name:")
        self.layout.addWidget(self.name_label)
        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_input)

        self.quantity_label = QLabel("Quantity:")
        self.layout.addWidget(self.quantity_label)
        self.quantity_input = QLineEdit()
        self.layout.addWidget(self.quantity_input)

        # Create a button to add the item
        self.add_button = QPushButton("Add Item")
        self.add_button.clicked.connect(self.add_item)
        self.layout.addWidget(self.add_button)

        # Create a button to return the item
        self.return_button = QPushButton("Return Item")
        self.return_button.clicked.connect(self.return_item)
        self.layout.addWidget(self.return_button)

        # Create the refresh button
        self.refresh_button = QPushButton("Refresh Inventory")
        self.refresh_button.clicked.connect(self.fetch_inventory)
        self.layout.addWidget(self.refresh_button)

        # Create the table to display the inventory
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)
        self.fetch_inventory()

    def fetch_inventory(self):
        self.worker = Worker()
        self.worker.result_signal.connect(self.update_table)
        self.worker.start()

    def update_table(self, inventory_data):
        if isinstance(inventory_data, list):  # Ensure data is a list
            self.table.setRowCount(len(inventory_data))
            self.table.setColumnCount(2)
            self.table.setHorizontalHeaderLabels(['Item Name', 'Quantity'])

            for row, item in enumerate(inventory_data):
                # Make sure each item is a dictionary with 'name' and 'quantity'
                if isinstance(item, dict) and 'name' in item and 'quantity' in item:
                    self.table.setItem(row, 0, QTableWidgetItem(item['name']))
                    self.table.setItem(row, 1, QTableWidgetItem(str(item['quantity'])))
                else:
                    print(f"Invalid item format: {item}")
        else:
            print("Invalid data format received:", inventory_data)

    def add_item(self):
        name = self.name_input.text()
        quantity = self.quantity_input.text()

        # Validate the input
        if name and quantity.isdigit():
            quantity = int(quantity)
            # Send the new item data to the server
            response = requests.post('http://localhost:5000/add_item', json={'name': name, 'quantity': quantity})

            if response.status_code == 201:
                print("Item added successfully!")
                self.fetch_inventory()  # Refresh the inventory table
                self.name_input.clear()
                self.quantity_input.clear()
            else:
                print("Failed to add item.")
        else:
            print("Invalid input!")

    def return_item(self):
        name = self.name_input.text()
        quantity = self.quantity_input.text()

        # Validate the input for returning item
        if name and quantity.isdigit():
            quantity = int(quantity)

            # Send a request to update the quantity or remove the item
            # Assuming we're reducing the item quantity here
            response = requests.post('http://localhost:5000/update-quantity', json={'name': name, 'quantity': -quantity})

            if response.status_code == 200:
                print("Item returned successfully!")
                self.fetch_inventory()  # Refresh the inventory table
                self.name_input.clear()
                self.quantity_input.clear()
            else:
                print("Failed to return item.")
        else:
            print("Invalid input!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = InventoryUI()
    window.show()
    sys.exit(app.exec_())

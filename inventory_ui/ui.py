import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QInputDialog
)

class InventoryManagementApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Inventory Management")
        self.setGeometry(100, 100, 600, 400)

        self.conn = sqlite3.connect("inventory.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        # Main Layout
        main_layout = QVBoxLayout()

        # Inventory Management Section (Buttons)
        inventory_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Item")
        self.remove_button = QPushButton("Remove Item")
        self.update_button = QPushButton("Update Quantity")
        self.purchase_button = QPushButton("Purchase")
        self.return_button = QPushButton("Return")

        # Connect buttons to respective functions
        self.add_button.clicked.connect(self.add_item_dialog)
        self.remove_button.clicked.connect(self.remove_item_dialog)
        self.update_button.clicked.connect(self.update_quantity_dialog)
        self.purchase_button.clicked.connect(self.purchase_item_dialog)
        self.return_button.clicked.connect(self.return_item_dialog)

        inventory_layout.addWidget(self.add_button)
        inventory_layout.addWidget(self.remove_button)
        inventory_layout.addWidget(self.update_button)
        inventory_layout.addWidget(self.purchase_button)
        inventory_layout.addWidget(self.return_button)
        main_layout.addLayout(inventory_layout)

        # Inventory Table
        self.inventory_table = QTableWidget(0, 2)
        self.inventory_table.setHorizontalHeaderLabels(["Item Name", "Quantity"])
        self.inventory_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.inventory_table)

        self.load_inventory()
        self.setLayout(main_layout)

    def create_table(self):
        """Creates the inventory database table if it doesn't exist."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                item_name TEXT PRIMARY KEY,
                quantity INTEGER NOT NULL
            )
        """)
        self.conn.commit()

    def load_inventory(self):
        """Loads inventory items from the database into the table."""
        self.inventory_table.setRowCount(0)
        self.cursor.execute("SELECT * FROM inventory")
        for row_position, (item_name, quantity) in enumerate(self.cursor.fetchall()):
            self.inventory_table.insertRow(row_position)
            self.inventory_table.setItem(row_position, 0, QTableWidgetItem(item_name))
            self.inventory_table.setItem(row_position, 1, QTableWidgetItem(str(quantity)))

    def add_item(self, item_name, quantity):
        """Adds a new item to the inventory."""
        try:
            self.cursor.execute("INSERT INTO inventory (item_name, quantity) VALUES (?, ?)", (item_name, quantity))
            self.conn.commit()
            self.load_inventory()
        except sqlite3.IntegrityError:
            self.show_error("Item already exists!")

    def update_quantity(self, item_name, new_quantity):
        """Updates the quantity of an existing inventory item."""
        self.cursor.execute("UPDATE inventory SET quantity = ? WHERE item_name = ?", (new_quantity, item_name))
        self.conn.commit()
        self.load_inventory()

    def remove_item(self, item_name):
        """Removes an item from the inventory."""
        self.cursor.execute("DELETE FROM inventory WHERE item_name = ?", (item_name,))
        self.conn.commit()
        self.load_inventory()

    def purchase_item(self, item_name, purchase_quantity):
        """Handles item purchases by reducing stock quantity."""
        self.cursor.execute("SELECT quantity FROM inventory WHERE item_name = ?", (item_name,))
        result = self.cursor.fetchone()
        if result and result[0] >= purchase_quantity:
            new_quantity = result[0] - purchase_quantity
            self.update_quantity(item_name, new_quantity)
        else:
            self.show_error("Insufficient stock or item not found!")

    def return_item(self, item_name, return_quantity):
        """Handles item returns by increasing stock quantity."""
        self.cursor.execute("SELECT quantity FROM inventory WHERE item_name = ?", (item_name,))
        result = self.cursor.fetchone()
        if result:
            new_quantity = result[0] + return_quantity
            self.update_quantity(item_name, new_quantity)
        else:
            self.add_item(item_name, return_quantity)

    def show_error(self, message):
        """Displays an error message box."""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.exec_()

    # Dialogs for user input
    def add_item_dialog(self):
        item_name, ok1 = QInputDialog.getText(self, "Add Item", "Enter item name:")
        if ok1 and item_name:
            quantity, ok2 = QInputDialog.getInt(self, "Add Item", "Enter quantity:", 1, 1, 1000)
            if ok2:
                self.add_item(item_name, quantity)

    def remove_item_dialog(self):
        item_name, ok = QInputDialog.getText(self, "Remove Item", "Enter item name to remove:")
        if ok and item_name:
            self.remove_item(item_name)

    def update_quantity_dialog(self):
        item_name, ok1 = QInputDialog.getText(self, "Update Quantity", "Enter item name:")
        if ok1 and item_name:
            quantity, ok2 = QInputDialog.getInt(self, "Update Quantity", "Enter new quantity:", 1, 1, 1000)
            if ok2:
                self.update_quantity(item_name, quantity)

    def purchase_item_dialog(self):
        item_name, ok1 = QInputDialog.getText(self, "Purchase Item", "Enter item name:")
        if ok1 and item_name:
            quantity, ok2 = QInputDialog.getInt(self, "Purchase Item", "Enter purchase quantity:", 1, 1, 1000)
            if ok2:
                self.purchase_item(item_name, quantity)

    def return_item_dialog(self):
        item_name, ok1 = QInputDialog.getText(self, "Return Item", "Enter item name:")
        if ok1 and item_name:
            quantity, ok2 = QInputDialog.getInt(self, "Return Item", "Enter return quantity:", 1, 1, 1000)
            if ok2:
                self.return_item(item_name, quantity)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventoryManagementApp()
    window.show()
    sys.exit(app.exec_())

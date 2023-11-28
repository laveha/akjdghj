import hashlib
import sqlite3
from datetime import datetime

class WarehouseManagementSystem:
    def __init__(self, db_name='warehouse.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        queries = [
            '''
            CREATE TABLE IF NOT EXISTS Products (
                product_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL
            )
            ''',
            '''
            CREATE TABLE IF NOT EXISTS Suppliers (
                supplier_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                contact_person TEXT,
                contact_number TEXT
            )
            ''',
            '''
            CREATE TABLE IF NOT EXISTS SupplyOrders (
                order_id INTEGER PRIMARY KEY,
                product_id INTEGER,
                supplier_id INTEGER,
                order_date TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                status TEXT DEFAULT 'Pending',
                FOREIGN KEY (product_id) REFERENCES Products (product_id),
                FOREIGN KEY (supplier_id) REFERENCES Suppliers (supplier_id)
            )
            '''
        ]

        for query in queries:
            self.execute_query(query)

    def execute_query(self, query, params=None):
        with self.conn:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

    def _validate_input(self, *args):
        if any(arg is None or arg == "" for arg in args):
            print("Invalid input. All fields are required.")
            return False
        return True

    def add_product(self, name, price, quantity):
        if not self._validate_input(name, price, quantity):
            print("Invalid input. Product name, price, and quantity are required.")
            return

        query = 'INSERT INTO Products (name, price, quantity) VALUES (?, ?, ?)'
        params = (name, price, quantity)
        self.execute_query(query, params)

    def add_supplier(self, name, contact_person=None, contact_number=None):
        if not self._validate_input(name):
            print("Invalid input. Supplier name is required.")
            return

        query = 'INSERT INTO Suppliers (name, contact_person, contact_number) VALUES (?, ?, ?)'
        params = (name, contact_person, contact_number)
        self.execute_query(query, params)

    def place_supply_order(self, product_id, supplier_id, quantity):
        if not self._validate_input(product_id, supplier_id, quantity):
            print("Invalid input. Product ID, Supplier ID, and quantity are required.")
            return

        order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = 'INSERT INTO SupplyOrders (product_id, supplier_id, order_date, quantity) VALUES (?, ?, ?, ?)'
        params = (product_id, supplier_id, order_date, quantity)
        self.execute_query(query, params)

    def update_product_quantity(self, product_id, new_quantity):
        if not self._validate_input(product_id, new_quantity):
            print("Invalid input. Product ID and new quantity are required.")
            return

        query = 'UPDATE Products SET quantity = ? WHERE product_id = ?'
        params = (new_quantity, product_id)
        self.execute_query(query, params)

    def view_products(self):
        query = 'SELECT * FROM Products'
        return self.execute_query(query)

    def view_suppliers(self):
        query = 'SELECT * FROM Suppliers'
        return self.execute_query(query)

    def view_supply_orders(self):
        query = 'SELECT * FROM SupplyOrders'
        return self.execute_query(query)

warehouse_system = WarehouseManagementSystem()
warehouse_system.add_product("Laptop", 1200.00, 50)
warehouse_system.add_product("Printer", 300.00, 30)
warehouse_system.add_supplier("Tech Supplier", "John Smith", "123-456-7890")
warehouse_system.place_supply_order(1, 1, 20)
warehouse_system.place_supply_order(2, 1, 15)
warehouse_system.update_product_quantity(1, 70)

print("Products:")
print(warehouse_system.view_products())
print("\nSuppliers:")
print(warehouse_system.view_suppliers())
print("\nSupply Orders:")
print(warehouse_system.view_supply_orders())
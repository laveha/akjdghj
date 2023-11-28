import hashlib

class Supplier:
    def __init__(self, supplier_id, name, contact_person=None, contact_number=None):
        self._supplier_id = supplier_id
        self._name = name
        self._contact_person = contact_person
        self._contact_number = contact_number

    @property
    def supplier_id(self):
        return self._supplier_id

    @property
    def name(self):
        return self._name

    @property
    def contact_person(self):
        return self._contact_person

    @property
    def contact_number(self):
        return self._contact_number


class Product:
    def __init__(self, product_id, name, price, quantity):
        self._product_id = product_id
        self._name = name
        self._price = price
        self._quantity = quantity

    @property
    def product_id(self):
        return self._product_id

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @property
    def quantity(self):
        return self._quantity


class SupplyOrder:
    def __init__(self, order_id, product_id, supplier_id, order_date, quantity, status='Pending'):
        self._order_id = order_id
        self._product_id = product_id
        self._supplier_id = supplier_id
        self._order_date = order_date
        self._quantity = quantity
        self._status = status

    @property
    def order_id(self):
        return self._order_id

    @property
    def product_id(self):
        return self._product_id

    @property
    def supplier_id(self):
        return self._supplier_id

    @property
    def order_date(self):
        return self._order_date

    @property
    def quantity(self):
        return self._quantity

    @property
    def status(self):
        return self._status
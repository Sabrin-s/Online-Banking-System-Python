# backend.py
class Customer:
    def __init__(self, name, customer_id, password):
        self.name = name
        self.customer_id = customer_id
        self.__password = password
        self.account = None

    def verify_password(self, password):
        return self.__password == password


class Account:
    def __init__(self, acc_number, balance=0):
        self.acc_number = acc_number
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def transfer(self, other_account, amount):
        if self.withdraw(amount):
            other_account.deposit(amount)
            return True
        return False


class BankSystem:
    def __init__(self):
        self.customers = {}

    def add_customer(self, name, customer_id, password):
        if customer_id not in self.customers:
            customer = Customer(name, customer_id, password)
            customer.account = Account(customer_id + "ACC")
            self.customers[customer_id] = customer
            return True
        return False

    def login(self, customer_id, password):
        customer = self.customers.get(customer_id)
        if customer and customer.verify_password(password):
            return customer
        return None

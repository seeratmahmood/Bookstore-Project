from abc import ABC, abstractmethod
import re
import threading
import time

data_lock = threading.Lock()   # ---- creating a lock


class Bookstore(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def search_books(self, query):
        pass

    @abstractmethod
    def list_books(self):
        pass

    @abstractmethod
    def view_book_info(self, isbn):
        pass

    @abstractmethod
    def add_to_basket(self, email, isbn, quantity):
        pass

    @abstractmethod
    def view_basket(self, email):
        pass

    @abstractmethod
    def modify_basket(self, email, isbn, new_quantity):
        pass

    @abstractmethod
    def proceed_checkout(self, email):
        pass


class Books:
    def __init__(self, isbn, title, author, price, quantity):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.price = price
        self.quantity = quantity
        self.book_inventory = {
            "1234567890": {
                "Title": "Harry Potter and The Chamber of Secrets",
                "Author": "J.K Rowling",
                "Price": 10.00,
                "Quantity": 10
            },
            "1234567891": {
                "Title": "Harry Potter and The Philosopher's Stone",
                "Author": "J.K Rowling",
                "Price": 15.00,
                "Quantity": 20
            }
        }

    def add_book(self):
        def create_book():
            isbn = input("Enter ISBN: ")
            # --- check if book already exists using ISBN
            if isbn in self.book_inventory[isbn]:
                print(f"Book with ISBN{isbn} already exists in inventory.")
                return      # ----- stops execution if ISBN exists

            title = input("Enter Title: ")
            author = input("Enter Author: ")
            price = input("Enter Price: ")
            quantity = input("Enter Quantity: ")

            try:
                price = float(price)
                quantity = int(quantity)
                # --------- validate input to add books to inventory
                if price < 0 or quantity < 0:
                    print(f"Price and Quantity must not be negative values.")
                else:
                    self.book_inventory[isbn] = {
                        "Title": title,
                        "Author": author,
                        "Price": price,
                        "Quantity": quantity
                    }
                    return print(f"Book added successfully!")
            except ValueError:
                print("Invalid input for price or quantity. Please enter numeric values.")
        return create_book

    def view_book_info(self, title_or_isbn):  # --- View by Title or ISBN
        found = False
        for isbn, book in self.book_inventory.items():
            if title_or_isbn.lower() in book['Title'].lower() or title_or_isbn == isbn:
                found = True
                print("Book Information:")
                print(f"Title: {book['Title']}")
                print(f"Author: {book['Author']}")
                print(f"Price: {book['Price']}")
                print(f"Quantity: {book['Quantity']}")
        if not found:
            print("Book not found.")

    def list_books(self):
        print("List of Books:")
        for isbn, book in self.book_inventory.items():
            print(f"ISBN: {isbn} | Title: {book['Title']}")

    def search_books(self, title_or_isbn):
        print(f"Search Results for '{title_or_isbn}':")
        found = False
        for isbn, book in self.book_inventory.items():
            if title_or_isbn.lower() in book['Title'].lower() or title_or_isbn == isbn:
                print(f"ISBN: {isbn}")
                print(f"Title: {book['Title']}")
                print(f"Author: {book['Author']}")
                print(f"Price: {book['Price']}")
                print(f"Quantity: {book['Quantity']}")
                print("-" * 20)  # -- Separator between books
                found = True
        if not found:
            print("No matching books found.")

    def load_books_inventory(self):
        try:
            with open('books.csv', 'r') as csvfile:  # Use the known filename 'books.csv'
                reader = csv.DictReader(csvfile)
                for row in reader:
                    isbn, title, author, price_str, quantity_str = row
                    self.book_inventory[isbn] = {
                        "Title": title,
                        "Author": author,
                        "Price": float(price_str.replace('£', '').strip()),
                        "Quantity": int(quantity_str)
                    }
            return True
        except FileNotFoundError:
            return False

    def save_books_inventory(self):
        with open('books.csv', 'r', newline='') as csvfile:
            fieldnames = ["ISBN", "Title", "Author", "Price", "Quantity"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for isbn, book in self.book_inventory.items():
                writer.writerow({
                    "ISBN": isbn,
                    "Title": book["Title"],
                    "Author": book["Author"],
                    "Price": book["Price"],
                    "Quantity": book["Quantity"]
                })


# Parent Class
class Users(Books):
    def __init__(self, first_name, last_name, email, password):
        super().__init__(None, None, None, None, None)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.__password = password
        self.user_basket = {
            "swoodson@gmail.com": {
                "ISBN": "1234567891",
                "Title": "Harry Potter and The Philosopher's Stone",
                "Quantity": 5
            },
            "cbass@gmail.com": {
                "ISBN": "1234567890",
                "Title": "Harry Potter and The Chamber of Secrets",
                "Quantity": 5
            }
        }
        self.user_accounts = {
            "swoodson@gmail.com": {
                "First Name": "Serena",
                "Last Name": "Woodson",
                "Password": "password123"
            },
            "cbass@gmail.com": {
                "First Name": "Chuck",
                "Last Name": "Bass",
                "Password": "password123@"
            }
        }

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        if any(char in "!@#$%^&*/" for char in password) and any(char.isdigit() for char in password):
            self.__password = password
        else:
            raise ValueError("Password must contain at least one number and one special character: !@#$%^&*/")

    def add_to_basket(self, isbn, quantity):
        book = self.book_inventory.get(isbn)
        if not book:
            return "Book not found"
        available_quantity = book['Quantity']
        if quantity > available_quantity:
            return "Insufficient stock."
        if self.email not in self.user_basket:
            self.user_basket[self.email] = {}
        if isbn in self.user_basket[self.email]:
            self.user_basket[self.email][isbn]['Quantity'] += quantity
        else:
            self.user_basket[self.email][isbn] = {
                'Title': book['Title'],
                'Price': book['Price'],
                'Quantity': quantity
            }
        return "Item(s) added to the basket"

    def view_basket(self, email):
        if email in self.user_basket:
            item = self.user_basket[email]
            print("Your Basket:")
            print(f"ISBN: {item['ISBN']}")
            print(f"Title: {item['Title']}")
            print(f"Quantity: {item['Quantity']}")
            print("-" * 20)  # Separator between items
        else:
            print("Email not found or basket is empty.")

    def modify_basket(self, email, isbn, new_quantity):
        if email in self.user_basket and isbn in self.user_basket[email]:
            book = self.book_inventory.get(isbn)
            if not book:
                return f"Book not found"
            available_quantity = book['Quantity']
            if new_quantity > available_quantity:
                return "Insufficient Stock"
            self.user_basket[email][isbn]['Quantity'] = new_quantity
            return "Basket updated"
        else:
            return "Item not found in the basket"

    def proceed_checkout(self, email):
        if email in self.user_basket and self.user_basket[email]:
            total_price = 0  # ----------Calculate the total price for items in the basket

            def checkout_thread():
                nonlocal total_price
                for email, item in self.user_basket.items():
                    if item['ISBN'] in self.book_inventory:
                        item_price = self.book_inventory[item['ISBN']]['Price']
                        total_price += item['Quantity'] * item_price
                    else:
                        print(f"Warning: Item with ISBN {item['ISBN']} not found in inventory.")

            checkout_thread = threading.Thread(target=checkout_thread)
            checkout_thread.start()
            checkout_thread.join()

            with data_lock:     # ----- using lock as a context manager
                for email, item in self.user_basket.items():
                    if item['ISBN'] in self.book_inventory:
                        inventory_item = self.book_inventory[item['ISBN']]
                        inventory_item['Quantity'] -= item['Quantity']
                self.user_basket[email] = {}
                return f"Checkout successful. Total price: £{total_price:.2f}"
        else:
            return "Basket is empty."

    def valid_password(self, password):
        if any(char in "!@#$%^&*/" for char in password) and any(char.isdigit() for char in password):
            self.__password = password
            return True
        else:
            print("Password must contain at least one number and one special character: !@#$%^&*/")
            return False

    def register_user(self):
        def create_user():  # ----- closure function, encapsulates user registration process
            first_name = input("First Name: ")
            last_name = input("Last Name: ")
            email = input("Enter Email Address: ")
            if email in self.user_accounts:  # Check if the email already exists in user_accounts
                print("Email already exists. Please log in.")
                return False
            password = input("Create a Password: ")  # Check if the password meets the criteria
            if not self.valid_password(password):
                return False
            self.user_accounts[email] = {  # Add the new user to user_accounts
                "First Name": first_name,
                "Last Name": last_name,
                "Password": password
            }
            print("Registration successful. Continue to Login.")
            return True
        return create_user


# Child class of Users
class RegisteredUsers(Users):
    def __init__(self, first_name, last_name, email, password):
        super().__init__(first_name, last_name, email, password)
        self.orders = {
            "swoodson@gmail.com": [
                {
                    "Order ID": 1234,
                    "Title": "Harry Potter and The Philosopher's Stone",
                    "Quantity": 5
                }
            ],
            "cbass@gmail.com": [
                {
                    "Order ID": 2234,
                    "Title": "Harry Potter and The Chamber of Secrets",
                    "Quantity": 3
                }
            ]
        }

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        if any(char in "!@#$%^&*/" for char in password) and any(char.isdigit() for char in password):
            self.__password = password
        else:
            raise ValueError("Password must contain at least one number and one special character: !@#$%^&*/")

    def login(self):
        email = input("Enter Email: ")
        password = input("Enter Password: ")
        if email == self.email and password == self.password:
            return f"Login successful!"
        else:
            return "Email or password is invalid. Please try again."

    def order_history(self, email):
        if email in self.orders:
            order_info = self.orders[email]
            for order in order_info:
                print(f"Order ID: {order['Order ID']}")
                print(f"Title: {order['Title']}")
                print(f"Quantity: {order['Quantity']}")
                print("-" * 20)
            else:
                return "No order history found for this user."
        else:
            return "Invalid email or password."

    def view_account_details(self, email, password):
        if email in self.user_accounts and self.user_accounts[email]["Password"] == password:
            account_details = self.user_accounts[email]
            print(f"Email: {email}")
            print(f"First Name: {account_details['First Name']}")
            print(f"Last Name: {account_details['Last Name']}")
            print(f"Password: {account_details['Password']}")
            return account_details
        else:
            return "User not found or incorrect password"

    def modify_account_details(self, email, new_first_name, new_last_name, new_email, new_password):
        if email in self.user_accounts:  # Check if the user is logged in
            self.user_accounts[email] = {  # Update the user's account details
                "First Name": new_first_name,
                "Last Name": new_last_name,
                "Email": new_email,
                "Password": new_password
            }
            print("Account details have been successfully modified!")
            print("Updated Account Details:")
            for key, value in self.user_accounts[email].items():
                print(f"{key}: {value}")
        else:
            print("You are not logged in. Please log in to modify your account details.")

    def purchase_books(self):
        if self.user_basket:
            total_price = 0

            def purchase_thread():    # ---- threading
                nonlocal total_price
                for isbn, item in self.user_basket.items():
                    purchase = self.book_inventory.get(isbn)
                    if not purchase:
                        return f"Book not found"
                    continue
                available_quantity = book['Quantity']
                if item['Quantity'] <= available_quantity:
                    item_price = float(item['Price'].replace('£', '').strip())
                    total_price += item['Quantity'] * item_price
                    # Reduce the available quantity in the inventory
                    self.book_inventory[isbn]['Quantity'] -= item['Quantity']
                else:
                    print(f"This book is out of stock: ISBN {isbn}")

            purchase_thread = threading.Thread(target=purchase_thread)
            purchase_thread.start()
            purchase_thread.join()

            self.user_basket = {}
            if total_price == 0:
                return "Basket is empty"
            else:
                return f"Payment Successful! Total price: £{total_price:.2f}"

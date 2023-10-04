
# file = open(r'C:\Users\smahmood\Desktop\Python\books.csv', 'x')
# ----- writing into csv file
with open('books.csv', 'w') as file1:
    file1.write("1234567890, Harry Potter and The Chamber of Secrets, J.K Rowling, 10.00, 10\n")
    file1.write("1234567891, Harry Potter and The Philosopher's Stone, J.K Rowling, 15.00, 20\n")
    file1.close()  # -------- saves memory
    print("Content has been written to 'books'")


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

# ----- insert in main block 
csv_filename = "books.csv"
if book.load_books_inventory():
    print("Data loaded successfully.")
else:
    print("CSV file not found.")
        
        
# ----- insert in user inputs
book.save_books_inventory()
book.load_books_inventory()

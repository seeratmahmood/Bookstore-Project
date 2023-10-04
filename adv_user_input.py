from classes import Bookstore, Books, Users, RegisteredUsers
import re
import threading
import time


def main():

    book = Books(isbn=None, title=None, author=None, price=None, quantity=None)
    user = Users(first_name=None, last_name=None, email=None, password=None)
    reg_user = RegisteredUsers(first_name=None, last_name=None, email=None, password=None)

    choice = input("Welcome to the Bookstore\nEnter your choice: ")

    while True:
        print("\nBookstore Menu:")
        print("1. Register")
        print("2. Login")
        print("3. Add Books")
        print("4. List Books")
        print("5. Search Books")
        print("6. View Book Details")
        print("7. Add to Shopping Basket")
        print("8. View Shopping Basket")
        print("9. Update Shopping Basket")
        print("10. Proceed to Checkout")
        print("11. Access Order History")
        print("12. View Account Details")
        print("13. Modify Account Details")
        print("14. Purchase Books")

        if choice == "1":
            register_user_closure = user.register_user()
            if register_user_closure():
                print(register_user_closure)
            break

        elif choice == "2":
            if reg_user.login():
                print("Login Successful!")
            else:
                print("Invalid Email or Password")
            break

# add book - staff/employees only
        elif choice == '3':
            add_book_closure = book.add_book()
            if add_book_closure:
                print(add_book_closure())
            break

        elif choice == '4':
            for book_info in book.list_books():
                print(book_info)

        elif choice == '5':
            title_or_isbn = input("Enter the Title or ISBN of the Book you are searching for: ")
            book.search_books(title_or_isbn)
            break

        elif choice == '6':
            title_or_isbn = input("Enter the Title or ISBN of the book to view book information: ")
            user.view_book_info(title_or_isbn)  # Search by ISBN and Title
            break

        if choice == '7':
            isbn = input("Enter the ISBN number of the book you want to add to the basket: ")
            quantity = int(input("Enter the quantity: "))
            result = user.add_to_basket(isbn, quantity)
            print(result)
            break

        elif choice == '8':
            email = input("Enter your email: ")
            isbn = input("Enter the ISBN of the book you want to update: ")
            modify_quantity = int(input("Enter the new quantity: "))
            result = user.modify_basket(isbn, email,  modify_quantity)
            print(result)
            break

        elif choice == '9':
            email = input("Enter your email to view basket: ")
            user.view_basket(email)
            break

        elif choice == '10':
            email = input("Enter your email: ")
            if email not in user.user_accounts:
                print("Email not found. Please register or log in.")
                continue
            result = user.proceed_checkout(email)
            print(result)
            break

        elif choice == '11':
            print("Login to access your Order History\n")
            email = input("Email: ")
            reg_user.order_history(email)
            break

        if choice == '12':
            print("Log in to view Account Details:\n")
            email = input("Email: ")
            password = input("Password: ")
            reg_user.view_account_details(email, password)
            break

        elif choice == '13':
            email = input("Enter your original email to modify account details: ")
            new_first_name = input("Enter updated First Name:")
            new_last_name = input("Enter updated Last Name: ")
            new_email = input("Enter updated Email: ")
            new_password = input("Enter updated Password: ")
            result = reg_user.modify_account_details(email,new_first_name, new_last_name, new_email, new_password)
            print(result)
            break

        elif choice == '14':
            result = reg_user.purchase_books()
            print(result)
            break


if __name__ == "__main__":
    main()
    

import sqlite3
from datetime import datetime, timedelta

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Drop existing tables if they exist (for fresh setup)
cursor.execute("DROP TABLE IF EXISTS loans")
cursor.execute("DROP TABLE IF EXISTS members")
cursor.execute("DROP TABLE IF EXISTS books")

# Create the Books table
cursor.execute(
    """
CREATE TABLE books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    isbn TEXT UNIQUE,
    publication_year INTEGER,
    genre TEXT,
    quantity INTEGER NOT NULL DEFAULT 1,
    available_copies INTEGER NOT NULL DEFAULT 1
)
"""
)

# Create the Members table
cursor.execute(
    """
CREATE TABLE members (
    member_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone_number TEXT,
    address TEXT,
    membership_date DATE NOT NULL
)
"""
)

# Create the Loans table
cursor.execute(
    """
CREATE TABLE loans (
    loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    loan_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (member_id) REFERENCES members(member_id)
)
"""
)


# Function to add a book
def add_book(title, author, isbn, publication_year, genre, quantity):
    cursor.execute(
        """
    INSERT INTO books (title, author, isbn, publication_year, genre, quantity, available_copies)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
        (title, author, isbn, publication_year, genre, quantity, quantity),
    )
    conn.commit()


# Function to add a member
def add_member(first_name, last_name, email, phone_number, address):
    membership_date = datetime.now().date()
    cursor.execute(
        """
    INSERT INTO members (first_name, last_name, email, phone_number, address, membership_date)
    VALUES (?, ?, ?, ?, ?, ?)
    """,
        (first_name, last_name, email, phone_number, address, membership_date),
    )
    conn.commit()

    # Function to add a loan


def add_loan(book_id, member_id, loan_date, due_date, return_date=None):
    cursor.execute(
        """
    INSERT INTO loans (book_id, member_id, loan_date, due_date, return_date)
    VALUES (?, ?, ?, ?, ?)
    """,
        (book_id, member_id, loan_date, due_date, return_date),
    )
    conn.commit()


# Adding books to the database
books = [
    ("To Kill a Mockingbird", "Harper Lee", "9780061120084", 1960, "Fiction", 4),
    ("Pride and Prejudice", "Jane Austen", "9780141040349", 1813, "Romance", 5),
    ("1984", "George Orwell", "9780451524935", 1949, "Dystopian", 3),
    ("Moby-Dick", "Herman Melville", "9781503280786", 1851, "Adventure", 2),
    ("The Catcher in the Rye", "J.D. Salinger", "9780316769488", 1951, "Fiction", 3),
    ("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565", 1925, "Fiction", 4),
    ("War and Peace", "Leo Tolstoy", "9780199232765", 1869, "Historical", 2),
    ("The Hobbit", "J.R.R. Tolkien", "9780261102217", 1937, "Fantasy", 5),
]

for book in books:
    add_book(*book)

# Adding members to the database
members = [
    (
        "Alice",
        "Johnson",
        "alice.johnson@example.com",
        "555-1234",
        "456 Elm St, Anytown, USA",
    ),
    ("Bob", "Smith", "bob.smith@example.com", "555-5678", "789 Oak St, Anytown, USA"),
    (
        "Charlie",
        "Brown",
        "charlie.brown@example.com",
        "555-8765",
        "101 Pine St, Anytown, USA",
    ),
    (
        "David",
        "Wilson",
        "david.wilson@example.com",
        "555-4321",
        "202 Maple St, Anytown, USA",
    ),
    ("Eve", "Davis", "eve.davis@example.com", "555-6789", "303 Cedar St, Anytown, USA"),
    (
        "Frank",
        "Miller",
        "frank.miller@example.com",
        "555-1357",
        "404 Birch St, Anytown, USA",
    ),
    (
        "Grace",
        "Taylor",
        "grace.taylor@example.com",
        "555-2468",
        "505 Walnut St, Anytown, USA",
    ),
    (
        "Hank",
        "Anderson",
        "hank.anderson@example.com",
        "555-3579",
        "606 Spruce St, Anytown, USA",
    ),
]

for member in members:
    add_member(*member)
    # Adding loans to the database
today = datetime.now().date()
loans = [
    (
        1,
        1,
        today.strftime("%Y-%m-%d"),
        (today + timedelta(days=10)).strftime("%Y-%m-%d"),
    ),
    (
        2,
        2,
        (today - timedelta(days=5)).strftime("%Y-%m-%d"),
        (today + timedelta(days=5)).strftime("%Y-%m-%d"),
    ),
    (
        3,
        3,
        (today - timedelta(days=2)).strftime("%Y-%m-%d"),
        (today + timedelta(days=8)).strftime("%Y-%m-%d"),
    ),
    (
        4,
        4,
        today.strftime("%Y-%m-%d"),
        (today + timedelta(days=12)).strftime("%Y-%m-%d"),
    ),
    (
        5,
        5,
        (today - timedelta(days=1)).strftime("%Y-%m-%d"),
        (today + timedelta(days=9)).strftime("%Y-%m-%d"),
    ),
]

for loan in loans:
    add_loan(*loan)

print("Database has been created and populated with books and members.")

# Close the connection
conn.close()

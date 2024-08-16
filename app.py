from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


def get_books_with_loans():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    cursor.execute(
        """
    SELECT 
        b.book_id, b.title, b.author, b.available_copies, 
        CASE 
            WHEN l.return_date IS NULL AND l.loan_id IS NOT NULL THEN 'On Loan'
            ELSE 'Available'
        END as loan_status
    FROM books b
    LEFT JOIN loans l ON b.book_id = l.book_id AND l.return_date IS NULL
    """
    )

    books = cursor.fetchall()
    conn.close()

    books_list = [
        {
            "book_id": book[0],
            "title": book[1],
            "author": book[2],
            "available_copies": book[3],
            "loan_status": book[4],
        }
        for book in books
    ]

    return books_list


def get_members_with_loans():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    cursor.execute(
        """
    SELECT 
        m.member_id, m.first_name, m.last_name, 
        b.title, l.loan_date, l.due_date, l.return_date
    FROM members m
    LEFT JOIN loans l ON m.member_id = l.member_id
    LEFT JOIN books b ON l.book_id = b.book_id
    """
    )

    loans = cursor.fetchall()
    conn.close()

    loans_list = [
        {
            "member_id": loan[0],
            "first_name": loan[1],
            "last_name": loan[2],
            "book_title": loan[3],
            "loan_date": loan[4],
            "due_date": loan[5],
            "return_date": loan[6],
        }
        for loan in loans
    ]

    return loans_list


@app.route("/")
def home():
    return render_template("base.html")


@app.route("/books")
def list_books():
    books = get_books_with_loans()
    return render_template("books.html", books=books)


@app.route("/loans")
def list_loans():
    loans = get_members_with_loans()
    return render_template("loans.html", loans=loans)


if __name__ == "__main__":
    app.run(debug=True)

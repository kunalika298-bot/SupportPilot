
import sqlite3
from datetime import datetime

# Connect to the database
def connect_db():
    return sqlite3.connect("tickets.db")


# Create the tickets table
def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_name TEXT,
            email TEXT,
            title TEXT,
            description TEXT,
            department TEXT,
            business_impact TEXT,
            category TEXT,
            severity TEXT,
            priority TEXT,
            confidence REAL,
            status TEXT DEFAULT 'Open',
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


# Save ticket details
def save_ticket(ticket):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tickets (
            employee_name, email, title, description,
            department, business_impact, category,
            severity, priority, confidence, status, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        ticket["employee_name"],
        ticket["email"],
        ticket["title"],
        ticket["description"],
        ticket["department"],
        ticket["business_impact"],
        ticket["category"],
        ticket["severity"],
        ticket["priority"],
        ticket["confidence"],
        "Open",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    ticket_id = cursor.lastrowid
    conn.close()

    return ticket_id


# Retrieve all tickets
def get_tickets():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tickets ORDER BY id DESC")
    tickets = cursor.fetchall()

    conn.close()
    return tickets

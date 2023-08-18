import sqlite3
import random
from datetime import datetime, timedelta

# Delete the existing database if it exists
try:
    conn = sqlite3.connect('total_prices.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS total_prices')
    conn.commit()
    conn.close()
    print("Existing database deleted.")
except:
    pass

# Create a new database 'total_prices.db' to store total prices over time
conn = sqlite3.connect('total_prices.db')
cursor = conn.cursor()

# Create a table to store total prices
cursor.execute('''
    CREATE TABLE IF NOT EXISTS total_prices (
        date TEXT,
        total_price REAL
    )
''')

# Generate 14 separate insert statements with dates up to August 17th
insert_statements = [
    ("2023-08-04", random.randint(5400, 5500)),
    ("2023-08-05", random.randint(5400, 5500)),
    ("2023-08-06", random.randint(5400, 5500)),
    ("2023-08-07", random.randint(5400, 5500)),
    ("2023-08-08", random.randint(5400, 5500)),
    ("2023-08-09", random.randint(5400, 5500)),
    ("2023-08-10", random.randint(5400, 5500)),
    ("2023-08-11", random.randint(5400, 5500)),
    ("2023-08-12", random.randint(5400, 5500)),
    ("2023-08-13", random.randint(5400, 5500)),
    ("2023-08-14", random.randint(5400, 5500)),
    ("2023-08-15", random.randint(5400, 5500)),
    ("2023-08-16", random.randint(5400, 5500)),
    ("2023-08-17", random.randint(5400, 5500))
]

for date, price in insert_statements:
    cursor.execute('INSERT INTO total_prices (date, total_price) VALUES (?, ?)', (date, price))

conn.commit()
conn.close()

print("New database created with 14 insert statements.")

import sqlite3
import csv
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

suppliers_data = []
for i in range(1, 51):
    supplier = {
        'id': i,
        'full_name': fake.company(),
        'is_active': random.choice([True, False]),
        'contact_number': fake.phone_number(),
        'created_at': fake.date_time_this_decade(),
        'updated_at': fake.date_time_this_decade(),
        'created_by_id': random.randint(1, 10),
        'updated_by_id': random.randint(1, 10)
    }
    suppliers_data.append(supplier)

categories_data = []
for i in range(1, 301):
    category = {
        'id': i,
        'name': fake.word(),
        'slug': fake.slug(),
        'created_at': fake.date_time_this_decade(),
        'updated_at': fake.date_time_this_decade(),
        'created_by_id': random.randint(1, 10),
        'updated_by_id': random.randint(1, 10)
    }
    categories_data.append(category)

products_data = []
for i in range(1, 10001):
    product = {
        'id': i,
        'title': fake.word(),
        'description': fake.text(),
        'price': round(random.uniform(10.0, 1000.0), 2),
        'slug': fake.slug(),
        'status': random.choice(['active', 'inactive']),
        'brand': fake.company(),
        'created_at': fake.date_time_this_decade(),
        'updated_at': fake.date_time_this_decade(),
        'created_by_id': random.randint(1, 10),
        'updated_by_id': random.randint(1, 10)
    }
    products_data.append(product)

def write_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

write_to_csv(suppliers_data, 'suppliers.csv')
write_to_csv(categories_data, 'categories.csv')
write_to_csv(products_data, 'products.csv')




def create_database():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()


    c.execute('''CREATE TABLE IF NOT EXISTS suppliers (
                    id INTEGER PRIMARY KEY,
                    full_name TEXT,
                    is_active BOOLEAN,
                    contact_number TEXT,
                    created_at DATETIME,
                    updated_at DATETIME,
                    created_by_id INTEGER,
                    updated_by_id INTEGER
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    slug TEXT,
                    created_at DATETIME,
                    updated_at DATETIME,
                    created_by_id INTEGER,
                    updated_by_id INTEGER
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY,
                    title TEXT,
                    description TEXT,
                    price REAL,
                    slug TEXT,
                    status TEXT,
                    brand TEXT,
                    created_at DATETIME,
                    updated_at DATETIME,
                    created_by_id INTEGER
                )''')

    conn.commit()
    conn.close()


def insert_data(table_name, csv_filename):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            columns = ', '.join(row.keys())
            placeholders = ', '.join(['?' for _ in range(len(row))])
            query = f"INSERT OR IGNORE INTO {table_name} ({columns}) VALUES ({placeholders})"
            c.execute(query, tuple(row.values()))

    conn.commit()
    conn.close()

create_database()


insert_data('suppliers', 'suppliers.csv')
insert_data('categories', 'categories.csv')
insert_data('products', 'products.csv')

print("Data inserted successfully into SQLite database!")

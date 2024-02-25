import sqlite3


db = sqlite3.connect('shop.db')

db.execute('''

CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL
);
           ''')

db.execute('''
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL, 
    email TEXT NOT NULL UNIQUE 
    );
           ''')

db.execute('''
CREATE TABLE IF NOT EXISTS orders ( 
order_id INTEGER PRIMARY KEY AUTOINCREMENT,
customer_id INTEGER NOT NULL,
product_id INTEGER NOT NULL,
quantity INTEGER NOT NULL,
order_date DATE NOT NULL,
FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
FOREIGN KEY (product_id) REFERENCES products(product_id) 
);
           ''')


def add_product(db,name,category,price):
    db.execute('''
               INSERT INTO products(name,category,price) VALUES (?,?,?)
               ''',(name,category,price))
    db.commit()
    
def add_customer(db,first_name,last_name,email):
    db.execute('''
               INSERT INTO customers(first_name,last_name,email) VALUES (?,?,?)
               ''',(first_name,last_name,email))
    db.commit()
    
def add_order(db,customer_id,product_id,quantity):
    db.execute('''
               INSERT INTO orders(customer_id,product_id,quantity,order_date) VALUES (?,?,?,CURRENT_TIMESTAMP)
               ''',(customer_id,product_id,quantity))
    db.commit()
    
def get_total_income(db):
    query = """ SELECT SUM(products.price * orders.quantity) AS total_bill
                FROM orders
                INNER JOIN products ON orders.order_id = products.product_id"""
    return db.execute(query).fetchone()

def order_quantity(db):
    query = db.execute(''' SELECT customers.first_name AS customer_name,
                       COUNT(orders.order_id) AS amount_of_orders
                       FROM orders
                       INNER JOIN customers ON orders.customer_id = customers.customer_id
                       GROUP BY customer_name''')
    return query.fetchall()

def avg_bill(db):
    query = db.execute(""" SELECT AVG(products.price * orders.quantity) AS avg_bill
                   FROM orders
                   INNER JOIN products ON orders.order_id = products.product_id""")
    return query.fetchall()

def most_popular_category(db):
    query = db.execute('''SELECT products.category, SUM(orders.quantity) AS total_order_quantity
                   FROM orders
                   INNER JOIN products ON orders.product_id = products.product_id
                   GROUP BY products.category
                   ORDER BY total_order_quantity DESC''')
    return query.fetchone()[0]

def get_products_quantity(db):
    query = db.execute('''SELECT products.category, SUM(orders.quantity) AS total_order_quantity
                   FROM orders
                   INNER JOIN products ON orders.product_id = products.product_id
                   GROUP BY products.category''')
    return query.fetchall()

def increase_value_of_phones_by_10_percents(db):
    db.execute('''UPDATE products
                SET price = price * 1.1
                WHERE category = "mobile phone"''')
    db.commit()
    
def show_all_customers(db):
    r = db.execute('''SELECT first_name, last_name FROM customers''')
    return r.fetchall()

def show_all_products(db):
    r = db.execute('''SELECT name FROM products''')
    return r.fetchall()

def show_all_orders(db):
    r = db.execute('''SELECT * FROM orders''')
    return r.fetchall()


while True:
    print('''
    Що ви хочете зробити?

    1 - Додавання продуктів:
    2 - Додавання клієнтів:
    3 - Замовлення товарів:
    4 - Сумарний обсяг продажів:
    5 - Кількість замовлень на кожного клієнта:
    6 - Середній чек замовлення:
    7 - Найбільш популярна категорія товарів:
    8 - Загальна кількість товарів кожної категорії:
    9 - Оновлення цін категорії на 10% більші:
    10 - Показати усіх користувачів
    11 - Показати усі продукти
    12 - Показати усі замовлення(Joined)
    0 - Вийти: ''')
    
    choice =int(input(': '))
    if choice == 1:
        name = input('name: ')
        category = input('category: ')
        price = input('price: ')
        add_product(db,name,category,price)
    elif choice == 2:
        first_name = input('first_name: ')
        last_name= input('last_name: ')
        email = input('email: ')
        add_customer(db,first_name,last_name,email)
    elif choice == 3:
        customer_id = input('customer_id: ')
        product_id= input('product_id: ')
        quantity = input('quantity: ')
        add_order(db,customer_id,product_id,quantity)
    elif choice == 4:
        print(get_total_income(db))
    elif choice == 5:
        print(order_quantity(db))
    elif choice == 6:
        print(avg_bill(db))
    elif choice == 7:
        print(most_popular_category(db))
    elif choice == 8:
        print(get_products_quantity(db))
    elif choice == 9:
        increase_value_of_phones_by_10_percents(db)
        print('updated')
    elif choice == 10:
        print(show_all_customers(db))
    elif choice == 11:
        print(show_all_products(db))
    elif choice == 12:
        print(show_all_orders(db))
    elif choice == 0:
        break
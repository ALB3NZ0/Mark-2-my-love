import sqlite3

class User:
    def __init__(self, user_id, username, password, role, full_name):
        self.id = user_id
        self.username = username
        self.password = password
        self.role = role
        self.full_name = full_name

class Tovar:
    def __init__(self, tovar_id, brand, model, year, product_count, price):
        self.tovar_id = tovar_id
        self.brand = brand
        self.model = model
        self.year = year
        self.product_count = product_count
        self.price = price

class Admin:
    def __init__(self, admin_id, surname, name):
        self.admin_id = admin_id
        self.surname = surname
        self.name = name

class Order:
    def __init__(self, order_id, user_id, product_id):
        self.order_id = order_id
        self.user_id = user_id
        self.product_id = product_id

class Database:
    conn = sqlite3.connect('sale_car.db')
    cursor = conn.cursor()

    @classmethod
    def create_tables(cls):
        cls.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                full_name TEXT NOT NULL
            )
        ''')

        cls.cursor.execute('''CREATE TABLE IF NOT EXISTS tovars (
            id INTEGER PRIMARY KEY,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            year INTEGER NOT NULL,
            product_count INTEGER NOT NULL,
            price REAL NOT NULL
        )''')
        cls.cursor.execute('''CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY,
            surname TEXT NOT NULL,
            name TEXT NOT NULL
        )''')
        cls.cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (product_id) REFERENCES tovars (id)
        )''')
        cls.conn.commit()

    @classmethod
    def fetch_user(cls, username, password):
        cls.cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user_data = cls.cursor.fetchone()
        if user_data:
            user = User(*user_data)
            return user
        return None

    @classmethod
    def add_user(cls, user):
        cls.cursor.execute('''
            INSERT INTO users (username, password, role, full_name)
            VALUES (?, ?, ?, ?)
        ''', (user.username, user.password, user.role, user.full_name))
        cls.conn.commit()

    @classmethod
    def add_tovar(cls, brand, model, year, product_count, price):
        cls.cursor.execute('''INSERT INTO tovars(brand, model, year, product_count, price) VALUES (?,?,?,?,?)''',
                           (brand, model, year, product_count, price))
        cls.conn.commit()

    @classmethod
    def add_admin(cls, surname, name):
        cls.cursor.execute(''' INSERT INTO admins(surname, name) VALUES (?,?)''', (surname, name))
        cls.conn.commit()

    @classmethod
    def add_order(cls, user_id, product_id):
        cls.cursor.execute('''INSERT INTO orders(user_id, product_id) VALUES (?,?)''', (user_id, product_id))
        cls.conn.commit()




    @classmethod
    def delete_user(cls, name, surname, login, password, role):
        connection = sqlite3.connect('sale_car.db')
        cls.cursor = connection.cursor()
        cls.cursor.execute('''DELETE FROM users WHERE name = ? AND surname = ? AND login = ? AND password = ? AND role = ?''',
                           (name,surname, login, password, role))




    @classmethod
    def delete_tovar(cls, brand, model, year, product_count, price):
        connection = sqlite3.connect('sale_car.db')
        cls.cursor = connection.cursor()
        cls.cursor.execute(
            '''DELETE FROM tovars WHERE brand = ? AND model = ? AND year = ? AND product_count = ? AND price = ?''',
            (brand, model, year, product_count, price))


    @classmethod
    def delete_admin(cls, surname, name):
        connection = sqlite3.connect('sale_car.db')
        cls.cursor = connection.cursor()
        cls.cursor.execute(
            '''DELETE FROM tovars WHERE surname = ? AND name = ? ''',
            (surname, name))



    @classmethod
    def delete_order(cls,order_id, user_id, product_id):
        connection = sqlite3.connect('sale_car.db')
        cls.cursor = connection.cursor()
        cls.cursor.execute('''DELETE FROM orders WHERE order_id = ?''',
                           (order_id,user_id, product_id))


    @classmethod
    def change_order(cls, order_id, new_products):
        connection = sqlite3.connect('sale_car.db')
        cls.cursor = connection.cursor()
        cls.cursor.execute('''UPDATE orders SET product_id = ? WHERE id = ?''',
                           (new_products, order_id))




class Interface:
    @staticmethod
    def register():
        username = input("Введите имя пользователя: ")
        password = input("Введите пароль: ")
        role = input("Выберите роль (Клиент/Сотрудник): ")
        full_name = input("Введите ваше полное имя: ")

        user = User(None, username, password, role, full_name)
        Database.add_user(user)
        print("Регистрация прошла успешно!")

    def login():
        username = input("Введите имя пользователя: ")
        password = input("Введите пароль: ")
        user = Database.fetch_user(username, password)

        if user:
            return user
        else:
            print("Неверное имя пользователя или пароль.")
            return None

    @staticmethod
    def view_products():
        Database.cursor.execute("SELECT * FROM tovars")
        products = Database.cursor.fetchall()

        # Выводим информацию о товарах
        if products:
            print("Список товаров:")
            for product in products:
                tovar_id, brand, model, year, product_count, price = product
                print(
                    f"ID: {tovar_id}, Бренд: {brand}, Модель: {model}, Год выпуска:{year}, Количество: {product_count}, Цена: {price}")
        else:
            print("В базе данных нет товаров.")

    @staticmethod
    def add_to_product_count():
        tovar_id = input("Введите ID товара, который хотите добавить в корзину: ")
        user_id = 1
        Database.add_order(user_id, tovar_id)
        print("Товар успешно добавлен в корзину!")

    @classmethod
    def change_order(cls, order_id, new_products):
        cls.cursor.execute('''
                UPDATE orders
                SET products = ?
                WHERE id = ?
            ''', (new_products, order_id))
        cls.conn.commit()

    @classmethod
    def delete_product(product_id):
        Database.cursor.execute('''
                      DELETE FROM products
                      WHERE id = ?
                  ''', (product_id,))
        Database.conn.commit()



    @staticmethod
    def change_order():
        order_id = input("Введите ID заказа, который хотите изменить: ")
        new_products = input("Введите новый список товаров: ")

        Database.cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id))
        order = Database.cursor.fetchone()

        if order:
            Database.change_order(order_id, new_products)
            print("Заказ успешно изменен!")
        else:
            print("Заказ с указанным ID не найден.")

    @staticmethod
    def delete_order():
        order_id = input("Введите ID заказа, который хотите удалить: ")
        user_id = input("Введите ID пользователя: ")
        product_id = input("Введите ID товара: ")

        Database.delete_order(order_id, user_id, product_id)
        print("Заказ успешно удален!")

    @staticmethod
    def delete_order(order_id):
        Database.delete_order(order_id)
        print("Заказ успешно удален!")

    @staticmethod
    def view_cart(user_id):
        # Просмотр корзины пользователя
        Database.cursor.execute('''
                SELECT orders.id, tovars.brand, tovars.model, tovars.price
                FROM orders
                JOIN tovars ON orders.product_id = tovars.id
                WHERE orders.user_id = ?
            ''', (user_id,))
        cart_items = Database.cursor.fetchall()

        if cart_items:
            print("Корзина:")
            for item in cart_items:
                order_id, brand, model, price = item
                print(f"Заказ #{order_id}: {brand} {model}, Цена: {price}")
        else:
            print("Корзина пуста.")

    @staticmethod
    def client_interface():
        print("Добро пожаловать в интерфейс клиента!")

        while True:
            choice = input(
                "1. Просмотр товаров\n2. Добавить товар в корзину\n3. Изменить заказ\n4. Удалить заказ\n5. Просмотреть корзину\n6. Выйти\nВыберите действие: ")

            if choice == "1":
                Interface.view_products()
            elif choice == "2":
                Interface.add_to_product_count()
            elif choice == "3":
                Interface.change_order()
            elif choice == "4":
                order_id = input("Введите ID заказа, который хотите удалить: ")
                Interface.delete_order(order_id)
            elif choice == "5":
                Interface.view_cart(user_id)
            elif choice == "6":
                return
            else:
                print("Неверный ввод. Пожалуйста, выберите корректное действие.")

    @staticmethod
    def add_tovar():
        brand = input("Введите название товара: ")
        model = input("Введите название модели:")
        year = input("Введите год выпуска:")
        product_count = input("Введите количество товара:")
        price = float(input("Введите цену товара: "))

        tovar = Tovar(None, brand, model, year, product_count, price)
        Database.add_tovar(tovar)
        print("Товар успешно добавлен!")

    @staticmethod
    def delete_tovar():
        tovar_id = input("Введите ID товара, который хотите удалить: ")
        Database.cursor.execute("SELECT * FROM tovars WHERE id = ?", (tovar_id,))
        tovar = Database.cursor.fetchone()

        if tovar:
            Database.cursor.execute("DELETE FROM tovars WHERE id = ?", (tovar_id,))
            Database.conn.commit()
            print("Товар успешно удален!")
        else:
            print("Товар с указанным ID не найден.")



    @staticmethod
    def update_tovar():
        tovar_id = input("Введите ID товара, который хотите изменить: ")

        Database.cursor.execute("SELECT * FROM tovars WHERE id = ?", (tovar_id,))
        product = Database.cursor.fetchone()

        if product:
            tovar_id, brand,model,year,product_count,price = product
            print(f"Текущие данные товара (ID: {tovar_id}):")
            print(f"Название: {brand}, Модель: {model},Год выпуска: {year},Количество: {product_count},Цена: {price}, ")

            new_brand = input("Введите новое название товара (или Enter, чтобы оставить без изменений): ")
            new_model = input("Введите новое название модели (или Enter, чтобы оставить без изменений): ")
            new_year = input("Введите новое значение года (или Enter, чтобы оставить без изменений): ")
            new_quantity = int(input("Введите новое количество товара (или Enter, чтобы оставить без изменений): "))
            new_price = float(input("Введите новую цену товара (или Enter, чтобы оставить без изменений): "))


            if new_name:
                product = (new_brand,new_model,new_year,new_quantity, new_price, tovar_id)
                Database.cursor.execute('''
                    UPDATE tovars
                    SET brand = ?, model = ?, year = ?, quantity = ?, price = ?
                    WHERE id = ?
                ''', product)
                Database.conn.commit()

            print("Товар успешно изменен!")
        else:
            print("Товар с указанным ID не найден.")



    @staticmethod
    def update_user():
        username = input("Введите имя пользователя, данные которого хотите изменить: ")

        Database.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user_data = Database.cursor.fetchone()

        if user_data:
            user_id, current_username, password, role, full_name = user_data
            print(f"Текущие данные пользователя (ID: {user_id}):")
            print(f"Имя пользователя: {current_username}, Роль: {role}, Полное имя: {full_name}")

            new_username = input("Введите новое имя пользователя (или Enter, чтобы оставить без изменений): ")
            new_role = input("Введите новую роль пользователя (или Enter, чтобы оставить без изменений): ")
            new_full_name = input("Введите новое полное имя пользователя (или Enter, чтобы оставить без изменений): ")

            if new_username:
                user = (new_username, new_role, new_full_name, username)
                Database.cursor.execute('''
                        UPDATE users
                        SET username = ?, role = ?, full_name = ?
                        WHERE username = ?
                    ''', user)
                Database.conn.commit()

            print("Данные пользователя успешно изменены!")
        else:
            print("Пользователь с указанным именем не найден.")


    @staticmethod
    def employee_interface():
        print("Добро пожаловать в интерфейс сотрудника!")
        while True:
            choice = input(
                "1. Добавить товар\n2. Удалить товар\n3. Изменить товар\n4. Изменить данные клиента\n5. Выйти\nВыберите действие: "
            )
            if choice == "1":
                Interface.add_tovar()
            elif choice == "2":
                Interface.delete_tovar()
            elif choice == "3":
                Interface.update_tovar()
            elif choice == "4":
                Interface.update_user()
            elif choice == "5":
                break
            else:
                print("Неверный ввод. Пожалуйста, выберите корректное действие.")

    @staticmethod
    def main():
        while True:
            choice = input("1. Регистрация\n2. Авторизация\n3. Выход\nВыберите действие: ")

            if choice == "1":
                Interface.register()
            elif choice == "2":
                user = Interface.login()
                if user and user.role == "Клиент":
                    Interface.client_interface()
                elif user and user.role == "Сотрудник":
                    Interface.employee_interface()
                break
            else:
                print("Неверный ввод. Пожалуйста, выберите корректное действие.")



if __name__ == "__main__":
    Database.create_tables()
    BMW = Tovar(None, "BMW", "E34", 1989, 10, 30000000)
    Mercedes = Tovar(None, "Mercedes", "CLS", 2012, 10, 15000000)
    Toyota = Tovar(None, "Toyota", "Mark 2", 1996, 10, 100000000)
    Honda = Tovar(None, "Honda", "Civic", 1992, 10, 10000000)
    Database.add_tovar(BMW.brand, BMW.model, BMW.year, BMW.product_count, BMW.price)
    Database.add_tovar(Mercedes.brand, Mercedes.model, Mercedes.year, Mercedes.product_count, Mercedes.price)
    Database.add_tovar(Toyota.brand, Toyota.model, Toyota.year, Toyota.product_count, Toyota.price)
    Database.add_tovar(Honda.brand, Honda.model, Honda.year, Honda.product_count, Honda.price)


    Interface.main()


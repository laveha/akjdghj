import sqlite3


class ZapchastiDatabase:
    def __init__(self):
        self.connection = sqlite3.connect('detali.db')
        self.create_tables()

    def create_tables(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS detali
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           title TEXT NOT NULL,
                           proizvoditel TEXT NOT NULL,
                           quantity INTEGER NOT NULL)''')

        cursor.execute("INSERT INTO detali (title, proizvoditel, quantity) VALUES (?, ?, ?)",
                       ('Кардан ВАЗ 2105', 'Россия', 10))
        cursor.execute("INSERT INTO detali (title, proizvoditel, quantity) VALUES (?, ?, ?)",
                       ('Привод Toyota Rav4', 'Япония', 6))

        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           username TEXT NOT NULL,
                           password TEXT NOT NULL,
                           role TEXT NOT NULL)''')
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                        ('Иван', '12345', 'user'))
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                        ('admin', 'admin123', 'admin'))

        self.connection.commit()

    def validate_user(self, username, password):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        if user:
            return user[3] 
        else:
            return None

    def get_detali(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM detali")
        return cursor.fetchall()

    def add_detal(self, title, proizvoditel, quantity):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO detali (title, proizvoditel, quantity) VALUES (?, ?, ?)",
                       (title, proizvoditel, quantity))
        self.connection.commit()

    def update__password_admin(self, password, name):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE users SET password = ? WHERE username = ?", (password, name))
        self.connection.commit()
    def update__name_admin(self, new_name, name):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE users SET name = ? WHERE username = ?", (new_name, name))
        self.connection.commit()
    def update_user_name(self, name, new_name):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE users SET name = ? WHERE username = ?", (new_name, name))
        self.connection.commit()
    def update_detal_quantity(self, detal_id, new_quantity):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE detali SET quantity = ? WHERE id = ?", (new_quantity, detal_id))
        self.connection.commit()
    def delete_detali(self,detal_ids):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM detali WHERE id >0",(detal_ids))
        self.connection.commit()
    def delete_detal(self, detal_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM detali WHERE id = ?", (detal_id,))
        self.connection.commit()



class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

class Zapchasti:
    def __init__(self, title, proizvoditel, quantity):
        self.title = title
        self.proizvoditel = proizvoditel
        self.quantity = quantity

    def __str__(self):
        return f"{self.title} - {self.proizvoditel} ({self.quantity} шт.)"



class Sklad:
    def __init__(self, database):
        self.database = database
        self.current_user = User('','','')

    def login(self, username, password):
        role = self.database.validate_user(username, password)
        if role:
            self.current_user = User(username, password, role)
            print('Авторизация успешна.')
        else:
            print('Ошибка авторизации.')


    def change_password_admin(self, new_password, name):
        if self.current_user.role == 'admin':
            self.database.update__password_admin(new_password, name)
            print('Деталь успешно добавлена на склад.')
        else:
            print('Ошибка доступа. Добавлять детали может только администратор.')

    def add_detal(self, title, proizvoditel, quantity):
        if self.current_user.role == 'admin':
            self.database.add_detal(title, proizvoditel, quantity)
            print('Деталь успешно добавлена на склад.')
        else:
            print('Ошибка доступа. Добавлять детали может только администратор.')

    def delete_detali(self,detal_ids):
            self.database.delete_detali(detal_ids)
            print('Деталь успешно удалена со сколада.')


    def delete_detal(self, detal_id):
        if self.current_user.role == 'admin':
            self.database.delete_detal(detal_id)
            print('Деталь успешно удалена со склада.')
        else:
            print('Ошибка доступа. Удалять детали может только администратор.')

    def show_detali(self):
        detali = self.database.get_detali()
        for detal in detali:
            detal_obj = detal(detal[1], detal[2], detal[3])
            print(detal_obj)

    def update_detal_quantity(self, detal_id, new_quantity):
        if self.current_user.role == 'admin':
            self.database.update_detal_quantity(detal_id, new_quantity)
            print('Количество деталей успешно обновлено.')
        else:
            print('Ошибка доступа. Обновлять количество деталей может только администратор.')


database = ZapchastiDatabase()

c = 2
detal_ids = 0
detali = Sklad(database)
print("Введите ваше имя:")
name = input()
print("Введите ваш пароль:")
passward = input()
detali.login(name, passward)
while True:
    if(name == "admin"):
        print("Что вы хотите сделать?")
        print("1. Изменить свое имя")
        print("2. Изменить пароль пользователя")
        print("3. Удалить детали из реестра")
        print("4. Добавить детали в реестр")
        print("5. Выйти")


        answer = input("Введите номер команды: ")
        match answer:
            case "1":
                print("Введите новый пароль")
                new_passward = input()
                detali.change_password_admin(new_passward,name)
            case "2":  
                continue
            case "3":
                for i in range(c,detal_ids):
                    detali.delete_detali(i)
                continue
            case "4":
                detali.add_detal('Коробка BMW F90', 'Германия', 2)
                c=c+1
                detal_ids = c
                continue
            case "5":
                for i in range(c,detal_ids):
                    detali.delete_detali(i)
                break
            case _:
                print("Такой команды нет!")
    
    detali.show_detali()


    detali.update_detal_quantity(1, 8)


    detali.delete_detal(2)
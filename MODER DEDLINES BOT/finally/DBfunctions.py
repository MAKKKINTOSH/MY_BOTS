import sqlite3
class data_base:
    """Класс для работы с базой данных"""

    def __init__(self, data_base):
        """Подключение базы данных"""
        self.connect = sqlite3.connect(data_base, check_same_thread=False)
        self.cursor = self.connect.cursor()

    def is_registred(self, user_id):
        """Проверяет, зарегистрирован ли пользователь в системе"""
        self.cursor.execute("SELECT user_id "
                            "FROM user "
                            "WHERE user_id = ?",
                            (user_id,))
        if str(self.cursor.fetchone()) == "None":
            return False
        return True

    def new_user(self, user_id, user_group):
        """Добавление в базу данных нового пользователя или изменение его группы"""
        self.cursor.execute("DELETE FROM user "
                            "WHERE user_id = ?",
                            (user_id,))
        self.cursor.execute("INSERT INTO user "
                            "('user_id', 'user_group') "
                            "VALUES (?, ?)",
                            (user_id, user_group))
        return self.connect.commit()

    def take_variable(self, user_id, variable):
        """Возвращает параметр пользователя по его id"""
        self.cursor.execute(f"SELECT {variable} "
                            f"FROM user "
                            f"WHERE user_id = ?",
                            (user_id,))
        value = str(self.cursor.fetchone())
        if variable == "user_group":
            return value[2:-3]
        return int(value[1:-2])


    def change_variable(self, user_id, variable, value):
        """Изменяет параметр пользователя с именем variable на value"""
        self.cursor.execute(f"UPDATE user "
                            f"SET {variable} = ?"
                            f" WHERE user_id = ?",
                            (value, user_id))
        return self.connect.commit()

    def change_date_variable(self, user_id, variable, operator):
        """Изменяет на +1 или -1 год или месяц на выбор variable"""
        self.cursor.execute(f"UPDATE user "
                            f"SET {variable} = '$change',"
                            f"{variable} = {variable} {operator} 1 "
                            f"WHERE user_id = ?",
                            (user_id,))
        return self.connect.commit()

    def make_deadline(self, group, day, month, year, text):
        """Создает дедлайн"""
        self.cursor.execute(f"INSERT INTO '{group}'"
                            f"('date', 'deadline')"
                            f"VALUES (?, ?)",
                            (f"{year}-{month}-{day}", text))
        return self.connect.commit()

    def show_deadline(self, group, day, month, year):
        """Показывает дедлайны на введенную дату"""
        self.cursor.execute(f"SELECT deadline FROM '{group}'"
                            f"WHERE date = ?",
                            (f"{year}-{month}-{day}", ))        #{year}-{month}-{day}

        deadlines = f"Дедлайны на {day}.{month}.{year}:\n\n"
        n = 1
        for k in self.cursor:
            deadlines += f"{n}. {str(k)[2:-3]}\n"
            n+=1
        if deadlines == f"Дедлайны на {day}.{month}.{year}:\n\n":
            deadlines += "Тут пусто"
            return deadlines
        return deadlines

    def delete_deadline(self, group, day, month, year, number):
        """Удаляет дедлайн"""
        date = f"{year}-{month}-{day}"
        self.cursor.execute(f"SELECT deadline "
                            f"FROM '{group}'"
                            f"WHERE date = ?",
                            (date, ))

        deadline = self.cursor.fetchall()[number-1]
        print(deadline)

        self.cursor.execute(f"DELETE FROM '{group}'"
                            f"WHERE deadline = ? "
                            f"AND date = ? ", (str(deadline)[2:-3], date))
        return self.connect.commit()

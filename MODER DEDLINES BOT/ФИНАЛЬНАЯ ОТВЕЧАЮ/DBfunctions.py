import sqlite3
class data_base:
    """Класс для работы с базой данных"""

    def __init__(self, data_base):
        """Подключение базы данных"""
        self.connect = sqlite3.connect(data_base, check_same_thread=False)
        self.cursor = self.connect.cursor()

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

        self.cursor.execute(f"DELETE FROM '{group}'"
                            f"WHERE deadline = ? "
                            f"AND date = ? ", (str(deadline)[2:-3], date))
        return self.connect.commit()

    def show_next_n_deadline(self, group, n):
        """Показывает ближайшие n дедлайнов"""
        self.cursor.execute(f"SELECT date, deadline "
                            f"FROM '{group}'"
                            f"ORDER BY date")

        deadlines = f"Ближайшие {n} дедлайнов:\n\n"
        n = 1

        for k in self.cursor:
            date = k[0]
            deadlines+=f"{n}. {date[8:]}.{date[5:7]}.{date[:4]}\n" \
                       f"{k[1]}\n\n"
            n+=1
            if n == 6:
                break

        if deadlines == f"Ближайшие {n} дедлайнов:\n\n":
            deadlines += "Тут пусто"
            return deadlines

        return deadlines

    def record_exist(self, group, day, month, year):
        self.cursor.execute(f"SELECT date "
                            f"FROM '{group}' "
                            f"WHERE date = ?",
                            (f"{year}-{month}-{day}", ))
        for k in self.cursor:
            return True
        return False
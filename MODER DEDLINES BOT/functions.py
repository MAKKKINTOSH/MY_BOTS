import sqlite3

class DeadDb:
    """Класс для работы с базой данных бота"""

    def __init__(self, data_base):
        """подключение базы данных"""
        self.connect = sqlite3.connect(data_base, check_same_thread=False)
        self.cursor = self.connect.cursor()

    def make_deadline(self, object_type, deadline_type, deadline_date):
        """ввод в базу данных нового дедлайна"""
        self.cursor.execute("INSERT INTO deadline ('object_type', 'deadline_type', 'deadline_date')"
                            " VALUES (?, ?, ?)",
                            (object_type, deadline_type, deadline_date))
        return self.connect.commit()

    def show_deadline(self, object_type, deadline_type):
        """вывод в сообщении ближайшего дедлайна"""
        self.cursor.execute("SELECT deadline_date"
                            " FROM deadline "
                            "WHERE object_type = ? AND deadline_type = ?"
                            "ORDER BY deadline_date",
                            (object_type, deadline_type))
        a = str(self.cursor.fetchone())[2:-3]       #yyyy-mm-dd -> dd.mm.yyyy
        #print(a)   #DELETE ON RELEASE
        if a == '': return 'Дедлайнов нет'
        date = a[8]+a[9]+'.'+a[5]+a[6]+'.'+a[0]+a[1]+a[2]+a[3]
        return date

    def object(self, object_type):
        """вывод названия предмета"""
        get = self.cursor.execute("SELECT object_name FROM object WHERE object_type = ?", (object_type,))
        return str(self.cursor.fetchone())[2:-3]

    def show_n_deadline(self, n):
        """Показ n-го дедлайна"""
        object_name = ''
        type=''
        date = ''
        selection = ''
        self.cursor.execute("SELECT object_type FROM deadline ORDER BY deadline_date")
        selection = self.cursor.fetchall()
        if len(selection) < n : return "Тут пусто"
        object_name = selection[n-1]
        self.cursor.execute("SELECT object_name FROM object WHERE object_type = ?", (str(object_name)[2:-3],))
        object_name = str(self.cursor.fetchone())[2:-3]
        #print(object_name, end='\t')        #DELETE ON RELEASE
        self.cursor.execute("SELECT deadline_type FROM deadline WHERE rowid = ? ORDER BY deadline_date", (n,))
        type = 'Д/З' if str(self.cursor.fetchone())[1:-2] == '0' else 'Л/Р'
        #print(type, end ='\t')      #DELETE ON RELEASE
        self.cursor.execute("SELECT deadline_date FROM deadline ORDER BY deadline_date")
        a = str(self.cursor.fetchall()[n-1])[2:-3] #yyyy-mm-dd   ->   dd.mm.yyyy
        #print(a)        #DELETE ON RELEASE
        date = a[8]+a[9]+'.'+a[5]+a[6]+'.'+a[0]+a[1]+a[2]+a[3]
        return (f"{object_name} {type}: {date}")

    def auto_delete_deadline(self,):
        """Автоудаление дедлайна по прошествии даты"""
        self.cursor.execute("DELETE FROM deadline WHERE deadline_date < date('now')")
        return self.connect.commit()

    def print_data_base(self):
        """Метод для тестирования базы"""
        self.cursor.execute("SELECT * FROM object")
        print(self.cursor.fetchall())

    def show_all_deadline(self, object_type):
        all_deadline_string= '              гггг-мм-дд'
        self.cursor.execute("SELECT deadline_type, deadline_date FROM deadline WHERE object_type = ? ORDER BY deadline_date", (object_type, ))
        all = self.cursor.fetchall()
        for n in range(len(all)):
            indexed_all=str(all[n])
            if indexed_all[1] == '0':
                indexed_all = indexed_all.replace('0', 'Д/З', 1)
            else:
                indexed_all = indexed_all.replace('1', 'Л/Р', 1)
            all_deadline_string+=f"\n{n+1}. {indexed_all[1:-1]}"
        #print(all_deadline_string)             DELETE ON RELEASE
        if all_deadline_string == '              гггг-мм-дд': return "\nТут нечего удалять"
        return all_deadline_string

    def delete_deadline(self, object_type,n):
        self.cursor.execute("SELECT deadline_type, deadline_date FROM deadline WHERE object_type = ? ORDER BY deadline_date", (object_type, ))
        deadline = self.cursor.fetchall()[n-1]
        self.cursor.execute("DELETE FROM deadline WHERE object_type = ? AND deadline_type = ? AND deadline_date = ?", (object_type, deadline[0], deadline[1]))
        return self.connect.commit()
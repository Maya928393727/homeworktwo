import tkinter as tk
from tkinter import ttk
import sqlite3
# Класс главного окна
class Main(tk.Frame):

    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    # Инициализация виджетов главного окна
    def init_main(self):

        # Верхняя панель для кнопок
        toolbar = tk.Frame(bg='#d7d7d7', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Кнопка добавления
        self.add_img = tk.PhotoImage(file='./img/add.png')
        btn_open_dialog = tk.Button(toolbar, bg='#d7d7d7', bd=0,
                                    image = self.add_img,
                                    command=self.open_dialog)
        btn_open_dialog.pack(side=tk.LEFT)

        # Кнопка редактирования
        self.upd_img = tk.PhotoImage(file='./img/update.png')
        btn_upd_dialog = tk.Button(toolbar, bg='#d7d7d7', bd=0,
                                   image = self.upd_img,
                                   command=self.open_update_dialog)
        btn_upd_dialog.pack(side=tk.LEFT)

        # Кнопка удаления
        self.del_img = tk.PhotoImage(file='./img/delete.png')
        btn_del_dialog = tk.Button(toolbar, bg='#d7d7d7', bd=0,
                                   image = self.del_img,
                                   command=self.delete_record)
        btn_del_dialog.pack(side=tk.LEFT)

        # Кнопка поиска
        self.search_img = tk.PhotoImage(file='./img/search.png')
        btn_search_dialog = tk.Button(toolbar, bg='#d7d7d7', bd=0,
                                      image = self.search_img,
                                      command=self.open_search_dialog)
        btn_search_dialog.pack(side=tk.LEFT)

        # Кнопка обновления таблицы
        self.ref_img = tk.PhotoImage(file='./img/refresh.png')
        btn_ref = tk.Button(toolbar, bg='#d7d7d7', bd=0,
                            image = self.ref_img,
                            command=self.view_records)
        btn_ref.pack(side=tk.LEFT)
        # Добавляем таблицы
        self.tree = ttk.Treeview(self,
                                 columns=['ID', 'Name', 'Phone', 'Email', 'Salary'],
                                 height=45,
                                 show='headings')

        # Добавить параметры колонок
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('Name', width=200, anchor=tk.CENTER)
        self.tree.column('Phone', width=150, anchor=tk.CENTER)
        self.tree.column('Email', width=150, anchor=tk.CENTER)
        self.tree.column('Salary', width=100, anchor=tk.CENTER)
        # Задаём подписи таблицы
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='ФИО')
        self.tree.heading('Phone', text='Телефон')
        self.tree.heading('Email', text='E-mail')
        self.tree.heading('Salary', text='Зарплата')
        self.tree.pack(side=tk.LEFT)
        # Скроллбар
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)
    # Метод для вызова добавления новых данных в БД
    def records(self, name, phone, email, salary):
        self.db.insert_data(name, phone, email, salary)
        self.view_records()

    # Изменение данных (строки) в БД
    def update_record(self, name, phone, email, salary):
        self.db.c.execute('''UPDATE List_Of_Employees SET Name = ?,
                          Phone = ?, Email = ?,
                          Salary = ?
                          WHERE Id = ?''',
                          (name, phone, email, salary, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()
    # Удаление данных (строки) из БД
    def delete_record(self):
        for sel_row in self.tree.selection():
            self.db.c.execute('''DELETE FROM List_Of_Employees WHERE Id = ?''',
                             (self.tree.set(sel_row, '#1'),))
        self.db.conn.commit()
        self.view_records()

    # Поиск записей по ФИО
    def search_records(self, name):
        self.db.c.execute('''SELECT * FROM List_Of_Employees WHERE Name LIKE ?''', 
                          ('%'+name+'%',))
        r = self.db.c.fetchall()
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=i) for i in r]
    # Отображения данных
    def view_records(self):
        self.db.c.execute('''SELECT * FROM List_Of_Employees''')
        r = self.db.c.fetchall()
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=i) for i in r]
    # Вызов дочерних окон
    def open_dialog(self):
        Child()
    def open_update_dialog(self):
        Update()
    def open_search_dialog(self):
        Search()
# Класс дочерних окон
class Child(tk.Toplevel):

    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    # Инициализация виджетов дочернего окна
    def init_child(self):
        self.title('Добавление сотрудника')
        self.geometry('400x200+300+200')
        self.resizable(False, False)

        # Перехватываем все события
        self.grab_set()

        # Захватываем фокус
        self.focus_set

        # Создание тегов
        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=50, y=30)
        label_phone = tk.Label(self, text='Телефон:')
        label_phone.place(x=50, y=60)
        label_email = tk.Label(self, text='E-mail:')
        label_email.place(x=50, y=90)
        label_salary = tk.Label(self, text='Зарплата:')
        label_salary.place(x=50, y=120)
        # Создание строк
        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=200, y=30)
        self.entry_phone = tk.Entry(self)
        self.entry_phone.place(x=200, y=60)
        self.entry_email = tk.Entry(self)
        self.entry_email.place(x=200, y=90)
        self.entry_salary = tk.Entry(self)
        self.entry_salary.place(x=200, y=120)

        # Кнопка добавления
        self.btn_ok = tk.Button(self, text='Добавить')
        self.btn_ok.bind('<Button-1>', lambda ev: self.view.records(
            self.entry_name.get(),
            self.entry_phone.get(),
            self.entry_email.get(),
            self.entry_salary.get()))
        self.btn_ok.place(x=190, y=150)

        # Кнопка закрытия
        self.btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=275, y=150)
# Класс для обновления (изменения) данных
class Update(Child):

    def __init__(self):
        super().__init__()
        self.init_edit()
        self.db = db
        self.load_data()
    # Инициализация виджетов окна редактирования данных
    def init_edit(self):
        self.title('Редактирование данных сотрудника')
        btn_edit = tk.Button(self, text='Изменить')
        btn_edit.bind('<Button-1>', lambda ev: self.view.update_record(
            self.entry_name.get(),
            self.entry_phone.get(),
            self.entry_email.get(),
            self.entry_salary.get()))
        btn_edit.bind('<Button-1>', lambda ev: self.destroy(), add = '+')
        btn_edit.place(x=190, y=150)
        self.btn_ok.destroy()
    # Подстановка данных (старых)
    def load_data(self):
        self.db.c.execute('''SELECT * FROM List_Of_Employees WHERE Id = ?''',
                         (self.view.tree.set(self.view.tree.selection()[0], '#1')))
        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])
# Класс дочернего окна для роиска по ФИО
class Search(tk.Toplevel):

    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    # Инициализация виджетов дочернего окна для поиска
    def init_child(self):
        self.title('Поиск')
        self.geometry('300x150+50+100')
        self.resizable(False, False)

        # Перехватываем все события
        self.grab_set()

        # Захватываем фокус
        self.focus_set

        # Создание тегов
        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=50, y=50)
        # Создание строк
        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=100, y=50)

        # Кнопка поиска
        self.btn_search = tk.Button(self, text='Найти')
        self.btn_search.bind('<Button-1>', lambda ev:
                             self.view.search_records(self.entry_name.get()))
        self.btn_search.bind('<Button-1>', lambda ev: self.destroy(), add = '+')
        self.btn_search.place(x=100, y=80)

        # Кнопка закрытия
        self.btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=170, y=80)
# Класс БД
class DB:

    # Создание базы данных
    def __init__(self):
        self.conn = sqlite3.connect('123456789.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS List_Of_Employees (
                       ID INTEGER PRIMARY KEY,
                       Name TEXT, Phone TEXT,
                       Email TEXT,
                       Salary INTEGER)''')
        self.conn.commit()

    # Добавление в БД
    def insert_data(self, name, phone, email, salary):
        self.c.execute('''INSERT INTO List_Of_Employees (Name, Phone, Email, Salary)
                       VALUES (?, ?, ?, ?)''',
                       (name, phone, email, salary))
        self.conn.commit()
# Запуск приложения
if __name__=='__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Список сотрудников компании')
    root.geometry('665x450+300+200')
    root.resizable(False, False)
    root.mainloop(

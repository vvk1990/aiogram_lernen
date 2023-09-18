import sqlite3 as sq
import tkinter as tk
import datetime
import PrintList
import sys
from PyQt5 import QtWidgets

import customtkinter as ctk
import ttkbootstrap as ttkb
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter import ttk
from PIL import Image  # работа с картинками

class Main():
    def __init__(self):
        self.convert_photo = None
        self.window = ctk.CTk()
        self.window.title('Work')
        self.window.geometry('1200x800')

        # переменные для обозначения работы виджета(для предотвращения дублирования окон)
        self.frame_clients_operation = False
        self.frame_brod_operation = False
        self.aplication_frame = False
        self.permanent_applications_frame = False

        # создаём базу данных и фрейм с главными кнопками
        self.creation_bd()
        self.button()

        self.window.mainloop()

    # Главные кнопки
    def button(self):
        frame_but = ctk.CTkFrame(self.window, width=300)
        frame_but.place(relx=0.03, rely=0.05)

        but_employees = ctk.CTkButton(frame_but, text='Клиенты', command=self.clients)
        but_employees.grid(padx=5, ipady=20, pady=5, sticky='wnse')

        but_majors = ctk.CTkButton(frame_but, text='Хлеб', command=self.brod)
        but_majors.grid(ipady=20, pady=5, padx=5, sticky='wnse')

        but_formula = ctk.CTkButton(frame_but, text='Рецепты', command=self.formula_brod)
        but_formula.grid(ipady=20, pady=5, padx=5, sticky='wnse')

        but_departament = ctk.CTkButton(frame_but, text='Заявки', command=self.application)
        but_departament.grid(ipady=20, pady=5, sticky='wnse', padx=5)

        but_departament = ctk.CTkButton(frame_but, text='Постоянные заявки', command=self.permanent_applications)
        but_departament.grid(ipady=20, pady=5, sticky='wnse', padx=5)

        but_exit = ctk.CTkButton(frame_but, text='Выход', fg_color='#FA8072', command=self.window.destroy)
        but_exit.grid(ipady=10, pady=5, sticky='wnse', padx=5)

        but_finich = ctk.CTkButton(frame_but, text='Печать', fg_color='#FA8072', command=self.finich)
        but_finich.grid(ipady=10, pady=5, sticky='wnse', padx=5)

        # label отображающий реальное время
        self.lab_time = ctk.CTkLabel(frame_but)
        self.lab_time.grid(ipady=10, pady=5, sticky='wnse', padx=5)
        self.update_clock()

    # функция подбивания заявки, расхода сырья и печати
    def finich(self):
        # подключимся к базе данных и соберем информацию о заявках и распечатаем их
        # ЯРОВОЕ
        # создаём список заявок Ярового для распечатки
        list_val = []
        # подключимся к базе данных и соберем информацию и записываем её наш список,
        # но сначала считаем клиентов ярового (индекс с 1 по 13)
        conn = None
        try:

            conn = sq.connect('Works.db')
            cur = conn.cursor()
            cur.execute(f'''select Name_Clients, Батон_Сдобный,
                               Батон_Французский,
                               Хлеб_Богатырский_отрубной,
                               Хлеб_Богатырский_отрубной_круглый,
                               Хлеб_Дарк_8_злаков,
                               Хлеб_Классический_075,
                               Хлеб_Классический_050,
                               Хлеб_Классический_035,
                               Хлеб_Купеческий_заварной_с_изюмом,
                               Хлеб_Купеческий_заварной_с_тмином,
                               Хлеб_Овсяный,
                               Хлеб_Степной,
                               Хлеб_Тостовый,
                               Хлеб_Чиабатта,
                               Хлеб_Яровской_ржаной,
                               Булочка_К_чаю,
                               Булочка_С_корицей,
                               Булочка_С_корицей_и_кремом,
                               Булочка_С_чесноком,
                               Булочка_С_кунжутом_для_гамбургера,
                               Булочка_Сдобная_для_хот_дога,
                               Плетёнка_с_маком,
                               Плюшка,
                               Растегай,
                               Рогалик,
                               Рулет_с_маком,
                               Тесто_Пирожковое_охлажденное,
                               Пряники
                                from {self.name_table_application} where ClientsID < 14''')
            list_val1 = cur.fetchall()
            for val in list_val1:
                list_val.append(list(val))

            # теперь подсчитаем итог и по столбцам для проводных клиентов с инд(до 14) и запишим в наш список(list_val)
            list_sum_clients1_1 = ['итого']
            list_sum_clients1_1_dable = []
            # с помощью цикла пройдемся по столбцам, подсчитаем их суммы и запишим их в список(list_sum_clients1_1)
            for brod in self.list_name_brod2_osnov:
                cur.execute(f'''select sum ({brod}) from {self.name_table_application} where ClientsID < 14''')
                list_sum_clients1_1_dable.append(cur.fetchone())
            for i in list_sum_clients1_1_dable:
                for c in i:
                    list_sum_clients1_1.append(c)
            # запишим в список заказов для распечатки список суммы стольцов коиентов до 14 id
            list_val.append(list_sum_clients1_1)

            # считаем клиентов ярового (индекс с 14 по 21)
            cur.execute(f'''select Name_Clients, Батон_Сдобный,
                                          Батон_Французский,
                                          Хлеб_Богатырский_отрубной,
                                          Хлеб_Богатырский_отрубной_круглый,
                                          Хлеб_Дарк_8_злаков,
                                          Хлеб_Классический_075,
                                          Хлеб_Классический_050,
                                          Хлеб_Классический_035,
                                          Хлеб_Купеческий_заварной_с_изюмом,
                                          Хлеб_Купеческий_заварной_с_тмином,
                                          Хлеб_Овсяный,
                                          Хлеб_Степной,
                                          Хлеб_Тостовый,
                                          Хлеб_Чиабатта,
                                          Хлеб_Яровской_ржаной,
                                          Булочка_К_чаю,
                                          Булочка_С_корицей,
                                          Булочка_С_корицей_и_кремом,
                                          Булочка_С_чесноком,
                                          Булочка_С_кунжутом_для_гамбургера,
                                          Булочка_Сдобная_для_хот_дога,
                                          Плетёнка_с_маком,
                                          Плюшка,
                                          Растегай,
                                          Рогалик,
                                          Рулет_с_маком,
                                          Тесто_Пирожковое_охлажденное,
                                          Пряники
                                           from {self.name_table_application} where ClientsID > 13 
                                          and ClientsID < 22''')
            list_val1 = cur.fetchall()
            for val in list_val1:
                list_val.append(list(val))

            # теперь подсчитаем сумму проводных и непроводных клиентов и запишем в наш список(list_val)
            list_sum_clients1_2 = ['всего']
            list_sum_clients1_2_dable = []
            # с помощью цикла пройдемся по столбцам, подсчитаем их суммы и запишим их в список(list_sum_clients1_1)
            for brod in self.list_name_brod2_osnov:
                cur.execute(f'''select sum ({brod}) from {self.name_table_application} where ClientsID < 22''')
                list_sum_clients1_2_dable.append(cur.fetchone())
            for i in list_sum_clients1_2_dable:
                for c in i:
                    list_sum_clients1_2.append(c)
            # запишим в список заказов для распечатки список суммы стольцов колиентов проводных и не проводных id
            # до 19(после 18 идёт славгород)
            list_val.append(list_sum_clients1_2)

        except sq.Error as err:
            tk.messagebox.showerror('Ошибка бызы данных', err)
        finally:
            if conn != None:
                conn.close()
        # создаём принтер через модуль PrintList
        app = QtWidgets.QApplication(sys.argv)
        pl = PrintList.PrintList()
        # # добавляем строки из нашешго списка заявок
        pl.data = list_val
        # # програмируем ширину столбцов
        pl.columnWidths = [50, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30,
                 30, 30, 30, 30, 30, 30, 30, 30, 30]
        # # добавляем имена колонок
        pl.headers = self.list_name_brod2_osnov_print
        # # запускаем поринтер
        pl.printData()


        # СЛАВГОРОД

        # создаём список заявок Славгорода для распечатки
        list_val_slav = []
        # подключимся к базе данных и соберем информацию и записываем её наш список,
        # но сначала считаем клиентов Славгорода (индекс с 22 по 39)
        conn = None
        try:

            conn = sq.connect('Works.db')
            cur = conn.cursor()
            cur.execute(f'''select Name_Clients, Батон_Сдобный,
                                      Батон_Французский,
                                      Хлеб_Богатырский_отрубной,
                                      Хлеб_Богатырский_отрубной_круглый,
                                      Хлеб_Дарк_8_злаков,
                                      Хлеб_Классический_075,
                                      Хлеб_Классический_050,
                                      Хлеб_Классический_035,
                                      Хлеб_Купеческий_заварной_с_изюмом,
                                      Хлеб_Купеческий_заварной_с_тмином,
                                      Хлеб_Овсяный,
                                      Хлеб_Степной,
                                      Хлеб_Тостовый,
                                      Хлеб_Чиабатта,
                                      Хлеб_Яровской_ржаной,
                                      Булочка_К_чаю,
                                      Булочка_С_корицей,
                                      Булочка_С_корицей_и_кремом,
                                      Булочка_С_чесноком,
                                      Булочка_С_кунжутом_для_гамбургера,
                                      Булочка_Сдобная_для_хот_дога,
                                      Плетёнка_с_маком,
                                      Плюшка,
                                      Растегай,
                                      Рогалик,
                                      Рулет_с_маком,
                                      Тесто_Пирожковое_охлажденное,
                                      Пряники
                                       from {self.name_table_application} where ClientsID > 21 and 
                    ClientsID < 40''')
            list_val1 = cur.fetchall()
            for val in list_val1:
                list_val_slav.append(list(val))

            # теперь подсчитаем итог и по столбцам для проводных клиентов и запишим в наш список(list_val_slav)
            list_sum_clients2_1 = ['итого']
            list_sum_clients2_1_dable = []
            # с помощью цикла пройдемся по столбцам, подсчитаем их суммы и запишим их в список(list_sum_clients2_1)
            for brod in self.list_name_brod2_osnov:
                cur.execute(f'''select sum ({brod}) from {self.name_table_application} where ClientsID > 21 and 
                ClientsID < 40''')
                list_sum_clients2_1_dable.append(cur.fetchone())
            for i in list_sum_clients2_1_dable:
                for c in i:
                    list_sum_clients2_1.append(c)
            # запишим в список заказов для распечатки список суммы стольцов проводимых  колиентов до 31 id
            list_val_slav.append(list_sum_clients2_1)

            # считаем клиентов славгорода (индекс с 40 по 49)
            cur.execute(f'''select Name_Clients, Батон_Сдобный,
                                                 Батон_Французский,
                                                 Хлеб_Богатырский_отрубной,
                                                 Хлеб_Богатырский_отрубной_круглый,
                                                 Хлеб_Дарк_8_злаков,
                                                 Хлеб_Классический_075,
                                                 Хлеб_Классический_050,
                                                 Хлеб_Классический_035,
                                                 Хлеб_Купеческий_заварной_с_изюмом,
                                                 Хлеб_Купеческий_заварной_с_тмином,
                                                 Хлеб_Овсяный,
                                                 Хлеб_Степной,
                                                 Хлеб_Тостовый,
                                                 Хлеб_Чиабатта,
                                                 Хлеб_Яровской_ржаной,
                                                 Булочка_К_чаю,
                                                 Булочка_С_корицей,
                                                 Булочка_С_корицей_и_кремом,
                                                 Булочка_С_чесноком,
                                                 Булочка_С_кунжутом_для_гамбургера,
                                                 Булочка_Сдобная_для_хот_дога,
                                                 Плетёнка_с_маком,
                                                 Плюшка,
                                                 Растегай,
                                                 Рогалик,
                                                 Рулет_с_маком,
                                                 Тесто_Пирожковое_охлажденное,
                                                 Пряники
                                                  from {self.name_table_application} where ClientsID > 39 
                                                 and ClientsID < 50''')
            list_val1 = cur.fetchall()
            for val in list_val1:
                list_val_slav.append(list(val))

            # теперь подсчитаем сумму проводных и непроводных клиентов и запишем в наш список(list_val_slav)
            list_sum_clients2_1 = ['всего']
            list_sum_clients2_2_dable = []
            # с помощью цикла пройдемся по столбцам, подсчитаем их суммы и запишим их в список(list_sum_clients2_1)
            for brod in self.list_name_brod2_osnov:
                cur.execute(f'''select sum ({brod}) from {self.name_table_application}''')
                list_sum_clients2_2_dable.append(cur.fetchone())
            for i in list_sum_clients2_2_dable:
                for c in i:
                    list_sum_clients2_1.append(c)
            # запишим в список заказов для распечатки список суммы стольцов колиентов проводных и не проводных id
            # до 41
            list_val_slav.append(list_sum_clients2_1)
        except sq.Error as err:
            tk.messagebox.showerror('Ошибка бызы данных', err)
        finally:
            if conn != None:
                conn.close()

        # создаём принтер через модуль PrintList
        app = QtWidgets.QApplication(sys.argv)
        pl = PrintList.PrintList()
        # # добавляем строки из нашешго списка заявок
        pl.data = list_val_slav
        # програмируем ширину столбцов
        pl.columnWidths = [50, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30
                , 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]

        # добавляем имена колонок
        pl.headers = self.list_name_brod2_osnov_print
        # запускаем поринтер
        pl.printData()

        # создаём печатный документ для Галины Васильевны_____________________________________________________________
        list_val_dop = []
        # подключимся к базе данных и соберем информацию и записываем её наш список,
        conn = None
        try:

            conn = sq.connect('Works.db')
            cur = conn.cursor()
            cur.execute(f'''select Name_Clients,
                                       Ватрушка_с_творогом,
                                       Ватрушка_с_сыром,
                                       Ватрушка_с_конфитюром,
                                       Беляш_печеный,
                                       Кекс_классический,
                                       Кекс_шоколадный,
                                       Кулебяка,
                                       Пирог_с_капустой,
                                       Пирог_с_яблоками,
                                       Пицца_мини,
                                       Ромовая_баба,
                                       Сосиска_в_тесте from {self.name_table_application} ''')
            list_val1 = cur.fetchall()
            # если колличество хлеба в заявке не 0, тогда запишем заявку клиента в списо для печати
            for val in list_val1:
                if val[1] + val[2] + val[3] + val[4] + val[5] + val[6] + val[7] + val[8] + val[9] + val[10] + val[11]\
                        + val[12] != 0:
                    list_val_dop.append(list(val))
            # теперь подсчитаем итог и по столбцам для всех клиентов и запишим в наш список(list_val_dop)
            list_sum_clients1_1 = ['итого']
            list_sum_clients1_1_dable = []
            # с помощью цикла пройдемся по столбцам, подсчитаем их суммы и запишим их в список(list_sum_clients1_1)
            for brod in self.list_name_brod2_dop:
                cur.execute(f'''select sum ({brod}) from {self.name_table_application}''')
                list_sum_clients1_1_dable.append(cur.fetchone())
            for i in list_sum_clients1_1_dable:
                for c in i:
                    list_sum_clients1_1.append(c)
            # запишим в список заказов для распечатки список суммы стольцов
            list_val_dop.append(list_sum_clients1_1)
        except sq.Error as err:
            tk.messagebox.showerror('Ошибка бызы данных', err)
        finally:
            if conn != None:
                conn.close()


        # создаём принтер через модуль PrintList
        app = QtWidgets.QApplication(sys.argv)
        pl = PrintList.PrintList()
        # # добавляем строки из нашешго списка заявок
        pl.data = list_val_dop
        # # програмируем ширину столбцов
        pl.columnWidths = [50, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]
        # # добавляем имена колонок
        pl.headers = self.list_name_brod2_dop_print
        # # запускаем поринтер
        # pl.printData()



    def formula_brod(self):
        pass

    # функция присваивающая время label перезапуская саму себя и запускает в определенное время функцию,
    # отправляющую на печать заявки
    def update_clock(self):
        # передаём реальное время на виджет
        now = datetime.datetime.today().strftime("%H:%M:%S")
        self.lab_time.configure(text=now)
        # и если наступило 22:32:05 и сегодня не суббота, запускаем функцию, отправляющую на печать заявки
        weekday = datetime.datetime.today().strftime('%A')
        if now == '22:35:05' and weekday != 'Saturday':
            self.finich()

        self.window.after(1000, self.update_clock)

    # функция обновления данных в таблице и спинбоксе, принимающая имя таблицы базы данных
    def reset(self, name_table):
        if name_table == 'Brod':
            # очистим таблицу с хлебом
            for item in self.table_brod.get_children():
                self.table_brod.delete(item)

            # заполним обновлёнными данными таблицы ХЛЕБ нащ новый список
            list_brod2 = []
            conn = sq.connect('Works.db')
            cur = conn.cursor()
            q = '''select * from {table}'''
            cur.execute(q.format(table=name_table))
            for i in cur.fetchall():
                list_brod2.append(i)

            # заполним нашу чистую таблицу данными из нашего обновленного списка
            for row in list_brod2:
                self.table_brod.insert('', tk.END, values=row)
            conn.close()
        elif name_table == "Clients":

            # очистим таблицу с хлебом
            for item in self.table_clients.get_children():
                self.table_clients.delete(item)

            # заполним обновлёнными данными таблицы ХЛЕБ нащ новый список
            list_brod2 = []
            conn = sq.connect('Works.db')
            cur = conn.cursor()
            q = '''select * from {table}'''
            cur.execute(q.format(table=name_table))
            for i in cur.fetchall():
                list_brod2.append(i)

            # заполним нашу чистую таблицу данными из нашего обновленного списка
            for row in list_brod2:
                self.table_clients.insert('', tk.END, values=row)
            conn.close()

    # ФОТО
    def add_photo(self):
        filename = fd.askopenfilename()
        self.convert_photo = self.convert_photo_binar(filename)
    def convert_photo_binar(self, filename):
        with open(filename, 'rb') as file:
            blob_data = file.read()
        return blob_data
    def open_old_photo(self):
        self.photo_old_phormate_blod = None
        id_brod = self.entry_change_id_brod.get()
        # из базы данных достаём по ID фото в формате blob
        conn = sq.connect('Works.db')
        cur = conn.cursor()
        cur.execute('''select Фото from Brod where ХлебID == ?''', (id_brod,))
        for i in cur.fetchone():
            self.photo_old_phormate_blod = i
        conn.close()
        # создаём файл и помещаем в него фото из базы данных
        with open('old_photo.jpg', 'wb') as file:
            file.write(self.photo_old_phormate_blod)
        # открываем фото и показываем его
        image = Image.open("old_photo.jpg")
        image.show()

    # Заявки
    def application(self):

        # система закрытия окон

        if self.frame_clients_operation == True:
            self.frame2_change_clients.destroy()
            self.frame_table_clients.destroy()
            self.frame3_but.destroy()
            self.frame_clients_operation = False
        if self.frame_brod_operation == True:
            self.frame2_change_brod.destroy()
            self.frame_table_brod.destroy()
            self.frame3_but_brod.destroy()
            self.frame_brod_operation = False
        if self.permanent_applications_frame == True:
            self.frame_permanent_applications.destroy()
            self.frame2_permanent_applications.destroy()
            self.permanent_applications_frame = False

        if self.aplication_frame == False:
            self.aplication_frame = True

            # создаём фрейм для расположение в нем виджетов для заполнения заявки
            self.frame1_aplication_brod = ctk.CTkFrame(self.window)
            self.frame1_aplication_brod.place(relx=0.35, rely=0.05)

            # self.lab_change_client = ctk.CTkLabel(self.frame1_aplication_brod, text='Клиенты: ')
            # self.lab_change_client.grid(row=0, column=0, sticky='wens', pady=5, padx=5)

            # заполняем список клиентов из таблицы и запихиваем ешо в комбобокс
            self.list_clients = []
            conn = sq.connect('Works.db')
            cur = conn.cursor()
            cur.execute('''select * from Clients''')
            for i in cur.fetchall():
                self.list_clients.append(i[1])
            conn.close()

            # создаём лейблы и ентрю для заявок через цикл присваивая им имя хлеба из цикла
            row = 1
            row2 = 1
            # создаём список нащих энтрю для возможности обратится к ним для извлечение информации
            self.entry_list_aplication_brod = []
            for name_brod in self.list_name_brod:
                if row <= 20:
                    self.label = ctk.CTkLabel(self.frame1_aplication_brod, text=f'{row}) {name_brod}', anchor='w',
                                              fg_color='#D3D3D3', text_color='#000000')
                    self.label.grid(row=row, column=0, sticky='wens', pady=5, padx=5)

                    self.entry_brod = ctk.CTkEntry(self.frame1_aplication_brod, width=50)
                    self.entry_brod.insert(0, 0)
                    self.entry_brod.grid(row=row, column=1, sticky='wens', pady=5, padx=5)

                    self.entry_list_aplication_brod.append(self.entry_brod)
                    row += 1
                else:
                    self.label_name_brod = ctk.CTkLabel(self.frame1_aplication_brod, text=f'{row}) {name_brod}', anchor='w',
                                                        fg_color='#D3D3D3', text_color='#000000')
                    self.label_name_brod.grid(row=row2, column=2, sticky='wens', pady=5, padx=5)

                    self.entry_brod = ctk.CTkEntry(self.frame1_aplication_brod, width=50)
                    self.entry_brod.insert(0, 0)
                    self.entry_brod.grid(row=row2, column=3, sticky='wens', pady=5, padx=5)

                    self.entry_list_aplication_brod.append(self.entry_brod)
                    row += 1
                    row2 += 1

            # создаём фрейм для календаря и кнопок(добавить, изменить удалить)
            self.frame_aplication_bot = ctk.CTkFrame(self.window)
            self.frame_aplication_bot.place(relx=0.168, rely=0.05)

            # календарь(отображается дата следующего дня)
            self.cal_date = ttkb.DateEntry(self.frame_aplication_bot, firstweekday=0, dateformat='day_%d_%m_%y',
                                           startdate=datetime.datetime.now() + datetime.timedelta(days=1), width=17)
            self.cal_date.grid(pady=5, padx=5)

            # # ещё один календарь
            # self.cal = ttk. (self.frame_aplication_bot, year=2023, selectmode='day')
            # self.cal.grid()

            # клиенты в комбобоксе
            self.combobox_employees = ctk.CTkComboBox(self.frame_aplication_bot, values=self.list_clients, )
            self.combobox_employees.grid(sticky='wens', pady=5, padx=5)
            # кнопка показать
            self.chou_aplication = ctk.CTkButton(self.frame_aplication_bot, text='Показать', fg_color='#3CB371',
                                                 command=self.chou_but_aplication)
            self.chou_aplication.grid(pady=5, padx=5, sticky='wnse')
            # кнопка сохранить
            self.but_add_aplication = ctk.CTkButton(self.frame_aplication_bot, text='Сохранить',
                                                    command=self.save_aplication)
            self.but_add_aplication.grid(pady=5, padx=5, ipady=10, sticky='wnse')
            # кнопка удалить
            self.but_add_aplication = ctk.CTkButton(self.frame_aplication_bot, text='Удалить', fg_color='#A52A2A',
                                                    command=self.del_aplication)
            self.but_add_aplication.grid(pady=5, padx=5, sticky='wnse')

    def chou_but_aplication(self):
        # получаем имя клиента из комбобокса
        name_clients = self.combobox_employees.get()
        # получаем название таблицы из календаря
        name_table = self.cal_date.entry.get()
        # получаем данные из таблицы по этому клиенту
        conn = None
        try:
            conn = sq.connect('Works.db')
            cur = conn.cursor()
            cur.execute(f'''select * from {name_table} where Name_Clients == ?''', (name_clients,))
            value = cur.fetchall()
            list_val = []
            # выгружаем данные кортежа в список
            for i in value:
                for val in i:
                    list_val.append(val)
            # сообщим если такой заявки нет
            if len(list_val) == 0:
                messagebox.showinfo(f'Заявка для {name_clients}',
                                    f'Заявки на {name_table} для клиента {name_clients} не существует!')
            # если такая заявка есть то:
            else:
                # очистим наши entry перед заполнением их данными
                for val in self.entry_list_aplication_brod:
                    val.delete(0, ctk.END)
                # заполняем наши entry из списка с данными
                i = 2
                for entry in self.entry_list_aplication_brod:
                    entry.insert(0, list_val[i])
                    i += 1
        except sq.Error as err:
            tk.messagebox.showerror('Ошибка бызы данных', err)
        finally:
            if conn != None:
                conn.close()

        pass

    def save_aplication(self):
        # считаем информацию из всех столбцов и сохраним её в список к которому будем обращаться через индексы
        list_aplication = []
        for data in self.entry_list_aplication_brod:
            list_aplication.append(int(data.get()))
        # получим имя клиента и его индекс
        # имя
        name_clients = self.combobox_employees.get()
        # индекс
        conn = sq.connect('Works.db')
        cur = conn.cursor()
        cur.execute('''select ClientsID from Clients where Name == ?''', (name_clients,))
        id_clients = ''
        for i in cur.fetchone():
            id_clients = i
        conn.close()

        # создадим таблицу для основной заявки если её ещё нет, имя таблицы берём из виджета календарь
        name_table = self.cal_date.entry.get()
        conn = None
        try:
            conn = sq.connect('Works.db')
            cur = conn.cursor()
            cur.execute(f'''CREATE TABLE IF NOT EXISTS {name_table}(
                                                                    ClientsID INTEGER PRIMARY KEY NOT NULL,
                                                                    Name_Clients text,
                                                                    Батон_Сдобный integer,
                                                                    Батон_Французский integer,
                                                                    Хлеб_Богатырский_отрубной integer,
                                                                    Хлеб_Богатырский_отрубной_круглый integer,
                                                                    Хлеб_Дарк_8_злаков integer,
                                                                    Хлеб_Классический_075 integer,
                                                                    Хлеб_Классический_050 integer,
                                                                    Хлеб_Классический_035 integer,
                                                                    Хлеб_Купеческий_заварной_с_изюмом integer,
                                                                    Хлеб_Купеческий_заварной_с_тмином integer,
                                                                    Хлеб_Овсяный integer,
                                                                    Хлеб_Степной integer,
                                                                    Хлеб_Тостовый integer,
                                                                    Хлеб_Чиабатта integer,
                                                                    Хлеб_Яровской_ржаной integer,
                                                                    Булочка_К_чаю integer,
                                                                    Булочка_С_корицей integer,
                                                                    Булочка_С_корицей_и_кремом integer,
                                                                    Булочка_С_чесноком integer,
                                                                    Булочка_С_кунжутом_для_гамбургера integer,
                                                                    Булочка_Сдобная_для_хот_дога integer,
                                                                    Плетёнка_с_маком integer,
                                                                    Плюшка integer,
                                                                    Растегай integer,
                                                                    Рогалик integer,
                                                                    Рулет_с_маком integer,
                                                                    Тесто_Пирожковое_охлажденное integer,
                                                                    Пряник integer,
                                                                    Ватрушка_с_творогом integer,
                                                                            Ватрушка_с_сыром integer,
                                                                            Ватрушка_с_конфитюром integer,
                                                                            Беляш_печеный integer,
                                                                            Кекс_классический integer,
                                                                            Кекс_шоколадный integer,
                                                                            Кулебяка integer,
                                                                            Пирог_с_капустой integer,
                                                                            Пирог_с_яблоками integer,
                                                                            Пицца_мини integer,
                                                                            Ромовая_баба integer,
                                                                            Сосиска_в_тесте integer
                                                                    )''')

            conn.commit()

        except sq.Error as err:
            tk.messagebox.showerror('Ошибка бызы данных', err)

        finally:
            if conn != None:
                conn.close()

        # создадим список в который поместим индексы организаций уже сделавших заявку на этот день
        list_clients_aplication1 = []
        list_clients_aplication2 = []
        # залезием в базу данных и запросим индексы организаций которые уже сделали заявку на этот день
        conn = None
        try:
            conn = sq.connect('Works.db')
            cur = conn.cursor()
            cur.execute(f'''select ClientsID from {name_table}''')
            for i in cur.fetchall():
                list_clients_aplication1.append(i)
            for i in list_clients_aplication1:
                for val in i:
                    list_clients_aplication2.append(val)

            # открываем базу данных и записываем данные из списка заявок в таблицу заявок
            if id_clients in list_clients_aplication2:
                x = messagebox.askyesno('Перезапись заявки', f'Вы точно хотите исправить заявку '
                                                             f'на {name_table} для {name_clients}')
                if x == True:
                    cur.execute(f'''UPDATE {name_table} 
                                    set 
                                                                        Батон_Сдобный = ?,
                                                                        Батон_Французский = ?,
                                                                        Хлеб_Богатырский_отрубной = ?,
                                                                        Хлеб_Богатырский_отрубной_круглый = ?,
                                                                        Хлеб_Дарк_8_злаков = ?,
                                                                               Хлеб_Классический_075 = ?,
                                                                               Хлеб_Классический_050 = ?,
                                                                               Хлеб_Классический_035 = ?,
                                                                               Хлеб_Купеческий_заварной_с_изюмом = ?,
                                                                               Хлеб_Купеческий_заварной_с_тмином = ?,
                                                                               Хлеб_Овсяный = ?,
                                                                               Хлеб_Степной = ?,
                                                                               Хлеб_Тостовый = ?,
                                                                               Хлеб_Чиабатта = ?,
                                                                               Хлеб_Яровской_ржаной = ?,
                                                                               Булочка_К_чаю = ?,
                                                                               Булочка_С_корицей = ?,
                                                                               Булочка_С_корицей_и_кремом = ?,
                                                                               Булочка_С_чесноком = ?,
                                                                               Булочка_С_кунжутом_для_гамбургера = ?,
                                                                               Булочка_Сдобная_для_хот_дога = ?,
                                                                               Плетёнка_с_маком = ?,
                                                                               Плюшка = ?,
                                                                               Растегай = ?,
                                                                               Рогалик = ?,
                                                                               Рулет_с_маком = ?,
                                                                               Тесто_Пирожковое_охлажденное = ?,
                                                                               Пряники =?,
                                                                               Ватрушка_с_творогом = ?,
                                                                               Ватрушка_с_сыром = ?,
                                                                               Ватрушка_с_конфитюром = ?,
                                                                               Беляш_печеный = ?,
                                                                               Кекс_классический = ?,
                                                                               Kekc_шоколадный = ?,
                                                                               Кулебяка = ?,
                                                                               Пирог_с_капустой = ?,
                                                                               Пирог_с_яблоками = ?,
                                                                               Пицца_мини = ?,
                                                                               Ромовая_баба = ?,
                                                                               Сосиска_в_тесте = ?
                                    where ClientsID == ?''', (list_aplication[0], list_aplication[1], list_aplication[2]
                                 , list_aplication[3], list_aplication[4], list_aplication[5], list_aplication[6]
                                 , list_aplication[7], list_aplication[8], list_aplication[9], list_aplication[10]
                                 , list_aplication[11], list_aplication[12], list_aplication[13], list_aplication[14]
                                 , list_aplication[15], list_aplication[16], list_aplication[17], list_aplication[18]
                                 , list_aplication[19], list_aplication[20], list_aplication[21], list_aplication[22]
                                 , list_aplication[23], list_aplication[24], list_aplication[25], list_aplication[26]
                                 , list_aplication[27], list_aplication[28], list_aplication[29],list_aplication[28],
                                    list_aplication[29],list_aplication[30], list_aplication[31], list_aplication[32],
                                    list_aplication[33], list_aplication[34], list_aplication[35], list_aplication[36],
                                    list_aplication[37], list_aplication[38], list_aplication[39]
                                                              , id_clients))
                    conn.commit()
                    messagebox.showinfo('Заявка на хлеб', f'Заявка на {name_table} для {name_clients} успешно перезаписана!')
            else:
                cur.execute(f'''insert into {name_table} (
                                                                               ClientsID,
                                                                               Name_Clients,
                                                                               Батон_Сдобный,
                                                                               Батон_Французский,
                                                                               Хлеб_Богатырский_отрубной,
                                                                               Хлеб_Богатырский_отрубной_круглый,
                                                                               Хлеб_Дарк_8_злаков,
                                                                               Хлеб_Классический_075,
                                                                               Хлеб_Классический_050,
                                                                               Хлеб_Классический_035,
                                                                               Хлеб_Купеческий_заварной_с_изюмом,
                                                                               Хлеб_Купеческий_заварной_с_тмином,
                                                                               Хлеб_Овсяный,
                                                                               Хлеб_Степной,
                                                                               Хлеб_Тостовый,
                                                                               Хлеб_Чиабатта,
                                                                               Хлеб_Яровской_ржаной,
                                                                               Булочка_К_чаю,
                                                                               Булочка_С_корицей,
                                                                               Булочка_С_корицей_и_кремом,
                                                                               Булочка_С_чесноком,
                                                                               Булочка_С_кунжутом_для_гамбургера,
                                                                               Булочка_Сдобная_для_хот_дога,
                                                                               Плетёнка_с_маком,
                                                                               Плюшка,
                                                                               Растегай,
                                                                               Рогалик,
                                                                               Рулет_с_маком,
                                                                               Тесто_Пирожковое_охлажденное,
                                                                               Пряники,
                                                                               Ватрушка_с_творогом,
                                                                                    Ватрушка_с_сыром,
                                                                                    Ватрушка_с_конфитюром,
                                                                                   Беляш_печеный,
                                                                                   Кекс_классический,
                                                                                   Кекс_шоколадный,
                                                                                   Кулебяка,
                                                                                   Пирог_с_капустой,
                                                                                   Пирог_с_яблоками,
                                                                                   Пицца_мини,
                                                                                   Ромовая_баба,
                                                                                   Сосиска_в_тесте
                                                                               )
                    values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                                (id_clients, name_clients, list_aplication[0], list_aplication[1], list_aplication[2]
                                 , list_aplication[3], list_aplication[4], list_aplication[5], list_aplication[6]
                                 , list_aplication[7], list_aplication[8], list_aplication[9], list_aplication[10]
                                 , list_aplication[11], list_aplication[12], list_aplication[13], list_aplication[14]
                                 , list_aplication[15], list_aplication[16], list_aplication[17], list_aplication[18]
                                 , list_aplication[19], list_aplication[20], list_aplication[21], list_aplication[22]
                                 , list_aplication[23], list_aplication[24], list_aplication[25], list_aplication[26]
                                 , list_aplication[27], list_aplication[28], list_aplication[29], list_aplication[30]
                                 , list_aplication[31], list_aplication[32], list_aplication[33], list_aplication[34]
                                 , list_aplication[35], list_aplication[36], list_aplication[37], list_aplication[38]
                                 , list_aplication[39]))

                conn.commit()
                messagebox.showinfo('Заявка на хлеб', f'Заявка на {name_table} для {name_clients} успешно создана!')
        except sq.Error as err:
            tk.messagebox.showerror('Ошибка бызы данных', err)

        finally:
            if conn != None:
                conn.close()

    def del_aplication(self):
        # получаем имя клиента
        name_clients = self.combobox_employees.get()
        # получаем название таблицы из календаря
        name_table = self.cal_date.entry.get()
        # удостоверимся что мы точно хотим удалить этот заказ
        x = messagebox.askyesno('Удаление заявки клиена', f'Вы точно хотите удалить заявку от {name_table}'
                                                          f'  клиента {name_clients} ?')

        # открываем базу данных и удаляем из таблицы заявку нашего клиента
        conn = None
        try:
            conn = sq.connect('Works.db')
            cur = conn.cursor()

            # прописываем условия:
            if x == True:
                cur.execute(f'''Delete from {name_table}
                                             where Name_Clients == ?''', (name_clients,))
                conn.commit()

        except sq.Error as err:
            tk.messagebox.showerror('Ошибка бызы данных', err)
        finally:
            if conn != None:
                conn.close()
        # удалим все данные из entry и запишем туда нули
        # очистим наши entry перед заполнением их данными
        for val in self.entry_list_aplication_brod:
            val.delete(0, ctk.END)
        # заполняем наши entry нулями
        for entry in self.entry_list_aplication_brod:
            entry.insert(0, 0)

    # Постоянные заявки
    def permanent_applications(self):
        # система закрытия окон
        if not self.permanent_applications_frame:
            self.permanent_applications_frame = True
            if self.frame_clients_operation:
                self.frame2_change_clients.destroy()
                self.frame_table_clients.destroy()
                self.frame3_but.destroy()
                self.frame_clients_operation = False
            if self.frame_brod_operation:
                self.frame2_change_brod.destroy()
                self.frame_table_brod.destroy()
                self.frame3_but_brod.destroy()
                self.frame_brod_operation = False
            if self.aplication_frame:
                self.frame1_aplication_brod.destroy()
                self.frame_aplication_bot.destroy()
                self.aplication_frame = False

            # создаём фрейм для расположение в нем виджетов для заполнения заявки
            self.frame_permanent_applications = ctk.CTkFrame(self.window)
            self.frame_permanent_applications.place(relx=0.35, rely=0.05)

            # заполняем список клиентов из таблицы и запихиваем его в комбобокс
            self.list_clients = []
            conn = sq.connect('Works.db')
            cur = conn.cursor()
            cur.execute('''select * from Clients''')
            for i in cur.fetchall():
                self.list_clients.append(i[1])
            conn.close()

            # создаём лейблы и ентрю для заявок через цикл присваивая им имя хлеба из цикла
            row = 1
            row2 = 1
            # создаём список нащих энтрю для возможности обратится к ним для извлечение информации
            self.entry_list_permanent_aplication_brod = []
            for name_brod in self.list_name_brod:
                if row <= 20:
                    self.label = ctk.CTkLabel(self.frame_permanent_applications, text=f'{row}) {name_brod}', anchor='w',
                                              fg_color='#D3D3D3', text_color='#000000')
                    self.label.grid(row=row, column=0, sticky='wens', pady=5, padx=5)

                    self.entry_brod = ctk.CTkEntry(self.frame_permanent_applications, width=50)
                    self.entry_brod.insert(0, 0)
                    self.entry_brod.grid(row=row, column=1, sticky='wens', pady=5, padx=5)

                    self.entry_list_permanent_aplication_brod.append(self.entry_brod)
                    row += 1
                else:
                    self.label_name_brod = ctk.CTkLabel(self.frame_permanent_applications, text=f'{row}) {name_brod}',
                                                        anchor='w', fg_color='#D3D3D3', text_color='#000000')
                    self.label_name_brod.grid(row=row2, column=2, sticky='wens', pady=5, padx=5)

                    self.entry_brod = ctk.CTkEntry(self.frame_permanent_applications, width=50)
                    self.entry_brod.insert(0, 0)
                    self.entry_brod.grid(row=row2, column=3, sticky='wens', pady=5, padx=5)

                    self.entry_list_permanent_aplication_brod.append(self.entry_brod)
                    row += 1
                    row2 += 1
            # создаём фрейм для кнопок(клиенты,показать, сохранить, удалить)
            self.frame2_permanent_applications = ctk.CTkFrame(self.window, width=200)
            self.frame2_permanent_applications.place(relx=0.165, rely=0.05 )

            # комбобокс с днями недели
            self.list_day_week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
            self.combobox_day_week_permanent_applications = ctk.CTkComboBox(self.frame2_permanent_applications,
                                                                             values=self.list_day_week, width=200)
            self.combobox_day_week_permanent_applications.grid(pady=5, padx=5)

            # клиенты в комбобоксе
            self.combobox_employees_permanent_applications = ctk.CTkComboBox(self.frame2_permanent_applications,
                                                                             values=self.list_clients, width=200)
            self.combobox_employees_permanent_applications.grid(pady=5, padx=5)
            # кнопка показать
            self.chou_permanent_applications = ctk.CTkButton(self.frame2_permanent_applications, text='Показать',
                                                             fg_color='#3CB371', width=200,
                                                             command=self.chou_but_permanent_applications)
            self.chou_permanent_applications.grid(pady=5, padx=5)
            # кнопка сохранить
            self.but_add_permanent_applications = ctk.CTkButton(self.frame2_permanent_applications, text='Сохранить',
                                                                width=200,
                                                                command=self.save_permanent_applications)
            self.but_add_permanent_applications.grid(pady=5, padx=5, ipady=10)
            # кнопка очистить
            self.but_clear_permanent_applications = ctk.CTkButton(self.frame2_permanent_applications, text='Очистить',
                                                                  width=200,
                                                                  command=self.clear_permanent_applications)
            self.but_clear_permanent_applications.grid(pady=5, padx=5, ipady=10,)
            # кнопка удалить
            self.but_del_permanent_applications = ctk.CTkButton(self.frame2_permanent_applications, text='Удалить',
                                                                fg_color='#A52A2A', width=200,
                                                                command=self.del_permanent_applications)
            self.but_del_permanent_applications.grid(pady=5, padx=5)
    def clear_permanent_applications(self):
        # пройдёмся по сриску и присвоим каждому фрейму значение 0
        # очистим наши entry перед заполнением их данными
        for val in self.entry_list_permanent_aplication_brod:
            val.delete(0, ctk.END)
        # заполняем наши entry нулями
        for entry in self.entry_list_permanent_aplication_brod:
            entry.insert(0, 0)

    def chou_but_permanent_applications(self):
        # получаем имя клиента из комбобокса
        name_clients = self.combobox_employees_permanent_applications.get()
        # получаем день недели
        day_week = self.combobox_day_week_permanent_applications.get()
        # получаем данные из таблицы нужного нам дня недели по нужному нам клиенту
        conn = None
        try:
            conn = sq.connect('Works.db')
            cur = conn.cursor()
            cur.execute(f'''select * from {day_week} where Name_Clients == ?''', (name_clients,))
            value = cur.fetchall()
            list_val = []
            # выгружаем данные кортежа в список
            for i in value:
                for val in i:
                    list_val.append(val)
            # сообщим если такой заявки нет
            if len(list_val) == 0:
                messagebox.showinfo(f'Постоянная заявка для {name_clients}',
                                    f'Постоянной заявки для клиента {name_clients} в {day_week} не существует!')
            # если такая заявка есть то:
            else:
                # очистим наши entry перед заполнением их данными
                for val in self.entry_list_permanent_aplication_brod:
                    val.delete(0, ctk.END)
                # заполняем наши entry из списка с данными
                i = 2
                for entry in self.entry_list_permanent_aplication_brod:
                    entry.insert(0, list_val[i])
                    i += 1
        except sq.Error as err:
            tk.messagebox.showerror('Ошибка бызы данных', err)
        finally:
            if conn != None:
                conn.close()

    def save_permanent_applications(self):
        # считаем информацию из всех столбцов и сохраним её в список к которому будем обращаться через индексы
        list_aplication = []
        for data in self.entry_list_permanent_aplication_brod:
            list_aplication.append(int(data.get()))
        # получим имя клиента и его индекс
        # имя
        name_clients = self.combobox_employees_permanent_applications.get()
        # индекс
        conn = sq.connect('Works.db')
        cur = conn.cursor()
        cur.execute('''select ClientsID from Clients where Name == ?''', (name_clients,))
        id_clients = ''
        for i in cur.fetchone():
            id_clients = i
        conn.close()

        # запишим данные в нашу таблицу постоянных заявок
        # присвоим переменной имя нужной таблицы из комбобокса
        # и пропишем условия если заявка уже существует
        # Получим из базы данных индексы клиентов с постоянной заявкой в этот день

        conn = sq.connect('Works.db')
        cur = conn.cursor()
        cur.execute(f'''select ClientsID from {self.combobox_day_week_permanent_applications.get()}''')
        id_clientse = []
        for i in cur.fetchall():
            for c in i:
                id_clientse.append(c)
        conn.close()

        if id_clients not in id_clientse:


            name_table = self.combobox_day_week_permanent_applications.get()
            conn = None
            try:
                conn = sq.connect('Works.db')
                cur = conn.cursor()
                cur.execute(f'''insert into {name_table}(
                                                                           ClientsID,
                                                                           Name_Clients,
                                                                           Батон_Сдобный,
                                                                           Батон_Французский,
                                                                           Хлеб_Богатырский_отрубной,
                                                                           Хлеб_Богатырский_отрубной_круглый,
                                                                           Хлеб_Дарк_8_злаков,
                                                                           Хлеб_Классический_075,
                                                                           Хлеб_Классический_050,
                                                                           Хлеб_Классический_035,
                                                                           Хлеб_Купеческий_заварной_с_изюмом,
                                                                           Хлеб_Купеческий_заварной_с_тмином,
                                                                           Хлеб_Овсяный,
                                                                           Хлеб_Степной,
                                                                           Хлеб_Тостовый,
                                                                           Хлеб_Чиабатта,
                                                                           Хлеб_Яровской_ржаной,
                                                                           Булочка_К_чаю,
                                                                           Булочка_С_корицей,
                                                                           Булочка_С_корицей_и_кремом,
                                                                           Булочка_С_чесноком,
                                                                           Булочка_С_кунжутом_для_гамбургера,
                                                                           Булочка_Сдобная_для_хот_дога,
                                                                           Плетёнка_с_маком,
                                                                           Плюшка,
                                                                           Растегай,
                                                                           Рогалик,
                                                                           Рулет_с_маком,
                                                                           Тесто_Пирожковое_охлажденное,
                                                                           Пряники,
                                                                           Ватрушка_с_творогом,
                                                                           Ватрушка_с_сыром,
                                                                           Ватрушка_с_конфитюром,
                                                                           Беляш_печеный,
                                                                           Кекс_классический,
                                                                           Кекс_шоколадный,
                                                                           Кулебяка,
                                                                           Пирог_с_капустой,
                                                                           Пирог_с_яблоками,
                                                                           Пицца_мини,
                                                                           Ромовая_баба,
                                                                           Сосиска_в_тесте)
                                                                           
                values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                            (id_clients, name_clients, list_aplication[0], list_aplication[1], list_aplication[2]
                             , list_aplication[3], list_aplication[4], list_aplication[5], list_aplication[6]
                             , list_aplication[7], list_aplication[8], list_aplication[9], list_aplication[10]
                             , list_aplication[11], list_aplication[12], list_aplication[13], list_aplication[14]
                             , list_aplication[15], list_aplication[16], list_aplication[17], list_aplication[18]
                             , list_aplication[19], list_aplication[20], list_aplication[21], list_aplication[22]
                             , list_aplication[23], list_aplication[24], list_aplication[25], list_aplication[26]
                             , list_aplication[27], list_aplication[28], list_aplication[29], list_aplication[30]
                             , list_aplication[31], list_aplication[32], list_aplication[33], list_aplication[34]
                             , list_aplication[35], list_aplication[36], list_aplication[37],list_aplication[38],
                             list_aplication[39]))

                conn.commit()

            except sq.Error as err:
                tk.messagebox.showerror('Ошибка бызы данных', err)

            finally:
                if conn != None:
                    conn.close()
            # напишем сообщеение что постоянная заявка сохранена
            messagebox.showinfo('Сохранение постоянной заявки',
                                f'Постоянная заявка в {self.combobox_day_week_permanent_applications.get()} '
                                f'для клиента {name_clients} успешно сохранена')
        else:
            name_table = self.combobox_day_week_permanent_applications.get()
            conn = None
            try:
                conn = sq.connect('Works.db')
                cur = conn.cursor()
                cur.execute(f'''update {name_table}
                                                                                       
                                                                                
                                                                          set          Батон_Сдобный == ?,
                                                                                       Батон_Французский == ?,
                                                                                       Хлеб_Богатырский_отрубной == ?,
                                                                                       Хлеб_Богатырский_отрубной_круглый == ?,
                                                                                       Хлеб_Дарк_8_злаков == ?,
                                                                                       Хлеб_Классический_075 == ?,
                                                                                       Хлеб_Классический_050 == ?,
                                                                                       Хлеб_Классический_035 == ?,
                                                                                       Хлеб_Купеческий_заварной_с_изюмом == ?,
                                                                                       Хлеб_Купеческий_заварной_с_тмином == ?,
                                                                                       Хлеб_Овсяный == ?,
                                                                                       Хлеб_Степной == ?,
                                                                                       Хлеб_Тостовый == ?,
                                                                                       Хлеб_Чиабатта == ?,
                                                                                       Хлеб_Яровской_ржаной == ?,
                                                                                       Булочка_К_чаю == ?,
                                                                                       Булочка_С_корицей == ?,
                                                                                       Булочка_С_корицей_и_кремом == ?,
                                                                                       Булочка_С_чесноком == ?,
                                                                                       Булочка_С_кунжутом_для_гамбургера == ?,
                                                                                       Булочка_Сдобная_для_хот_дога == ?,
                                                                                       Плетёнка_с_маком == ?,
                                                                                       Плюшка == ?,
                                                                                       Растегай == ?,
                                                                                       Рогалик == ?,
                                                                                       Рулет_с_маком == ?,
                                                                                       Тесто_Пирожковое_охлажденное == ?,
                                                                                       Ватрушка_с_творогом == ?,
                                                                                       Ватрушка_с_сыром == ?,
                                                                                       Ватрушка_с_конфитюром == ?,
                                                                                       Беляш_печеный == ?,
                                                                                       Кекс_классический == ?,
                                                                                       Кулебяка == ?,
                                                                                       Пирог_с_капустой == ?,
                                                                                       Пирог_с_яблоками == ?,
                                                                                       Пицца_мини == ?,
                                                                                       Ромовая_баба == ?,
                                                                                       Сосиска_в_тесте == ?
                                                                            where CLientsID == ?

                            ''',
                            (list_aplication[0], list_aplication[1], list_aplication[2]
                             , list_aplication[3], list_aplication[4], list_aplication[5], list_aplication[6]
                             , list_aplication[7], list_aplication[8], list_aplication[9], list_aplication[10]
                             , list_aplication[11], list_aplication[12], list_aplication[13], list_aplication[14]
                             , list_aplication[15], list_aplication[16], list_aplication[17], list_aplication[18]
                             , list_aplication[19], list_aplication[20], list_aplication[21], list_aplication[22]
                             , list_aplication[23], list_aplication[24], list_aplication[25], list_aplication[26]
                             , list_aplication[27], list_aplication[28], list_aplication[29], list_aplication[30]
                             , list_aplication[31], list_aplication[32], list_aplication[33], list_aplication[34]
                             , list_aplication[35], list_aplication[36], list_aplication[37], id_clients))

                conn.commit()

            except sq.Error as err:
                tk.messagebox.showerror('Ошибка бызы данных', err)

            finally:
                if conn != None:
                    conn.close()
            # напишем сообщеение что постоянная заявка сохранена
            messagebox.showinfo('Сохранение постоянной заявки',
                                f'Постоянная заявка в {self.combobox_day_week_permanent_applications.get()} '
                                f'для клиента {name_clients} успешно пересохранена')


    def del_permanent_applications(self):
        # получаем имя клиента
        name_clients = self.combobox_employees_permanent_applications.get()
        # получаем имя таблицы
        name_table = self.combobox_day_week_permanent_applications.get()
        # удостоверимся что мы точно хотим удалить этот заказ
        x = messagebox.askyesno('Удаление постоянной заявки клиента', f'Вы точно хотите удалить постоянную заявку '
                                                                      f'клиента {name_clients} ?')

        # открываем базу данных и удаляем из таблицы заявку нашего клиента
        conn = None
        try:
            conn = sq.connect('Works.db')
            cur = conn.cursor()

            # прописываем условия:
            if x == True:
                cur.execute(f'''Delete from {name_table}
                                             where Name_Clients == ?''', (name_clients,))
                conn.commit()

        except sq.Error as err:
            tk.messagebox.showerror('Ошибка бызы данных', err)
        finally:
            if conn != None:
                conn.close()
        # удалим все данные из entry и запишем туда нули
        # очистим наши entry перед заполнением их данными
        for val in self.entry_list_permanent_aplication_brod:
            val.delete(0, ctk.END)
        # заполняем наши entry нулями
        for entry in self.entry_list_permanent_aplication_brod:
            entry.insert(0, 0)



    # ХЛЕБ
    def brod(self):
        # система закрытия окон
        if self.frame_clients_operation:
            self.frame_table_clients.destroy()
            self.frame2_change_clients.destroy()
            self.frame3_but.destroy()
            self.frame_clients_operation = False
        if self.aplication_frame:
            self.frame1_aplication_brod.destroy()
            self.frame_aplication_bot.destroy()
            self.aplication_frame = False
        if self.permanent_applications_frame:
            self.frame_permanent_applications.destroy()
            self.frame2_permanent_applications.destroy()
            self.permanent_applications_frame = False

        if not self.frame_brod_operation:
            self.frame_brod_operation = True

            # создаём фрейм для расположения в нем виджетов
            self.frame2_change_brod = ctk.CTkFrame(self.window)
            self.frame2_change_brod.place(relx=0.2, rely=0.55)

            self.lab_change_brod = ctk.CTkLabel(self.frame2_change_brod, text='ID: ')
            self.lab_change_brod.grid(row=0, column=0, sticky='wens', pady=5, padx=3, ipady=3)

            self.var_entry_chenge_id_brod = ctk.StringVar()
            self.entry_change_id_brod = ctk.CTkEntry(self.frame2_change_brod, width=65,
                                                       textvariable=self.var_entry_chenge_id_brod)
            self.entry_change_id_brod.grid(row=0, column=1, pady=5, padx=5, ipady=3)


            self.lab_change_name_brod = ctk.CTkLabel(self.frame2_change_brod, text='Название: ')
            self.lab_change_name_brod.grid(row=0, column=2, pady=5, padx=5, ipady=3)

            self.var_entry_chenge_name_brod = ctk.StringVar()
            self.entry_change_name_brod = ctk.CTkEntry(self.frame2_change_brod, width=280,
                                                       textvariable=self.var_entry_chenge_name_brod)
            self.entry_change_name_brod.grid(row=0, column=3, pady=3, padx=3, ipady=3)

            self.lab_change_weight_brod = ctk.CTkLabel(self.frame2_change_brod, text='Вес: ')
            self.lab_change_weight_brod.grid(row=0, column=4, pady=3, padx=3, ipady=3)

            self.var_entry_chenge_weight_brod = ctk.StringVar()
            self.entry_change_weight_brod = ctk.CTkEntry(self.frame2_change_brod, width=60,
                                                         textvariable=self.var_entry_chenge_weight_brod)
            self.entry_change_weight_brod.grid(row=0, column=5, pady=3, padx=3, ipady=3)

            self.lab_change_price_brod = ctk.CTkLabel(self.frame2_change_brod, text='Цена: ')
            self.lab_change_price_brod.grid(row=0, column=6, pady=3, padx=3, ipady=3)

            self.var_entry_chenge_price_brod = ctk.StringVar()
            self.entry_change_price_brod = ctk.CTkEntry(self.frame2_change_brod, width=60,
                                                        textvariable=self.var_entry_chenge_price_brod)
            self.entry_change_price_brod.grid(row=0, column=7, pady=3, padx=3, ipady=3)

            self.lab_change_price_slav_brod = ctk.CTkLabel(self.frame2_change_brod, text='Цена Славгород: ')
            self.lab_change_price_slav_brod.grid(row=0, column=8, pady=3, padx=3, ipady=3)

            self.var_entry_chenge_price_slav_brod = ctk.StringVar()
            self.entry_change_price_slav_brod = ctk.CTkEntry(self.frame2_change_brod, width=65,
                                                             textvariable=self.var_entry_chenge_price_slav_brod)
            self.entry_change_price_slav_brod.grid(row=0, column=9, pady=3, padx=3, ipady=3)

            # frame для кнопок фото/добавить/сохранить/удалить
            self.frame3_but_brod = ctk.CTkFrame(self.window)
            self.frame3_but_brod.place(relx=0.2, rely=0.65)

            # добавить/сохранить/удалить

            self.bat_add_brod = ctk.CTkButton(self.frame3_but_brod, text='Добавить', command=self.save_add_brod,
                                              fg_color='#2F4F4F')
            self.bat_add_brod.grid(row=0, column=0, columnspan=2, sticky='wens', pady=3, padx=3, ipady=5)

            self.bat_save_change_brod = ctk.CTkButton(self.frame3_but_brod, text='Сохранить изменения',
                                                      command=self.save_change_brod)
            self.bat_save_change_brod.grid(row=0, column=2, columnspan=2, sticky='wens', pady=3, padx=35)

            self.bat_del_brod = ctk.CTkButton(self.frame3_but_brod, text='Удалить', command=self.del_brod,
                                              fg_color='#8B0000')
            self.bat_del_brod.grid(row=0, column=4, columnspan=2, sticky='wens', pady=3, padx=3)

            # фото (показываем старое и добавляем новое)
            self.but_old_photo = ctk.CTkButton(self.frame3_but_brod, text='Показать фото', fg_color='#006400',
                                               command=self.open_old_photo)
            self.but_old_photo.grid(row=0, column=6, columnspan=2, sticky='wens', pady=3, padx=35, ipady=3)

            self.but_add_photo = ctk.CTkButton(self.frame3_but_brod, text='Изменить фото',  fg_color='#006400',
                                               command=self.add_photo)
            self.but_add_photo.grid(row=0, column=8, columnspan=2, sticky='wens', pady=3, padx=3, ipady=3)

            # _______________________________________________
            # Таблица
            self.frame_table_brod = ctk.CTkFrame(self.window)
            self.frame_table_brod.place(relx=0.2, rely=0.05)

            self.table_brod = ttk.Treeview(self.frame_table_brod, show='headings', height=21
                                           )  # show='headings'-убираем первую пустую колонку
            # создаём колонки
            name_columns = ['id', 'Название', 'Вес', 'Цена Яровое', 'Цена Славгород']
            self.table_brod['columns'] = name_columns
            self.table_brod.column('id', width=100)
            self.table_brod.column('Название', width=300)
            self.table_brod.column('Вес', width=150)
            self.table_brod.column('Цена Яровое', width=150)
            self.table_brod.column('Цена Славгород', width=150)

            # заполняем названия колонок
            for header in name_columns:
                # присваиваем название
                self.table_brod.heading(header, text=header, anchor='center')
                # выравниваем текст данных по центру
                self.table_brod.column(header, anchor='center')
                # если нужно можно поменять местами колонки
                # self.table_clients['displaycolumns'] = ['нужный порядок']

            # записываем в таблицу данные из списка клиентов
            self.list_brod2 = []
            # заполняем список клиентов из таблицы
            conn = sq.connect('Works.db')
            cur = conn.cursor()
            cur.execute('''select ХлебID, Имя,
                Вес, Цена, Цена_Славгород from Brod''')
            for i in cur.fetchall():
                self.list_brod2.append(i)
            conn.close()

            # заполняем таблицу информацией из нашего списка
            # Create Striped Row Tags_________________________________________________
            self.table_brod.tag_configure('oddrow', background="white")
            self.table_brod.tag_configure('evenrow', background="lightblue")
            x = 1
            for row in self.list_brod2:
                if x == 1:
                    self.table_brod.insert('', tk.END, values=row, tags=('evenrow',))
                    x += 1
                else:
                    self.table_brod.insert('', tk.END, values=row, tags=('oddrow',))
                    x -= 1

            self.table_brod.grid(row=0, column=0)

            # создаём ивент при наведении на строку таблицы
            self.table_brod.bind('<<TreeviewSelect>>', self.selected_record_brod)

            # Добавляем виджет для прокрутки содержимого
            self.scrolbar = ctk.CTkScrollbar(self.frame_table_brod, command=self.table_brod.yview,
                                             orientation=tk.VERTICAL)
            self.table_brod.configure(yscrollcommand=self.scrolbar.set)
            self.scrolbar.grid(row=0, column=1)

    def save_add_brod(self):
        # id_brod = self.entry_change_id_brod.get()
        name = self.var_entry_chenge_name_brod.get()
        weight = self.var_entry_chenge_weight_brod.get()
        price = self.var_entry_chenge_weight_brod.get()
        price_slav = self.var_entry_chenge_price_slav_brod.get()
        photo = self.convert_photo

        self.list_brod = []
        # заполняем список клиентов из таблицы
        conn = sq.connect('Works.db')
        cur = conn.cursor()
        cur.execute('''select Имя from Brod''')
        for i in cur.fetchall():
            self.list_brod.append(i)
        conn.close()

        if name in self.list_brod:
            messagebox.showerror('Ошибка!', 'Хлеб с таким названием уже существует!')
        else:

            # открываем базу данных,
            conn = None

            try:
                conn = sq.connect('Works.db')
                cur = conn.cursor()

                if name != '' and price != None:
                    cur.execute('''insert into Brod(Имя, Вес, Цена, Цена_Славгород, Фото) values(?,?,?,?,?)''',
                                (name, weight, price, price_slav, photo))
                    conn.commit()
                else:
                    messagebox.showinfo('Cоздание клиента', 'Убедитесь что заполнили все столбцы!')
            except sq.Error as err:
                tk.messagebox.showerror('Ошибка бызы данных', err)
            finally:
                if conn != None:
                    conn.close()
            messagebox.showinfo("Добавить Хлеб", f'Вы добавили {name} в базу данных')
            name_table_brod = 'Brod'
            self.reset(name_table_brod)

    def save_change_brod(self):
        id_brod = self.entry_change_id_brod.get()
        name = self.entry_change_name_brod.get()
        weight = self.entry_change_weight_brod.get()
        price = self.entry_change_price_brod.get()
        price_slav = self.entry_change_price_slav_brod.get()
        photo = self.convert_photo

        # открываем базу данных,
        conn = None

        try:
            conn = sq.connect('Works.db')
            cur = conn.cursor()

            if name != '' and price != None:
                cur.execute('''update Brod
                               set Имя == ?,
                                   Вес == ?,
                                   Цена == ?,
                                   Цена_Славгород == ?,
                                   Фото == ?
                                   where ХлебID == ?''',
                            (name, weight, price, price_slav, photo, id_brod))
                conn.commit()
            else:
                messagebox.showinfo('Cоздание клиента', 'Убедитесь что заполнили все столбцы!')
        except sq.Error as err:
            tk.messagebox.showerror('Ошибка бызы данных', err)
        finally:
            if conn != None:
                conn.close()
        name_table_brod = 'Brod'
        self.reset(name_table_brod)
    def del_brod(self):

        id_brod = self.entry_change_id_brod.get()
        name = self.entry_change_name_brod.get()
        x = messagebox.askyesno('Удаление хлеб', f'Вы точно хотите удалить  {name} ?')

        # открываем базу данных, и получаем данные из наших энтрю
        conn = None
        try:
            conn = sq.connect('Works.db')
            cur = conn.cursor()

            # прописываем условия:
            if x == True:
                cur.execute('''Delete from Brod
                                              where ХлебID == ?''', (id_brod,))
                conn.commit()

        except sq.Error as err:
            tk.messagebox.showerror('Ошибка бызы данных', err)
        finally:
            if conn != None:
                conn.close()
        messagebox.showinfo('Удаление', f'Вы удалили {name} из базы!')

        delete = True
        name_table_brod = 'Brod'
        self.reset(name_table_brod)

    # функции которые при нажатии на строку в таблице хлеба или клиента выводит информацию в наши виджеты
    def selected_record_clients(self, e):
        # очищаем виджеты
        self.entry_change_id.delete(0, tk.END)
        self.entry_change_name.delete(0, tk.END)
        self.entry_change_telephone.delete(0, tk.END)
        self.entry_change_address.delete(0, tk.END)
        self.entry_change_name_store.delete(0, tk.END)

        # получаем информацию из выбранной строчки
        selected = self.table_clients.focus()
        values = self.table_clients.item(selected, 'values')

        # записываем эту информацию в наши виджеты
        self.entry_change_id.insert(0, values[0])
        self.entry_change_name.insert(0, values[1])
        self.entry_change_telephone.insert(0, values[2])
        self.entry_change_address.insert(0, values[3])
        self.entry_change_name_store.insert(0, values[4])

    def selected_record_brod(self, e):
        # очищаем виджеты
        self.entry_change_name_brod.delete(0, ctk.END)
        self.entry_change_weight_brod.delete(0, ctk.END)
        self.entry_change_price_brod.delete(0, ctk.END)
        self.entry_change_price_slav_brod.delete(0, ctk.END)
        self.entry_change_id_brod.delete(0, ctk.END)
        # self.photo_old_phormate_blod = None

        # получаем информацию из выбранной строчки
        selected = self.table_brod.focus()
        values = self.table_brod.item(selected, 'values')

        # записываем эту информацию в наши виджеты
        self.entry_change_id_brod.insert(0, values[0])
        self.entry_change_name_brod.insert(0, values[1])
        self.entry_change_weight_brod.insert(0, values[2])
        self.entry_change_price_brod.insert(0, values[3])
        self.entry_change_price_slav_brod.insert(0, values[4])
        # self.photo_old_phormate_blod = values[5]

    # КЛИЕНТЫ
    def clients(self):
        # система закрытия лишних окон
        if self.frame_brod_operation:
            self.frame2_change_brod.destroy()
            self.frame_table_brod.destroy()
            self.frame3_but_brod.destroy()
            self.frame_brod_operation = False
        if self.aplication_frame:
            self.frame1_aplication_brod.destroy()
            self.frame_aplication_bot.destroy()
            self.aplication_frame = False
        if self.permanent_applications_frame:
            self.frame_permanent_applications.destroy()
            self.frame2_permanent_applications.destroy()
            self.permanent_applications_frame = False
        if not self.frame_clients_operation:
            self.frame_clients_operation = True

            # создаём фрейм для расположения в нем виджетов анкеты(label, entry, кнопки добавить/сохранить/удалить)
            self.frame2_change_clients = ctk.CTkFrame(self.window)
            self.frame2_change_clients.place(relx=0.2, rely=0.55)

            self.lab_change_client = ctk.CTkLabel(self.frame2_change_clients, text='ID:')
            self.lab_change_client.grid(row=0, column=0, pady=5, padx=5)

            self.var_entry_chenge_id = ctk.StringVar()
            self.entry_change_id = ctk.CTkEntry(self.frame2_change_clients, textvariable=self.var_entry_chenge_id,
                                                width=40)
            self.entry_change_id.grid(row=0, column=1, sticky='wens', pady=3, padx=3, ipady=2)

            self.lab_change_name = ctk.CTkLabel(self.frame2_change_clients, text='Имя: ')
            self.lab_change_name.grid(row=0, column=2, sticky='wens', pady=5, padx=5, ipady=2)

            self.var_entry_chenge_name = ctk.StringVar()
            self.entry_change_name = ctk.CTkEntry(self.frame2_change_clients, width=130,
                                                  textvariable=self.var_entry_chenge_name)
            self.entry_change_name.grid(row=0, column=4, sticky='wens', pady=3, padx=3, ipady=2)

            self.lab_change_telephone = ctk.CTkLabel(self.frame2_change_clients, text='Телефон: ')
            self.lab_change_telephone.grid(row=0, column=5, sticky='wens', pady=3, padx=3, ipady=2)

            self.var_entry_chenge_telephone = ctk.StringVar()
            self.entry_change_telephone = ctk.CTkEntry(self.frame2_change_clients, width=100,
                                                       textvariable=self.var_entry_chenge_telephone)
            self.entry_change_telephone.grid(row=0, column=6, sticky='wens', pady=3, padx=3, ipady=2)

            self.lab_change_address = ctk.CTkLabel(self.frame2_change_clients, text='Адрес: ')
            self.lab_change_address.grid(row=0, column=7, sticky='wens', pady=3, padx=3, ipady=2)

            self.var_entry_chenge_address = ctk.StringVar()
            self.entry_change_address = ctk.CTkEntry(self.frame2_change_clients, width=120,
                                                     textvariable=self.var_entry_chenge_address)
            self.entry_change_address.grid(row=0, column=8, sticky='wens', pady=3, padx=3, ipady=2)

            self.lab_change_name_store = ctk.CTkLabel(self.frame2_change_clients, text='Название магазина: ')
            self.lab_change_name_store.grid(row=0, column=9, pady=3, padx=3, ipady=2)

            self.var_entry_chenge_name_store = ctk.StringVar()
            self.entry_change_name_store = ctk.CTkEntry(self.frame2_change_clients, width=120,
                                                        textvariable=self.var_entry_chenge_name_store)
            self.entry_change_name_store.grid(row=0, column=10, sticky='wens', pady=3, padx=3, ipady=2)

            # создаём фрейм для расположения в нем кнопок добавить/сохранить/удалить
            self.frame3_but = ctk.CTkFrame(self.window)
            self.frame3_but.place(relx=0.2, rely=0.65)

            self.bat_add_clients = ctk.CTkButton(self.frame3_but, text='Добавить', fg_color='#2F4F4F',
                                                 command=self.save_add_clients)
            self.bat_add_clients.grid(row=6, column=0 ,columnspan=2, sticky='wens', pady=3, padx=3)

            self.bat_save_change_clients = ctk.CTkButton(self.frame3_but, text='Сохранить изменения',
                                                         command=self.save_change_clients)
            self.bat_save_change_clients.grid(row=6, column=2, columnspan=2, sticky='wens', pady=3, padx=10)

            self.bat_del_clients = ctk.CTkButton(self.frame3_but, text='Удалить', fg_color='#8B0000',
                                                 command=self.del_clients)
            self.bat_del_clients.grid(row=6, column=4, columnspan=2, sticky='wens', pady=3, padx=3)

            # _______________________________________________
            # Таблица
            # Создаём фрейм в котором расположим таблицу и скролбар
            self.frame_table_clients = ctk.CTkFrame(self.window)
            self.frame_table_clients.place(relx=0.2, rely=0.05)

            # Создаём таблицу,
            self.table_clients = ttk.Treeview(self.frame_table_clients, show='headings', height=21
                                              )  # show='headings'-убираем первую пустую колонку
            self.table_clients.grid(row=0, column=0)

            # создаём переменную с названием колонок
            name_columns = ['id', 'Название организации', 'Телефон', 'Адрес', 'Название магазина']
            self.table_clients['columns'] = name_columns
            # присваиваем колонке с названием ID ширину 50
            self.table_clients.column('id', width=50)

            # заполняем названия колонок
            for header in name_columns:
                # присваиваем название
                self.table_clients.heading(header, text=header, anchor='center')
                # выравниваем текст данных по центру
                self.table_clients.column(header, anchor='center')

                # если нужно можно поменять местами колонки
                # self.table_clients['displaycolumns'] = ['нужный порядок']
            self.table_clients.column('Название организации', anchor='w')
            # записываем в таблицу данные из списка клиентов
            self.list_clients2 = []
            # заполняем список клиентов из таблицы
            conn = sq.connect('Works.db')
            cur = conn.cursor()
            cur.execute('''select * from Clients''')
            for i in cur.fetchall():
                self.list_clients2.append(i)
            conn.close()

            # Add Some Style___________________________
            style = ttk.Style()

            # Pick A Theme
            style.theme_use('default')

            # Configure the Treeview Colors
            style.configure("Treeview",
                            background="#D3D3D3",
                            foreground="black",
                            rowheight=16,
                            fieldbackground="#D3D3D3")

            # Change Selected Color
            style.map('Treeview',
                      background=[('selected', "#347083")])

            # Create Striped Row Tags_________________________________________________
            self.table_clients.tag_configure('oddrow', background="white")
            self.table_clients.tag_configure('evenrow', background="lightblue")



            # записываем данные прлученные из базы данных в таблицу
            x = 1
            for row in self.list_clients2:
                if x == 1:
                    self.table_clients.insert('', tk.END, values=row, tags=('evenrow',))
                    x += 1
                else:
                    self.table_clients.insert('', tk.END, values=row, tags=('oddrow',))
                    x -= 1

            # создаём ивент при наведении на строку таблицы
            self.table_clients.bind('<<TreeviewSelect>>', self.selected_record_clients)

            # Добавляем виджет для прокрутки содержимого
            self.scrolbar = ctk.CTkScrollbar(self.frame_table_clients, command=self.table_clients.yview,
                                             orientation=tk.VERTICAL)
            self.table_clients.configure(yscrollcommand=self.scrolbar.set)
            self.scrolbar.grid(row=0, column=1)

    def save_add_clients(self):
        name = self.var_entry_chenge_name.get()
        telephone = self.var_entry_chenge_telephone.get()
        address = self.var_entry_chenge_address.get()
        name_store = self.var_entry_chenge_name_store.get()

        self.list_clients = []
        # заполняем список клиентов из таблицы
        conn = sq.connect('Works.db')
        cur = conn.cursor()
        cur.execute('''select Name from Clients''')
        for i in cur.fetchall():
            self.list_clients.append(i)
        conn.close()
        if name in self.list_clients:
            messagebox.showerror('Ошибка', 'Клиент с таким именем уже существует!')
        else:
            # открываем базу данных,
            conn = None

            try:
                conn = sq.connect('Works.db')
                cur = conn.cursor()

                if name != '' and telephone != '':
                    cur.execute('''insert into Clients(Name, Phone_number, Address, Name_shop) values(?,?,?,?)''',
                                (name, telephone, address, name_store))
                    conn.commit()
                else:
                    messagebox.showinfo('Cоздание клиента', 'Убедитесь что заполнили все столбцы!')
            except sq.Error as err:
                tk.messagebox.showerror('Ошибка бызы данных', err)
            finally:
                if conn != None:
                    conn.close()
            messagebox.showinfo('Создание клиента', f'Вы создали клиента {name}!')

            self.entry_change_name.delete(0, ctk.END)
            self.entry_change_telephone.delete(0, ctk.END)
            self.entry_change_address.delete(0, ctk.END)
            self.entry_change_name_store.delete(0, ctk.END)

            name_table_clients = 'Clients'
            self.reset(name_table_clients)

    def save_change_clients(self):
        id_clients = self.entry_change_id.get()
        name = self.entry_change_name.get()
        telephone = self.entry_change_telephone.get()
        address = self.entry_change_address.get()
        name_store = self.entry_change_name_store.get()

        # открываем базу данных,
        conn = None

        try:
            conn = sq.connect('Works.db')
            cur = conn.cursor()

            if name != '' and telephone != '':
                cur.execute('''update Clients
                                set Name == ?,
                                    Phone_number == ?,
                                    Address == ?,
                                    Name_shop == ?
                                where ClientsID == ?''',
                            (name, telephone, address, name_store, id_clients))
                conn.commit()
            else:
                messagebox.showinfo('Cоздание клиента', 'Убедитесь что заполнили все столбцы!')
        except sq.Error as err:
            tk.messagebox.showerror('Ошибка бызы данных', err)
        finally:
            if conn != None:
                conn.close()
        name_table_clients = 'Clients'
        self.reset(name_table_clients)

    def del_clients(self):
        id_clients = self.entry_change_id.get()
        x = messagebox.askyesno('Удаление контакта', f'Вы точно хотите клиента с id - {id_clients} ?')

        # открываем базу данных, и получаем данные из наших энтрю
        conn = None
        try:
            conn = sq.connect('Works.db')
            cur = conn.cursor()

            # прописываем условия:
            if x == True:
                cur.execute('''Delete from Clients
                                      where ClientsID == ?''', (id_clients,))
                conn.commit()

        except sq.Error as err:
            tk.messagebox.showerror('Ошибка бызы данных', err)
        finally:
            if conn != None:
                conn.close()
        name_table_clients = 'Clients'
        self.reset(name_table_clients)

    # создание базы данных и таблицы
    def creation_bd(self):
        # списки с хлебом для печати
        self.list_name_brod = ['Батон_Сдобный',
                               'Батон_Французский',
                               'Хлеб_Богатырский_отрубной',
                               'Хлеб_Богатырский_отрубной_круглый',
                               'Хлеб_Дарк_8_злаков',
                               'Хлеб_Классический_075',
                               'Хлеб_Классический_050',
                               'Хлеб_Классический_035',
                               'Хлеб_Купеческий_заварной_с_изюмом',
                               'Хлеб_Купеческий_заварной_с_тмином',
                               'Хлеб_Овсяный',
                               'Хлеб_Степной',
                               'Хлеб_Тостовый',
                               'Хлеб_Чиабатта',
                               'Хлеб_Яровской_ржаной',
                               'Булочка_К_чаю',
                               'Булочка_С_корицей',
                               'Булочка_С_корицей_и_кремом',
                               'Булочка_С_чесноком',
                               'Булочка_С_кунжутом_для_гамбургера',
                               'Булочка_Сдобная_для_хот_дога',
                               'Плетёнка_с_маком',
                               'Плюшка',
                               'Растегай',
                               'Рогалик',
                               'Рулет_с_маком',
                               'Тесто_Пирожковое_охлажденное',
                               'Пряники',
                               'Ватрушка_с_творогом',
                               'Ватрушка_с_сыром',
                               'Ватрушка_с_конфитюром',
                               'Беляш_печеный',
                               'Кекс_классический',
                               'Кекс_шоколадный',
                               'Кулебяка',
                               'Пирог_с_капустой',
                               'Пирог_с_яблоками',
                               'Пицца_мини',
                               'Ромовая_баба',
                               'Сосиска_в_тесте'
                               ]
        self.list_name_brod2_osnov = ['Батон_Сдобный',
                               'Батон_Французский',
                               'Хлеб_Богатырский_отрубной',
                               'Хлеб_Богатырский_отрубной_круглый',
                               'Хлеб_Дарк_8_злаков',
                               'Хлеб_Классический_075',
                               'Хлеб_Классический_050',
                               'Хлеб_Классический_035',
                               'Хлеб_Купеческий_заварной_с_изюмом',
                               'Хлеб_Купеческий_заварной_с_тмином',
                               'Хлеб_Овсяный',
                               'Хлеб_Степной',
                               'Хлеб_Тостовый',
                               'Хлеб_Чиабатта',
                               'Хлеб_Яровской_ржаной',
                               'Булочка_К_чаю',
                               'Булочка_С_корицей',
                               'Булочка_С_корицей_и_кремом',
                               'Булочка_С_чесноком',
                               'Булочка_С_кунжутом_для_гамбургера',
                               'Булочка_Сдобная_для_хот_дога',
                               'Плетёнка_с_маком',
                               'Плюшка',
                               'Растегай',
                               'Рогалик',
                               'Рулет_с_маком',
                               'Тесто_Пирожковое_охлажденное',
                               'Пряники']
        self.list_name_brod2_dop = [
                               'Ватрушка_с_творогом',
                               'Ватрушка_с_сыром',
                               'Ватрушка_с_конфитюром',
                               'Беляш_печеный',
                               'Кекс_классический',
                               'Кекс_шоколадный',
                               'Кулебяка',
                               'Пирог_с_капустой',
                               'Пирог_с_яблоками',
                               'Пицца_мини',
                               'Ромовая_баба',
                               'Сосиска_в_тесте']
        self.list_name_brod2_osnov_print = ['Клиент',
                                      'Сдоб',
                                      'Фран',
                                      'Бога',
                                      'Богк',
                                      'Дарк',
                                      'Кл75',
                                      'Кл50',
                                      'Кл35',
                                      'Куиз',
                                      'Кутм',
                                      'Овся',
                                      'Степ',
                                      'Тост',
                                      'Чиаб',
                                      'Яров',
                                      'Кчаю',
                                      'Кори',
                                      'Коркр',
                                      'Счес',
                                      'гамб',
                                      'хотд',
                                      'Плет',
                                      'Плюш',
                                      'Раст',
                                      'Рога',
                                      'Руле',
                                      'Тест',
                                      'Прян']
        self.list_name_brod2_dop_print = ['Клиент',
                                    'Ватв',
                                    'Васы',
                                    'Вако',
                                    'Беля',
                                    'КеКл',
                                    'КеШо',
                                    'Куле',
                                    'ПиКа',
                                    'ПиЯб',
                                    'Пицц',
                                    'Ромо',
                                    'Соси']
        # получаем сегодняшнюю дату
        date_today = datetime.datetime.today()
        # получаем завтрешнюю дату
        date_tomorrow = date_today + datetime.timedelta(days=1)
        # создаём переменную с завтрешней датой в удобном формате
        self.name_table_application = date_tomorrow.strftime('day_%d_%m_%y')
        # создаём переменную и присваиваем ей название сегоднешнего дня недели
        weekday = datetime.datetime.today().strftime('%A')
        conn = None
        try:

            conn = sq.connect('Works.db')
            cur = conn.cursor()
            # создадим таблицу с нашей продукцией
            cur.execute(
                '''create table if not exists Brod(ХлебID INTEGER PRIMARY KEY NOT NULL, Имя text,
                Вес INTEGER, Цена INTEGER, Цена_Славгород INTEGER, Фото BLOB)''')
            # создадим таблицу с нашими клиентами
            cur.execute('''create table if not exists Clients(ClientsID INTEGER PRIMARY KEY NOT NULL, Name text,
                                            Phone_number text, Address text, Name_shop text)''')
            # создадим таблицы постоянных заявок на все дни недели
            list_day_week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
            for day in list_day_week:
                cur.execute(f'''CREATE TABLE IF NOT EXISTS {day} (
                                                                        ClientsID INTEGER PRIMARY KEY NOT NULL,
                                                                        Name_Clients text,
                                                                        Батон_Сдобный integer,
                                                                        Батон_Французский integer,
                                                                        Хлеб_Богатырский_отрубной integer,
                                                                        Хлеб_Богатырский_отрубной_круглый integer,
                                                                        Хлеб_Дарк_8_злаков integer,
                                                                        Хлеб_Классический_075 integer,
                                                                        Хлеб_Классический_050 integer,
                                                                        Хлеб_Классический_035 integer,
                                                                        Хлеб_Купеческий_заварной_с_изюмом integer,
                                                                        Хлеб_Купеческий_заварной_с_тмином integer,
                                                                        Хлеб_Овсяный integer,
                                                                        Хлеб_Степной integer,
                                                                        Хлеб_Тостовый integer,
                                                                        Хлеб_Чиабатта integer,
                                                                        Хлеб_Яровской_ржаной integer,
                                                                        Булочка_К_чаю integer,
                                                                        Булочка_С_корицей integer,
                                                                        Булочка_С_корицей_и_кремом integer,
                                                                        Булочка_С_чесноком integer,
                                                                        Булочка_С_кунжутом_для_гамбургера integer,
                                                                        Булочка_Сдобная_для_хот_дога integer,
                                                                        Плетёнка_с_маком integer,
                                                                        Плюшка integer,
                                                                        Растегай integer,
                                                                        Рогалик integer,
                                                                        Рулет_с_маком integer,
                                                                        Тесто_Пирожковое_охлажденное integer,
                                                                        Пряники integer,
                                                                        Ватрушка_с_творогом integer,
                                                                        Ватрушка_с_сыром integer,
                                                                        Ватрушка_с_конфитюром integer,
                                                                        Беляш_печеный integer,
                                                                        Кекс_классический integer,
                                                                        Кекс_шоколадный integer,
                                                                        Кулебяка integer,
                                                                        Пирог_с_капустой integer,
                                                                        Пирог_с_яблоками integer,
                                                                        Пицца_мини integer,
                                                                        Ромовая_баба integer,
                                                                        Сосиска_в_тесте integer)''')

            # если сегодня не суббота то создаём таблицу заявки(основного хлеба) на следующий день
            if weekday != 'Saturday':
                cur.execute(f'''CREATE TABLE IF NOT EXISTS {self.name_table_application}(
                                                            ClientsID INTEGER PRIMARY KEY NOT NULL,
                                                            Name_Clients text,
                                                            Батон_Сдобный integer,
                                                            Батон_Французский integer,
                                                            Хлеб_Богатырский_отрубной integer,
                                                            Хлеб_Богатырский_отрубной_круглый integer,
                                                            Хлеб_Дарк_8_злаков integer,
                                                            Хлеб_Классический_075 integer,
                                                            Хлеб_Классический_050 integer,
                                                            Хлеб_Классический_035 integer,
                                                            Хлеб_Купеческий_заварной_с_изюмом integer,
                                                            Хлеб_Купеческий_заварной_с_тмином integer,
                                                            Хлеб_Овсяный integer,
                                                            Хлеб_Степной integer,
                                                            Хлеб_Тостовый integer,
                                                            Хлеб_Чиабатта integer,
                                                            Хлеб_Яровской_ржаной integer,
                                                            Булочка_К_чаю integer,
                                                            Булочка_С_корицей integer,
                                                            Булочка_С_корицей_и_кремом integer,
                                                            Булочка_С_чесноком integer,
                                                            Булочка_С_кунжутом_для_гамбургера integer,
                                                            Булочка_Сдобная_для_хот_дога integer,
                                                            Плетёнка_с_маком integer,
                                                            Плюшка integer,
                                                            Растегай integer,
                                                            Рогалик integer,
                                                            Рулет_с_маком integer,
                                                            Тесто_Пирожковое_охлажденное integer,
                                                            Пряники integer, 
                                                            Ватрушка_с_творогом integer,
                                                            Ватрушка_с_сыром integer,
                                                            Ватрушка_с_конфитюром integer,
                                                            Беляш_печеный integer,
                                                            Кекс_классический integer,
                                                            Кекс_шоколадный integer,
                                                            Кулебяка integer,
                                                            Пирог_с_капустой integer,
                                                            Пирог_с_яблоками integer,
                                                            Пицца_мини integer,
                                                            Ромовая_баба integer,
                                                            Сосиска_в_тесте integer)''')
            conn.commit()

        except sq.Error as err:
            tk.messagebox.showerror('Ошибка бызы данных', err)
        finally:
            if conn != None:
                conn.close()

        # заполним таблицу заявок постоянными заявками____!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # пропишем услоавия для выбора имени таблицы постоянных заявок для автоматического записывания их в таблицу
        # заявок завтрешнего дня

        try:

            conn = sq.connect('Works.db')
            cur = conn.cursor()
            self.x = []
            # если сегодня понедельник, запишем в список все постоянные заявки понедельника
            if weekday == 'Monday':
                cur.execute('''select * from Вторник''')
                self.x = cur.fetchall()
            # если сегодня вторник, запишем в список все постоянные заявки вторника
            if weekday == 'Tuesday':
                cur.execute('''select * from Среда''')
                self.x = cur.fetchall()
            # если сегодня среда, запишем в список все постоянные заявки среды
            if weekday == 'Wednesday':
                cur.execute('''select * from Четверг''')
                self.x = cur.fetchall()
            # если сегодня четверг, запишем в список все постоянные заявки четверга
            if weekday == 'Thursday':
                cur.execute('''select * from Пятница''')
                self.x = cur.fetchall()
            # если сегодня пятница, запишем в список все постоянные заявки пятницы
            if weekday == 'Friday':
                cur.execute('''select * from Суббота''')
                self.x = cur.fetchall()
            # если сегодня воскресенье, запишем в список все постоянные заявки субботы
            if weekday == 'Sunday':
                cur.execute('''select * from Понедельник''')
                self.x = cur.fetchall()
            # запишем заявки из нашего списка в таблицу заявок завтрешнего дня
            # если их там ещё нет
            # для этого запишем в список id клиентов из таблицы заявок
            conn = sq.connect('Works.db')
            cur = conn.cursor()
            cur.execute(f'''select ClientsID from {self.name_table_application}''')
            id_clientse = []
            for i in cur.fetchall():
                for c in i:
                    id_clientse.append(c)
            # если в нашем списке нет клиента с таким id то внесем его в таблицу заявок
            for list_aplication in self.x:
                if list_aplication[0] not in id_clientse:
                    cur.execute(f'''insert into {self.name_table_application} (
                                                                               ClientsID,
                                                                               Name_Clients,
                                                                               Батон_Сдобный,
                                                                               Батон_Французский,
                                                                               Хлеб_Богатырский_отрубной,
                                                                               Хлеб_Богатырский_отрубной_круглый,
                                                                               Хлеб_Дарк_8_злаков,
                                                                               Хлеб_Классический_075,
                                                                               Хлеб_Классический_050,
                                                                               Хлеб_Классический_035,
                                                                               Хлеб_Купеческий_заварной_с_изюмом,
                                                                               Хлеб_Купеческий_заварной_с_тмином,
                                                                               Хлеб_Овсяный,
                                                                               Хлеб_Степной,
                                                                               Хлеб_Тостовый,
                                                                               Хлеб_Чиабатта,
                                                                               Хлеб_Яровской_ржаной,
                                                                               Булочка_К_чаю,
                                                                               Булочка_С_корицей,
                                                                               Булочка_С_корицей_и_кремом,
                                                                               Булочка_С_чесноком,
                                                                               Булочка_С_кунжутом_для_гамбургера,
                                                                               Булочка_Сдобная_для_хот_дога,
                                                                               Плетёнка_с_маком,
                                                                               Плюшка,
                                                                               Растегай,
                                                                               Рогалик,
                                                                               Рулет_с_маком,
                                                                               Тесто_Пирожковое_охлажденное,
                                                                               Пряники,
                                                                               Ватрушка_с_творогом,
                               Ватрушка_с_сыром,
                               Ватрушка_с_конфитюром,
                               Беляш_печеный,
                               Кекс_классический,
                               Кекс_шоколадный,
                               Кулебяка,
                               Пирог_с_капустой,
                               Пирог_с_яблоками,
                               Пицца_мини,
                               Ромовая_баба,
                               Сосиска_в_тесте)
                    values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                                    (list_aplication[0], list_aplication[1], list_aplication[2]
                                     , list_aplication[3], list_aplication[4], list_aplication[5], list_aplication[6]
                                     , list_aplication[7], list_aplication[8], list_aplication[9], list_aplication[10]
                                     , list_aplication[11], list_aplication[12], list_aplication[13], list_aplication[14]
                                     , list_aplication[15], list_aplication[16], list_aplication[17], list_aplication[18]
                                     , list_aplication[19], list_aplication[20], list_aplication[21], list_aplication[22]
                                     , list_aplication[23], list_aplication[24], list_aplication[25], list_aplication[26]
                                     , list_aplication[27], list_aplication[28], list_aplication[29], list_aplication[30]
                                 , list_aplication[31], list_aplication[32], list_aplication[33], list_aplication[34]
                                 , list_aplication[35], list_aplication[36], list_aplication[37], list_aplication[38]
                                     , list_aplication[39], list_aplication[40], list_aplication[41]))

                    conn.commit()
        except sq.Error as err:
            tk.messagebox.showerror('Ошибка бызы данных', err)
        finally:
            if conn != None:
                conn.close()

if __name__ == '__main__':
    x = Main()

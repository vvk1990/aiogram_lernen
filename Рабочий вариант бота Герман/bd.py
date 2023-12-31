import sqlite3 as sq
import datetime


# # Создадим функцию вывода Прайса
def price():
    conn = sq.connect('Works.db')
    cur = conn.cursor()
    cur.execute('''select ХлебID, Имя, Вес, Цена, Цена_Славгород, Фото  from Brod ''')
    data_clients = []
    data_clients2 = []
    for i in cur.fetchall():
        data_clients.append(i)
    conn.close()
    return data_clients


# Список названия хлеба
def price_name():
    conn = sq.connect('Works.db')
    cur = conn.cursor()
    cur.execute('''select  Имя  from Brod ''')
    data_clients = []
    for i in cur.fetchall():
        for ii in i:
            data_clients.append(ii)
    conn.close()
    return data_clients


# Создадим функцию вывода Прайса для Ярового из bd
def price_jrovoe():
    conn = sq.connect('Works.db')
    cur = conn.cursor()
    cur.execute('''select ХлебID, Имя, Вес, Цена from Brod ''')
    data_clients = []
    for i in cur.fetchall():
        data_clients.append(i)
    conn.close()
    return data_clients


# Создадим функцию вывода Прайса для Славгорода из bd
def price_slavgorod():
    conn = sq.connect('Works.db')
    cur = conn.cursor()
    cur.execute('''select ХлебID, Имя, Вес, Цена_Славгород   from Brod ''')
    data_clients = []
    for i in cur.fetchall():
        data_clients.append(i)
    conn.close()
    return data_clients


# Создадим функцию вывода списка цен Ярового
def price_jrovoe_list():
    conn = sq.connect('Works.db')
    cur = conn.cursor()
    list_prise = []
    cur.execute(f'''select Цена  from Brod''')
    for i in cur.fetchall():
        for ii in i:
            list_prise.append(ii)
    conn.close()
    return list_prise


# Создадим функцию вывода списка цен Славгород
def price_slavgorod_list():
    conn = sq.connect('Works.db')
    cur = conn.cursor()
    list_prise = []
    cur.execute(f'''select Цена_Славгород  from Brod''')
    for i in cur.fetchall():
        for ii in i:
            list_prise.append(ii)
    conn.close()
    return list_prise


# Создадим функцию вывода имени клиента по его id
def name_clients(user_id):
    conn = sq.connect('Works.db')
    cur = conn.cursor()
    cur.execute('''select  Name from Clients where ClientsID == ?''', (user_id,))
    data_clients = []
    for i in cur.fetchone():
        data_clients.append(i)
    name_clients = data_clients[0]

    conn.close()
    return name_clients


# Создадим функцию вывода имени клиента по его id2
def name_clients2(user_id):
    conn = sq.connect('Works.db')
    cur = conn.cursor()
    cur.execute('''select  Name from Clients where ClientsID2 == ?''', (user_id,))
    data_clients = []
    for i in cur.fetchone():
        data_clients.append(i)
    print(data_clients)
    name_clients = data_clients[0]

    conn.close()
    return name_clients


# Создадим функцию вывода имени клиента и его id2 в bd
def name_and_id_clients(user_id):
    conn = sq.connect('Works.db')
    cur = conn.cursor()
    cur.execute('''select ClientsID, Name from Clients where ClientsID2 == ?''', (user_id,))
    data_clients = []
    for i in cur.fetchone():
        data_clients.append(i)
    id_clients = data_clients[0]
    name_clients = data_clients[1]
    list_name_and_id_clients = [id_clients, name_clients]
    conn.close()
    return list_name_and_id_clients


# Создадим функцию вывода всех клиентов и их id
def id_and_name_all_clients():
    conn = sq.connect('Works.db')
    cur = conn.cursor()
    cur.execute('''select ClientsID, Name from Clients''')
    data_clients = []
    for i in cur.fetchall():
        data_clients.append(i)
    conn.close()
    return data_clients


# Функция вывода города и статуса клиента
def citi_wiring_clients(id_clients):
    conn = sq.connect('Works.db')
    cur = conn.cursor()
    cur.execute(f'''select Город, Проводка from Clients where ClientsID == {id_clients} ''')
    data_clients = []
    for i in cur.fetchall():
        for ii in i:
            data_clients.append(ii)
    conn.close()
    return data_clients


# функция просмотрзаявки на наличие
def applications_true_falshe(name_clients):
    # получаем имя таблицы "сегодняшнюю дату"
    date_today = datetime.datetime.today()
    # получаем завтрашнюю дату
    date_tomorrow = date_today + datetime.timedelta(days=1)
    # создаём переменную с завтрашней датой в удобном формате
    name_table_application = date_tomorrow.strftime('day_%d_%m_%y')

    # создадим переменную и поместим в неё список имен клиентов сделавших заявку
    list_clients_aplication1 = []

    # залезаем в базу данных и запросим индексы организаций которые уже сделали заявку на этот день
    conn = sq.connect('Works.db')
    cur = conn.cursor()
    cur.execute(f'''select Name_Clients from {name_table_application}''')
    for i in cur.fetchall():
        for ii in i:
            list_clients_aplication1.append(ii)
    conn.close()
    # проверим есть ли заявку у нашего клиента, и выдадим да или нет
    if name_clients in list_clients_aplication1:
        return True
    else:
        return False


# создадим таблицу для основной заявки если её ещё нет и запишем в нее заявку клиента
def create_request_table(id_clients, name_clients, list_aplication1, citi_clients, wiring_clients):
    # получаем имя таблицы "сегодняшнюю дату"
    date_today = datetime.datetime.today()
    # получаем завтрашнюю дату
    date_tomorrow = date_today + datetime.timedelta(days=1)
    # создаём переменную с завтрашней датой в удобном формате
    name_table_application = date_tomorrow.strftime('day_%d_%m_%y')
    # создаём переменную и присваиваем ей название сегодняшнего дня недели
    weekday = datetime.datetime.today().strftime('%A')

    # если сегодня не суббота(так как в воскр не работаем) тогда создадим таблицу заявок если её ещё нет
    if weekday != 'Saturday':
        conn = sq.connect('Works.db')
        cur = conn.cursor()
        cur.execute(f'''CREATE TABLE IF NOT EXISTS {name_table_application}(
                                                                        ClientsID INTEGER PRIMARY KEY NOT NULL,
                                                                        Name_Clients text,
                                                                        Город text,
                                                                        Проводка text,
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
                                                                                Сосиска_в_тесте integer
                                                                        )''')

        conn.commit()
        conn.close()

    # создадим список в который поместим индексы организаций уже сделавших заявку на этот день
    list_clients_aplication1 = []
    # залезаем в базу данных и запросим индексы организаций которые уже сделали заявку на этот день
    conn = sq.connect('Works.db')
    cur = conn.cursor()
    cur.execute(f'''select ClientsID from {name_table_application}''')
    for i in cur.fetchall():
        for ii in i:
            list_clients_aplication1.append(ii)

    # если клиент ещё не сделал заявку тогда запишем её
    if int(id_clients) in list_clients_aplication1:
        return False

    else:
        # открываем базу данных и записываем данные из списка заявок в таблицу заявок
        conn = sq.connect('Works.db')
        cur = conn.cursor()
        cur.execute(f'''insert into {name_table_application} (
                                                                                           ClientsID,
                                                                                           Name_Clients,
                                                                                           Город,
                                                                                           Проводка,
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
                     values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                    (int(id_clients), name_clients, citi_clients, wiring_clients, list_aplication1[0],
                     list_aplication1[1], list_aplication1[2]
                     , list_aplication1[3], list_aplication1[4], list_aplication1[5], list_aplication1[6]
                     , list_aplication1[7], list_aplication1[8], list_aplication1[9], list_aplication1[10]
                     , list_aplication1[11], list_aplication1[12], list_aplication1[13], list_aplication1[14]
                     , list_aplication1[15], list_aplication1[16], list_aplication1[17], list_aplication1[18]
                     , list_aplication1[19], list_aplication1[20], list_aplication1[21], list_aplication1[22]
                     , list_aplication1[23], list_aplication1[24], list_aplication1[25], list_aplication1[26]
                     , list_aplication1[27], list_aplication1[28], list_aplication1[29], list_aplication1[30]
                     , list_aplication1[31], list_aplication1[32], list_aplication1[33], list_aplication1[34]
                     , list_aplication1[35], list_aplication1[36], list_aplication1[37], list_aplication1[38]
                     , list_aplication1[39]))

        conn.commit()
        conn.close()
        return True


# исправим старую заявку клиента
def change_old_aplikation(id_clients, list_aplication1):
    # получаем сегодняшнюю дату
    date_today = datetime.datetime.today()
    # получаем завтрашнюю дату
    date_tomorrow = date_today + datetime.timedelta(days=1)
    # создаём переменную с завтрашней датой в удобном формате
    name_table_application = date_tomorrow.strftime('day_%d_%m_%y')

    # зайдем в bd и исправим старую заявку клиента
    conn = sq.connect('Works.db')
    cur = conn.cursor()
    cur.execute(f'''UPDATE {name_table_application} 
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
                                                                                      Кекс_шоколадный = ?,
                                                                                      Кулебяка = ?,
                                                                                      Пирог_с_капустой = ?,
                                                                                      Пирог_с_яблоками = ?,
                                                                                      Пицца_мини = ?,
                                                                                      Ромовая_баба = ?,
                                                                                      Сосиска_в_тесте = ?
                                           where ClientsID == ?''',
                (list_aplication1[0], list_aplication1[1], list_aplication1[2]
                 , list_aplication1[3], list_aplication1[4], list_aplication1[5], list_aplication1[6]
                 , list_aplication1[7], list_aplication1[8], list_aplication1[9], list_aplication1[10]
                 , list_aplication1[11], list_aplication1[12], list_aplication1[13], list_aplication1[14]
                 , list_aplication1[15], list_aplication1[16], list_aplication1[17], list_aplication1[18]
                 , list_aplication1[19], list_aplication1[20], list_aplication1[21], list_aplication1[22]
                 , list_aplication1[23], list_aplication1[24], list_aplication1[25], list_aplication1[26]
                 , list_aplication1[27], list_aplication1[28], list_aplication1[29], list_aplication1[30]
                 , list_aplication1[31], list_aplication1[32], list_aplication1[33], list_aplication1[34]
                 , list_aplication1[35], list_aplication1[36], list_aplication1[37], list_aplication1[38]
                 , list_aplication1[39]
                 , id_clients))
    conn.commit()
    conn.close()


# скачаем старую заявку и поместим её в наш список
def old_aplication(name_clients):
    # получаем имя таблицы "сегодняшнюю дату"
    date_today = datetime.datetime.today()
    # получаем завтрашнюю дату
    date_tomorrow = date_today + datetime.timedelta(days=1)
    # создаём переменную с завтрашней датой в удобном формате
    name_table_application = date_tomorrow.strftime('day_%d_%m_%y')

    conn = sq.connect('Works.db')
    cur = conn.cursor()
    cur.execute(f'''select * from {name_table_application} where Name_Clients == ?''', (name_clients,))
    value = cur.fetchall()
    # выгружаем данные кортежа в список
    list_old_aplication = []
    for i in value:
        for val in i:
            list_old_aplication.append(val)
    # удалим из списка индекс и имя клиента
    del list_old_aplication[0]
    # имя переместилось на 1 место поэтому-[0]
    del list_old_aplication[0]
    # удалим из списка город и статус клиента
    del list_old_aplication[0]
    # имя переместилось на 1 место поэтому-[0]
    del list_old_aplication[0]

    return list_old_aplication


# регистрация клиента
def registration_clients(user_id, text):
    conn = sq.connect('Works.db')
    cur = conn.cursor()
    cur.execute('''update Clients
                               set ClientsID2 == ?
                               where ClientsID == ?''',
                (user_id, text))
    conn.commit()
    conn.close()

    return True


# заполняем таблицу с отзывами
def registration_review(id_clients, name_clients, text):
    conn = sq.connect('Works.db')
    cur = conn.cursor()
    cur.execute('''insert into reviews (ClientID, Name, Reviews)
                             values(?, ?, ?)''', (id_clients, name_clients, text))
    conn.commit()
    conn.close()


# скачаем ID2 клиентов в список
def list_id2_clients():
    conn = sq.connect('Works.db')
    cur = conn.cursor()
    cur.execute('''select ClientsID2 from Clients''')
    id_clientse = []
    for i in cur.fetchall():
        for c in i:
            id_clientse.append(c)
    conn.close()

    return id_clientse


# постоянная заявка клиента
def permanent_applications(id_clients, name_table):
    conn = sq.connect('Works.db')
    cur = conn.cursor()
    cur.execute(f'''select * from {name_table} where ClientsID == ?''', (int(id_clients),))
    value = cur.fetchall()
    list_val = []
    # выгружаем данные кортежа в список
    for i in value:
        for val in i:
            list_val.append(val)

    print(list_val)
    conn.close()
    return list_val


# сохраним нашу постоянную заявку
def save_permanent_applications(id_clients, name_clients, list_aplication1, name_table):
    # создадим список в который поместим индексы организаций уже сделавших заявку на этот день
    list_clients_aplication1 = []
    # залезаем в базу данных и запросим индексы организаций которые уже сделали заявку на этот день
    conn = sq.connect('Works.db')
    cur = conn.cursor()
    cur.execute(f'''select ClientsID from {name_table}''')
    for i in cur.fetchall():
        for ii in i:
            list_clients_aplication1.append(ii)

    # если клиент уже сделал заявку тогда перезапишем её
    if int(id_clients) in list_clients_aplication1:
        # зайдем в bd и исправим старую постоянную заявку клиента
        conn = sq.connect('Works.db')
        cur = conn.cursor()
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
                                                                                          Кекс_шоколадный = ?,
                                                                                          Кулебяка = ?,
                                                                                          Пирог_с_капустой = ?,
                                                                                          Пирог_с_яблоками = ?,
                                                                                          Пицца_мини = ?,
                                                                                          Ромовая_баба = ?,
                                                                                          Сосиска_в_тесте = ?
                                               where ClientsID == ?''',
                    (list_aplication1[0], list_aplication1[1], list_aplication1[2]
                     , list_aplication1[3], list_aplication1[4], list_aplication1[5], list_aplication1[6]
                     , list_aplication1[7], list_aplication1[8], list_aplication1[9], list_aplication1[10]
                     , list_aplication1[11], list_aplication1[12], list_aplication1[13], list_aplication1[14]
                     , list_aplication1[15], list_aplication1[16], list_aplication1[17], list_aplication1[18]
                     , list_aplication1[19], list_aplication1[20], list_aplication1[21], list_aplication1[22]
                     , list_aplication1[23], list_aplication1[24], list_aplication1[25], list_aplication1[26]
                     , list_aplication1[27], list_aplication1[28], list_aplication1[29], list_aplication1[30]
                     , list_aplication1[31], list_aplication1[32], list_aplication1[33], list_aplication1[34]
                     , list_aplication1[35], list_aplication1[36], list_aplication1[37], list_aplication1[38]
                     , list_aplication1[39]
                     , id_clients))
        conn.commit()
        conn.close()
    # если не было постоянной заявки тогда создадим её
    else:
        conn = sq.connect('Works.db')
        cur = conn.cursor()
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
                    (int(id_clients), name_clients, list_aplication1[0], list_aplication1[1], list_aplication1[2]
                     , list_aplication1[3], list_aplication1[4], list_aplication1[5], list_aplication1[6]
                     , list_aplication1[7], list_aplication1[8], list_aplication1[9], list_aplication1[10]
                     , list_aplication1[11], list_aplication1[12], list_aplication1[13], list_aplication1[14]
                     , list_aplication1[15], list_aplication1[16], list_aplication1[17], list_aplication1[18]
                     , list_aplication1[19], list_aplication1[20], list_aplication1[21], list_aplication1[22]
                     , list_aplication1[23], list_aplication1[24], list_aplication1[25], list_aplication1[26]
                     , list_aplication1[27], list_aplication1[28], list_aplication1[29], list_aplication1[30]
                     , list_aplication1[31], list_aplication1[32], list_aplication1[33], list_aplication1[34]
                     , list_aplication1[35], list_aplication1[36], list_aplication1[37], list_aplication1[38]
                     , list_aplication1[39]))

        conn.commit()
        conn.close()
    return True


# УДАЛИМ - ПОСТОЯННУЮ заявку
def del_permanent_applications(id_client, name_table):
    conn = sq.connect('Works.db')
    cur = conn.cursor()
    cur.execute(f'''DELETE  from {name_table} where ClientsID == {id_client}''')
    conn.commit()
    conn.close()
    return True


# УДАЛИМ -  заявку
def del_applications(id_client):
    # получаем имя таблицы "сегодняшнюю дату"
    date_today = datetime.datetime.today()
    # получаем завтрашнюю дату
    date_tomorrow = date_today + datetime.timedelta(days=1)
    # создаём переменную с завтрашней датой в удобном формате
    name_table = date_tomorrow.strftime('day_%d_%m_%y')

    conn = sq.connect('Works.db')
    cur = conn.cursor()
    cur.execute(f'''DELETE  from {name_table} where ClientsID == {id_client}''')
    conn.commit()
    conn.close()
    return True


# КЛИЕНТ - добавляем в базу данных
def add_clients(list_clients):
    conn = sq.connect('Works.db')
    cur = conn.cursor()
    cur.execute('''insert into Clients(Name, Phone_number, Address, Name_shop, Город, Проводка )
                   values(?, ?, ?, ?, ?, ?)''', (list_clients[0], list_clients[1], list_clients[2], list_clients[3],
                                                 list_clients[4], list_clients[5]))
    conn.commit()
    conn.close()
    return True


# КЛИЕНТ запрос информации о клиенте по id для изменения данных
def get_info_client(id_client):
    conn = sq.connect('Works.db')
    cur = conn.cursor()
    cur.execute(f'''select * from Clients where ClientsID == {id_client}''')
    data_clients = []
    for i in cur.fetchone():
        data_clients.append(i)
    conn.commit()
    conn.close()
    return data_clients


# КЛИЕНТ - добавляем изменения в bd
def change_clients(list_clients):
    conn = sq.connect('Works.db')
    cur = conn.cursor()
    cur.execute(f'''UPDATE Clients set Name = ?,
                                       Phone_number = ?,
                                       Address = ?,
                                       Name_shop = ?,
                                       Город = ?,
                                       Проводка = ?
                                       where ClientsID == ?''',
                (list_clients[1], list_clients[2], list_clients[3], list_clients[4], list_clients[5],
                 list_clients[6], list_clients[0]))
    conn.commit()
    conn.close()

    return True


# КЛИЕНТ - удаляем из bd
def del_clients(id_clients):
    conn = sq.connect('Works.db')
    cur = conn.cursor()
    cur.execute(f'''DELETE from Clients WHERE ClientsID == {id_clients} ''')
    conn.commit()
    conn.close()

    return True


# ХЛЕБ - добавляем в bd
def add_brod(list_data_brod_add):
    conn = sq.connect('Works.db')
    cur = conn.cursor()
    cur.execute('''insert into Brod(Имя, Вес, Цена, Цена_Славгород, Фото)
                   values(?, ?, ?, ?, ?)''',
                (list_data_brod_add[0], list_data_brod_add[1], list_data_brod_add[2], list_data_brod_add[3],
                 list_data_brod_add[4]))
    conn.commit()
    conn.close()
    return True


# Вывод списка хлеба Прайса для Ярового из bd
def price_brod():
    conn = sq.connect('Works.db')
    cur = conn.cursor()
    cur.execute('''select ХлебID, Имя, Вес, Цена, Цена_Славгород, Фото from Brod ''')
    data_brod = []
    for i in cur.fetchall():
        data_brod.append(i)
    conn.close()
    return data_brod


# ХЛЕБ - вносим изменения в bd
def change_brod(list_data_brod_change):
    conn = sq.connect('Works.db')
    cur = conn.cursor()
    cur.execute(f'''UPDATE Brod set Имя = ?,
                                     Вес = ?,
                                     Цена = ?,
                                     Цена_Славгород = ?,
                                     Фото = ?
                                 where ХлебID == ?''',
                (list_data_brod_change[1], list_data_brod_change[2], list_data_brod_change[3], list_data_brod_change[4],
                 list_data_brod_change[5], list_data_brod_change[0]))
    conn.commit()
    conn.close()
    return True


# Хлеб - удаляем хлеб из bd
def del_brod(id_brod):
    conn = sq.connect('Works.db')
    cur = conn.cursor()
    cur.execute(f''' DELETE from Brod
                     WHERE ХлебID == {id_brod} ''')
    conn.commit()
    conn.close()
    return True


# финиш - помещаем постоянные заявки(нужного нам дня) в список для добавления их в заявку завтрашнего дня
def add_permanent_app():
    # получаем сегодняшнюю дату
    date_today = datetime.datetime.today()
    # получаем завтрешнюю дату
    date_tomorrow = date_today + datetime.timedelta(days=1)
    # создаём переменную с завтрешней датой в удобном формате
    name_table_application = date_tomorrow.strftime('day_%d_%m_%y')
    # создаём переменную и присваиваем ей название сегоднешнего дня недели
    weekday = datetime.datetime.today().strftime('%A')

    conn = sq.connect('Works.db')
    cur = conn.cursor()
    x = []
    # если сегодня понедельник, запишем в список все постоянные заявки понедельника
    if weekday == 'Monday':
        cur.execute('''select * from Вторник''')
        x = cur.fetchall()
    # если сегодня вторник, запишем в список все постоянные заявки вторника
    if weekday == 'Tuesday':
        cur.execute('''select * from Среда''')
        x = cur.fetchall()
    # если сегодня среда, запишем в список все постоянные заявки среды
    if weekday == 'Wednesday':
        cur.execute('''select * from Четверг''')
        x = cur.fetchall()
    # если сегодня четверг, запишем в список все постоянные заявки четверга
    if weekday == 'Thursday':
        cur.execute('''select * from Пятница''')
        x = cur.fetchall()
    # если сегодня пятница, запишем в список все постоянные заявки пятницы
    if weekday == 'Friday':
        cur.execute('''select * from Суббота''')
        x = cur.fetchall()
    # если сегодня воскресенье, запишем в список все постоянные заявки субботы
    if weekday == 'Sunday':
        cur.execute('''select * from Понедельник''')
        x = cur.fetchall()
    # запишем заявки из нашего списка в таблицу заявок завтрешнего дня
    # если их там ещё нет
    # для этого запишем в список id клиентов из таблицы заявок
    conn = sq.connect('Works.db')
    cur = conn.cursor()
    cur.execute(f'''select ClientsID, Город, Проводка from {name_table_application}''')
    id_client = []
    for i in cur.fetchall():
        for c in i:
            id_client.append(c)
    # если в нашем списке нет клиента с таким id, то внесем его в таблицу заявок
    for list_application in x:
        # узнаем город и статус клиента
        citi_clients = citi_wiring_clients(list_application[0])[0]
        wiring_clients = citi_wiring_clients(list_application[0])[1]
        # если этот клиент еще не сделал на сегодня заявку, то запишем её
        if list_application[0] not in id_client:
            cur.execute(f'''insert into {name_table_application} (
                                                                       ClientsID,
                                                                       Name_Clients,
                                                                       Город,
                                                                       Проводка,
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
            values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                        (list_application[0], list_application[1], citi_clients, wiring_clients, list_application[2]
                         , list_application[3], list_application[4], list_application[5], list_application[6]
                         , list_application[7], list_application[8], list_application[9], list_application[10]
                         , list_application[11], list_application[12], list_application[13], list_application[14]
                         , list_application[15], list_application[16], list_application[17], list_application[18]
                         , list_application[19], list_application[20], list_application[21], list_application[22]
                         , list_application[23], list_application[24], list_application[25], list_application[26]
                         , list_application[27], list_application[28], list_application[29], list_application[30]
                         , list_application[31], list_application[32], list_application[33], list_application[34]
                         , list_application[35], list_application[36], list_application[37], list_application[38]
                         , list_application[39], list_application[40], list_application[41]))

            conn.commit()
    conn.close()


# зайдем в bd и поместим в список клиентов Яровских проводных
def app_jr_pr(list_name_brod2_osnov):
    # получаем сегодняшнюю дату
    date_today = datetime.datetime.today()
    # получаем завтрешнюю дату
    date_tomorrow = date_today + datetime.timedelta(days=1)
    # создаём переменную с завтрешней датой в удобном формате
    name_table_application = date_tomorrow.strftime('day_%d_%m_%y')
    list_val = []
    conn = None
    try:

        conn = sq.connect('Works.db')
        cur = conn.cursor()
        cur.execute(f'''select Name_Clients,
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
                                  Пряники
                                   from {name_table_application} where Город == ? and Проводка == ?''',
                    ('Яровое', 'п'))
        list_val1 = cur.fetchall()

        for val in list_val1:
            list_val.append(list(val))

        # теперь подсчитаем итог и по столбцам для проводных яровских клиентов и запишим в наш список(list_val)
        list_sum_clients1_1 = ['итого']
        list_sum_clients1_1_dable = []
        # с помощью цикла пройдемся по столбцам, подсчитаем их суммы и запишим их в список(list_sum_clients1_1)
        for brod in list_name_brod2_osnov:
            cur.execute(
                f'''select sum ({brod}) from {name_table_application} where Город == ? and Проводка == ?''',
                ('Яровое', 'п'))
            list_sum_clients1_1_dable.append(cur.fetchone())
        for i in list_sum_clients1_1_dable:
            for c in i:
                list_sum_clients1_1.append(c)
        # запишим в список заказов для распечатки список суммы стольцов коиентов до 14 id
        list_val.append(list_sum_clients1_1)

        # считаем клиентов ярового непроводных
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
                                              from {name_table_application} where Город == ? and Проводка == ?''',
                    ('Яровое', 'н'))
        list_val1 = cur.fetchall()
        for val in list_val1:
            list_val.append(list(val))

            # теперь подсчитаем сумму проводных и непроводных клиентов и запишем в наш список(list_val)
        list_sum_clients1_2 = ['всего']
        list_sum_clients1_2_dable = []
        # с помощью цикла пройдемся по столбцам, подсчитаем их суммы и запишим их в список(list_sum_clients1_1)
        for brod in list_name_brod2_osnov:
            cur.execute(f'''select sum ({brod}) from {name_table_application} where Город == ?''',
                        ('Яровое',))
            list_sum_clients1_2_dable.append(cur.fetchone())
        for i in list_sum_clients1_2_dable:
            for c in i:
                list_sum_clients1_2.append(c)
        # запишим в список заказов для распечатки список суммы стольцов колиентов Ярового
        list_val.append(list_sum_clients1_2)

    except sq.Error as err:
        print('Ошибка бызы данных', err)
    finally:
        if conn != None:
            conn.close()

    return list_val


# Славгород
def app_sl(list_name_brod2_osnov):
    # получаем сегодняшнюю дату
    date_today = datetime.datetime.today()
    # получаем завтрешнюю дату
    date_tomorrow = date_today + datetime.timedelta(days=1)
    # создаём переменную с завтрешней датой в удобном формате
    name_table_application = date_tomorrow.strftime('day_%d_%m_%y')

    # создаём список заявок Славгорода для распечатки
    list_val_slav = []
    # подключимся к базе данных и соберем информацию и записываем её наш список,
    # но сначала считаем клиентов Славгорода проводных
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
                                              from {name_table_application} where Город == ? and Проводка == ?''',
                    ('Славгород', 'п'))
        list_val1 = cur.fetchall()
        for val in list_val1:
            list_val_slav.append(list(val))

        # теперь подсчитаем итог и по столбцам для проводных клиентов и запишим в наш список(list_val_slav)
        list_sum_clients2_1 = ['итого']
        list_sum_clients2_1_dable = []
        # с помощью цикла пройдемся по столбцам, подсчитаем их суммы и запишим их в список(list_sum_clients2_1)
        for brod in list_name_brod2_osnov:
            cur.execute(f'''select sum ({brod}) from {name_table_application}
                                                where Город == ? and Проводка == ?''',
                    ('Славгород', 'п'))
            list_sum_clients2_1_dable.append(cur.fetchone())
        for i in list_sum_clients2_1_dable:
            for c in i:
                list_sum_clients2_1.append(c)
        # запишем в список заказов для распечатки список суммы столбцов проводимых клиентов
        list_val_slav.append(list_sum_clients2_1)

        # считаем клиентов славгорода не проводных
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
                                                         from {name_table_application} 
                                                         where Город == ? and Проводка == ?''',
                    ('Славгород', 'н'))
        list_val1 = cur.fetchall()
        for val in list_val1:
            list_val_slav.append(list(val))

        # теперь подсчитаем сумму проводных и непроводных клиентов и запишем в наш список(list_val_slav)
        list_sum_clients2_1 = ['всего']
        list_sum_clients2_2_dable = []
        # с помощью цикла пройдемся по столбцам, подсчитаем их суммы и запишим их в список(list_sum_clients2_1)
        for brod in list_name_brod2_osnov:
            cur.execute(f'''select sum ({brod}) from {name_table_application}''')
            list_sum_clients2_2_dable.append(cur.fetchone())
        for i in list_sum_clients2_2_dable:
            for c in i:
                list_sum_clients2_1.append(c)
        # запишем в список заказов для распечатки список суммы столбцов клиентов проводных и не проводных id
        # до 41
        list_val_slav.append(list_sum_clients2_1)
    except sq.Error as err:
        print('Ошибка бызы данных', err)
    finally:
        if conn is not None:
            conn.close()

    return list_val_slav


# Создаем список для Галины Васильевны
def app_dop(list_name_brod2_dop):
    # получаем сегодняшнюю дату
    date_today = datetime.datetime.today()
    # получаем завтрашнюю дату
    date_tomorrow = date_today + datetime.timedelta(days=1)
    # создаём переменную с завтрашней датой в удобном формате
    name_table_application = date_tomorrow.strftime('day_%d_%m_%y')

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
                                              Сосиска_в_тесте from {name_table_application} ''')
        list_val1 = cur.fetchall()
        # если количество хлеба в заявке не 0, тогда запишем заявку клиента в список для печати
        for val in list_val1:
            if val[1] + val[2] + val[3] + val[4] + val[5] + val[6] + val[7] + val[8] + val[9] + val[10] + val[11] \
                    + val[12] != 0:
                list_val_dop.append(list(val))
        # теперь подсчитаем итог и по столбцам для всех клиентов и запишем в наш список(list_val_dop)
        list_sum_clients1_1 = ['итого']
        list_sum_clients1_1_dable = []
        # с помощью цикла пройдемся по столбцам, подсчитаем их суммы и запишем их в список(list_sum_clients1_1)
        for brod in list_name_brod2_dop:
            cur.execute(f'''select sum ({brod}) from {name_table_application}''')
            list_sum_clients1_1_dable.append(cur.fetchone())
        for i in list_sum_clients1_1_dable:
            for c in i:
                list_sum_clients1_1.append(c)
        # запишим в список заказов для распечатки список суммы стольцов
        list_val_dop.append(list_sum_clients1_1)
    except sq.Error as err:
        print('Ошибка бызы данных', err)
    finally:
        if conn is not None:
            conn.close()

    return list_val_dop


# скачиваем формулы и помешаем в список
def formula_brod():
    formula = []
    # подключимся к базе данных и соберем информацию и записываем её наш список,
    # но сначала считаем клиентов Славгорода проводных
    conn = None
    try:

        conn = sq.connect('Works.db')
        cur = conn.cursor()
        cur.execute('''select * from formula ''')
        list_val1 = cur.fetchall()
        for val in list_val1:
            formula.append(list(val))

    except sq.Error as err:
        print('Ошибка бызы данных', err)
    finally:
        if conn is not None:
            conn.close()

    return formula
import sqlite3 as sq
import datetime


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


# Создадим функцию вывода списка цен Ярового
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
def create_request_table(id_clients, name_clients, list_aplication1):
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
        print('не в списке')
        # открываем базу данных и записываем данные из списка заявок в таблицу заявок
        conn = sq.connect('Works.db')
        cur = conn.cursor()
        cur.execute(f'''insert into {name_table_application} (
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
    cur.execute('''insert into Clients(Name, Phone_number, Address, Name_shop)
                   values(?, ?, ?, ?)''', (list_clients[0], list_clients[1], list_clients[2], list_clients[3]))
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
                                       Name_shop = ?
                                       where ClientsID == ?''',
                (list_clients[1], list_clients[2], list_clients[3], list_clients[4], list_clients[0]))
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

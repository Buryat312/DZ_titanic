"""
Скачайте этот файл и положите в папку. 
Откройте postgres и создайте там базу данных **titanic**. 
Создайте пользователя postgres и дайте ему все привилегии для этой базы данных. 
Затем в той же папке, куда вы положили скачанный файл, создайте файл **reader.py**.
"""
# CREATE DATABASE titanic;
# CREATE USER sultan WITH ENCRYPTED PASSWORD '123';
# GRANT ALL PRIVILEGES ON DATABASE titanic TO sultan;

import psycopg2
conn = psycopg2.connect(dbname='titanic', user='sultan', password='123')
cur = conn.cursor()
cur.execute("""DROP TABLE IF EXISTS passengers;
    CREATE TABLE IF NOT EXISTS passengers(
    id integer,
    survived integer,
    class integer,
    name text,
    sex varchar(50),
    age varchar(50),
    sibsp integer,
    parch integer,
    ticket varchar(255),
    fare numeric NULL,
    cabin varchar(255) NULL,
    embarked varchar(50)
)
""")
with open(r'titanic.txt', 'r') as f:
    next(f)
    cur.copy_from(f, 'passengers', sep='|')

conn.commit()
# начало вашего кода
#1) Выведет имена всех погибших людей
# SELECT name FROM passengers WHERE survived=0; # 549 survived
def did_n_survived():
    cur.execute("SELECT name FROM passengers WHERE survived=0;")
    all_ddnt_survived = cur.fetchall()
    for name in all_ddnt_survived:
        print(name)
did_n_survived()

# 2) Высчитает процент выживших среди:
# - Женщин первого класса
# SELECT COUNT(*) FROM passengers WHERE sex='female' AND class=1 AND survived=1; #91 females survived out of 94

def females_f_class():
    cur.execute("SELECT COUNT(*) FROM passengers WHERE sex='female' AND class=1 AND survived=1;")
    females_f = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM passengers WHERE sex='female' AND class=1;")
    all_fem_f_class = cur.fetchone()[0]
    fem_counting = females_f*100/all_fem_f_class
    return fem_counting
print(f'Процент выживших среди женщин первого класса = {females_f_class():.2f}%')

# # - Мужчин младше 20 лет третьего класса
# SELECT COUNT(*) FROM passengers WHERE sex='male' AND class=3 AND age<'20' AND survived=1; #15 males survived out of 143

def mens_third_class():
    cur.execute("SELECT COUNT(*) FROM passengers WHERE sex='male' AND class=3 AND age<'20' AND survived=1;")
    mens_class = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM passengers WHERE sex='male' AND class=3 AND age<'20';")
    all_m_third_class = cur.fetchone()[0]
    mens_counting = mens_class*100/all_m_third_class
    return mens_counting
print(f'Процент выживших среди мужчин младше 20 лет третьего класса = {mens_third_class():.2f}%')

# # - Пассажиров второго класса старше 30 лет
# SELECT COUNT(*) FROM passengers WHERE class=2 AND age>'30' AND survived=1; # 39 passengers  survived out of 84
def passengers_sec_class():
    cur.execute("SELECT COUNT(*) FROM passengers WHERE class=2 AND age>'30' AND survived=1;")
    pass_sec_class = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM passengers WHERE class=2 AND age>'30';")
    all_pass_sec_class = cur.fetchone()[0]
    pass_sec_class_counting = pass_sec_class*100/all_pass_sec_class
    return pass_sec_class_counting
print(f'Процент выживших среди пассажиров второго класса старше 30 лет = {passengers_sec_class():.2f}%')

# # - Женщин второго класса, севшие на борт в порту Cherbourg
# SELECT COUNT(*) FROM passengers WHERE sex='female' AND class=2 AND embarked='C' AND survived=1; #7 females survived out of 7
def female_sec_class():
    cur.execute("SELECT COUNT(*) FROM passengers WHERE sex='female' AND class=2 AND embarked='C' AND survived=1;")
    fem_sec_class = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM passengers WHERE sex='female' AND class=2 AND embarked='C';")
    all_fem_sec_class = cur.fetchone()[0]
    fem_sec_class_counting = fem_sec_class*100/all_fem_sec_class
    return fem_sec_class_counting
print(f'Процент выживших среди женщин второго класса, севшие на борт в порту Cherbourg = {female_sec_class():.2f}%')

# # - Пассажиров имевших на борту братьев или сестёр
# SELECT COUNT(*) FROM passengers WHERE sibsp!=0 AND survived=1; # 132 passengers with sibsp survived out of 283
def passengers_with_sblngs():
    cur.execute("SELECT COUNT(*) FROM passengers WHERE sibsp!=0 AND survived=1;")
    pass_with_sblngs = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM passengers WHERE sibsp!=0;")
    all_passengers = cur.fetchone()[0]
    pass_with_sblngs_counting = pass_with_sblngs*100/all_passengers
    return pass_with_sblngs_counting
print(f'Процент выживших среди пассажиров имевших на борту братьев или сестёр = {passengers_with_sblngs():.2f}%')

# 3) Посчитает средний возраст погибших людей

def average_age():
    cur.execute("SELECT AVG(CAST(age AS FLOAT)) FROM passengers WHERE survived=0 AND age>'0';")
    avg_age = cur.fetchone()[0]
    print(f'Средний возраст погибших людей {round(avg_age)}')
average_age()

# 4) Порт, люди с которого, имели наибольший шанс выжить

def chance_to_survive():
    cur.execute("SELECT COUNT(*) FROM passengers WHERE embarked='Q';")
    all_q_pass = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM passengers WHERE embarked='Q' AND survived=1;")
    survived_q_pass = cur.fetchone()[0]
    queen_port = survived_q_pass*100/all_q_pass
    cur.execute("SELECT COUNT(*) FROM passengers WHERE embarked='S';")
    all_s_pass = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM passengers WHERE embarked='S' AND survived=1;")
    survived_s_pass = cur.fetchone()[0]
    south_port = survived_s_pass*100/all_s_pass
    cur.execute("SELECT COUNT(*) FROM passengers WHERE embarked='C';")
    all_c_pass = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM passengers WHERE embarked='C' AND survived=1;")
    survived_c_pass = cur.fetchone()[0]
    cherb_port = survived_c_pass*100/all_c_pass
    dct = {
        'Cherbourg': cherb_port,
        'Queenstown': queen_port,
        'Southampton': south_port,
    }
    lst = [cherb_port, queen_port, south_port]
    for i, j in dct.items():
        if j == max(lst):
            print(f'{i} - {j:.4}% - Порт, люди с которого, имели наибольший шанс выжить')
chance_to_survive()

cur.close()
conn.close()


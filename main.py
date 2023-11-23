import sqlite3
from datetime import datetime, date


def validate_date(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def calculate_age(birth_date: date, death_date: date) -> int:
    age = death_date.year - birth_date.year - ((death_date.month, death_date.day) < (birth_date.month, birth_date.day))
    return age


def view_corpses():
    cursor.execute('SELECT * FROM corpses')
    rows = cursor.fetchall()
    for row in rows:
        print(row)


def add_corpse():
    name = input("Введите имя: ")
    cause_of_death = input("Введите причину смерти: ")

    # Проверка ввода даты смерти
    while True:
        date_of_death = input("Введите дату смерти (гггг-мм-дд): ")
        if validate_date(date_of_death) and datetime.strptime(date_of_death, '%Y-%m-%d') <= datetime.today():
            break
        else:
            print("Некорректная дата смерти. Попробуйте снова.")

    # Ввод даты рождения с валидацией
    while True:
        birth_date = input("Введите дату рождения (гггг-мм-дд): ")
        if validate_date(birth_date) and datetime.strptime(birth_date, '%Y-%m-%d') <= datetime.today():
            break
        else:
            print("Некорректная дата рождения. Попробуйте снова.")

    age = calculate_age(datetime.strptime(birth_date, '%Y-%m-%d'), datetime.strptime(date_of_death, '%Y-%m-%d'))

    cursor.execute('''
        INSERT INTO corpses (name, cause_of_death, date_of_death, birth_date, age)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, cause_of_death, date_of_death, birth_date, age))
    conn.commit()


def update_corpse():
    view_corpses()
    corps_id = int(input("Введите ID трупа для обновления: "))
    name = input("Введите новое имя: ")
    cause_of_death = input("Введите новую причину смерти: ")

    # Проверка ввода даты смерти
    while True:
        date_of_death = input("Введите новую дату смерти (гггг-мм-дд): ")
        if validate_date(date_of_death) and datetime.strptime(date_of_death, '%Y-%m-%d') <= datetime.today():
            break
        else:
            print("Некорректная дата смерти. Попробуйте снова.")

    # Ввод новой даты рождения с валидацией
    while True:
        birth_date = input("Введите новую дату рождения (гггг-мм-дд): ")
        if validate_date(birth_date) and datetime.strptime(birth_date, '%Y-%m-%d') <= datetime.today():
            break
        else:
            print("Некорректная дата рождения. Попробуйте снова.")

    age = calculate_age(datetime.strptime(birth_date, '%Y-%m-%d'), datetime.strptime(date_of_death, '%Y-%m-%d'))

    cursor.execute('''
        UPDATE corpses
        SET name=?, cause_of_death=?, date_of_death=?, birth_date=?, age=?
        WHERE id=?
    ''', (name, cause_of_death, date_of_death, birth_date, age, corps_id))
    conn.commit()


def delete_corpse():
    view_corpses()
    corps_id = int(input("Введите ID трупа для удаления: "))
    cursor.execute('DELETE FROM corpses WHERE id=?', (corps_id,))
    conn.commit()


def search_corpse():
    name = input("Введите имя для поиска: ")
    cursor.execute('SELECT * FROM corpses WHERE name LIKE ?', ('%' + name + '%',))
    rows = cursor.fetchall()

    if not rows:
        print(f"Трупа с именем '{name}' не найдено.")
    else:
        for row in rows:
            print(row)


def print_menu():
    print("1. Просмотреть трупы")
    print("2. Добавить труп")
    print("3. Обновить данные о трупе")
    print("4. Удалить труп")
    print("5. Найти труп")
    print("0. Выйти")


def main():
    while True:
        print_menu()
        choice = input("Выберите действие: ")

        if choice == "1":
            view_corpses()
        elif choice == "2":
            add_corpse()
        elif choice == "3":
            update_corpse()
        elif choice == "4":
            delete_corpse()
        elif choice == "5":
            search_corpse()
        elif choice == "0":
            break
        else:
            print("Неверный выбор. Попробуйте еще раз.")


if __name__ == "__main__":
    conn = sqlite3.connect('morg_database.db')
    cursor = conn.cursor()

    try:
        main()
    finally:
        conn.close()

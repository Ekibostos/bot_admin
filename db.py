import os
from typing import Dict, List, Tuple

import sqlite3


conn = sqlite3.connect(os.path.join("db", "users.db"), check_same_thread=False)
cursor = conn.cursor()


def insert_new_user(chat_id, capcha):
    """Сохраняет в таблицу пользователей не прошедших проверку ID пользователя и число которое для него будет правильным ответом"""
    column_values = {"user_id": chat_id, "capcha": capcha}
    columns = ', '.join( column_values.keys() )
    values = [tuple(column_values.values())]
    placeholders = ", ".join( "?" * len(column_values.keys()) )
    cursor.executemany(
        f"INSERT INTO newuser "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    conn.commit()

def insert(chat_id, word = "word"):
    """Сохраняет ID пользователя в таблицу прошедших проверку, может сохранять ещё какую-нибудь информацию, но я не придумал какую"""
    column_values = {"user_id": chat_id, "word": word}
    columns = ', '.join( column_values.keys() )
    values = [tuple(column_values.values())]
    placeholders = ", ".join( "?" * len(column_values.keys()) )
    cursor.executemany(
        f"INSERT INTO usersid "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    conn.commit()

def remove_new_user_from_table(chat_id):
    """Удаляет пользователя из таблицы не прошедших проверку"""
    ex = f"DELETE FROM newuser WHERE user_id = {chat_id}"
    cursor.execute(ex)
    conn.commit()

def get_all_new_users():
    """Возврашает список всех пользователей не прошедших проверку"""
    cursor.execute(f"SELECT user_id FROM newuser")
    rows = cursor.fetchall()
    return rows

def get_all_users():
    """Возврашает список всех пользователей прошедших проверку"""
    cursor.execute(f"SELECT user_id FROM usersid")
    rows = cursor.fetchall()
    return rows

def update_capcha(chat_id, capcha):
    """Обновляет число которое будет правльным ответом для пользователя не прошедшего проверку.
    Нужно в случае если человек не прошёл проверку, вышел из чата а потом снова зашёл"""
    ex = "UPDATE newuser SET capcha = ? WHERE user_id = ?"
    cursor.execute(ex,(capcha, chat_id))
    conn.commit()

def get_capcha_or_false(user_id):
    """Возвращает число которое будет правльным ответом для пользователя не прошедшего проверку"""
    cursor.execute(f"select capcha "
                   f"from newuser where user_id == '{user_id}'")
    capcha = cursor.fetchone()
    if not capcha:
        return False
    return capcha

def _init_db():
    """Инициализирует БД"""
    with open("createdb.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exists():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='usersid'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()

check_db_exists()


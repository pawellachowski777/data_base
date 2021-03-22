import psycopg2
from configparser import ConfigParser
import time


def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def check_flag(flag):
    if flag == 1:
        query = f"SELECT id FROM a_b WHERE flag = {flag} ORDER BY id;"
        return query

    if flag == 4:
        query = f"SELECT id FROM a_b WHERE flag = {flag} AND CURRENT_DATE - updated_at  >= 1 ORDER BY id;"
        return query


def fetch_query(cur, query):
    cur.execute(query)
    fetch = cur.fetchone()
    return fetch


def recalculate(sql_row, cur, conn, sleep_time=20):

    # aktualizacja falgi z 4 na 2
    query_id = sql_row[0]
    print("selected row with id", query_id)
    query_flag_to_1 = f"UPDATE a_b SET flag = 2 WHERE id = {query_id};"
    cur.execute(query_flag_to_1)
    conn.commit()

    # przeliczenie wyniku
    query_calculate = f"UPDATE a_b SET result = a + b WHERE id = {query_id};"
    cur.execute(query_calculate)
    time.sleep(sleep_time)
    conn.commit()

    # zmiana flagi z 2 na 3
    query_flag_to_3 = f"UPDATE a_b SET flag = 3 WHERE id = {query_id} AND flag = 2;"
    cur.execute(query_flag_to_3)
    conn.commit()

    # aktualizacja updated_at
    query_updated_at = f"UPDATE a_b SET updated_at = CURRENT_DATE WHERE id = {query_id};"
    cur.execute(query_updated_at)
    print("row updated")
    conn.commit()


def sql_operation():
    # połączenie z bazą
    params = config()
    conn = psycopg2.connect(**params)

    # szukanie rezultatu z flaga = 4 i data aktualizacji starszą niż jeden dzień
    query_flag_is_4 = check_flag(4)
    cur = conn.cursor()
    sql_flag_is_4 = fetch_query(cur, query_flag_is_4)

    # jeżeli znajdzie, obilcza ponownie
    if sql_flag_is_4 is not None:
        recalculate(sql_flag_is_4, cur, conn)

    else:
        # jeżeli nie znajdzie, szuka czy istnieją rekordy z flagą 1
        query_flag_is_1 = check_flag(1)
        sql_flag_is_1 = fetch_query(cur, query_flag_is_1)

        if sql_flag_is_1 is not None:
            # jeżeli znajdzie, oblicza
            recalculate(sql_flag_is_1, cur, conn)

        else:
            # jeżeli nie znajdzie, baza jest aktualna
            print("Base up to date")

    conn.close()


def sql_take_row():
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    query_flag_is_4 = check_flag(4)
    query_flag_is_1 = check_flag(1)

    sql_flag_is_4 = fetch_query(cur, query_flag_is_4)
    sql_flag_is_1 = fetch_query(cur, query_flag_is_1)

    if sql_flag_is_4 is not None or sql_flag_is_1 is not None:
        return True
    conn.close()

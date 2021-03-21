def connect(host="localhost", database="baza", user="postgres", password="1234"):
    import psycopg2

    conn = psycopg2.connect(host=host,
                            database=database,
                            user=user,
                            password=password)
    return conn


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
    import time

    # aktualizacja falgi z 4 na 2
    query_id = sql_row[0]
    print("selected row with id", query_id)
    query_flag_to_1 = f"UPDATE a_b SET flag = 2 WHERE id = {query_id}"
    cur.execute(query_flag_to_1)
    conn.commit()

    # przeliczenie wyniku
    query_calculate = f"UPDATE a_b SET result = a + b WHERE id = {query_id}"
    cur.execute(query_calculate)
    time.sleep(sleep_time)
    conn.commit()

    # zmiana flagi z 2 na 3
    query_flag_to_3 = f"UPDATE a_b SET flag = 3 WHERE id = {query_id}"
    cur.execute(query_flag_to_3)
    conn.commit()

    # aktualizacja updated_at
    query_updated_at = f"UPDATE a_b SET updated_at = CURRENT_DATE WHERE id = {query_id}"
    cur.execute(query_updated_at)
    print("row updated")
    conn.commit()


def sql_operation():
    import time
    # połączenie z bazą
    conn = connect()

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
            # jeżeli znajdzie, obliczba ponownie
            recalculate(sql_flag_is_1, cur, conn)

        else:
            # jeżeli nie znajdzie, baza jest aktualna
            print("Base up to date")
            time.sleep(5)

    conn.close()


def sql_take_row():
    conn = connect()
    query_flag_is_4 = check_flag(4)
    query_flag_is_1 = check_flag(1)
    cur = conn.cursor()
    sql_flag_is_4 = fetch_query(cur, query_flag_is_4)
    sql_flag_is_1 = fetch_query(cur, query_flag_is_1)

    if sql_flag_is_4 is not None or sql_flag_is_1 is not None:
        return True
    conn.close()

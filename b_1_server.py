def sql_operation(host="localhost", database="baza", user="postgres", password="1234"):
    import psycopg2
    import time

    conn = psycopg2.connect(host=host,
                            database=database,
                            user=user,
                            password=password)

    # wybranie rezultatu z flaga = 4 i data aktualizacji starszą niż jeden dzień
    query_error = "SELECT id FROM a_b WHERE flag = 4 AND CURRENT_DATE - updated_at  >= 1;"
    cur = conn.cursor()
    cur.execute(query_error)
    sql_error = cur.fetchone()

    if sql_error is not None:

        # aktualizacja falgi z 4 na 2
        query_id = sql_error[0]
        print(query_id)
        query_flag_to_1 = f"UPDATE a_b SET flag = 2 WHERE id = {query_id}"
        cur.execute(query_flag_to_1)

        # przeliczenie wyniku
        query_calculate = f"UPDATE a_b SET result = a + b WHERE id = {query_id}"
        cur.execute(query_calculate)
        time.sleep(10)
        conn.commit()

        # zmiana flagi z 2 na 3
        query_flag_to_3 = f"UPDATE a_b SET flag = 3 WHERE id = {query_id}"
        cur.execute(query_flag_to_3)

        # aktualizacja updated_at
        query_updated_at = f"UPDATE a_b SET updated_at = CURRENT_DATE WHERE id = {query_id}"
        cur.execute(query_updated_at)
        conn.commit()

    else:

        # sprawdzenie czy istnieją rekordy z flagą 1
        query_flag_is_1 = "SELECT id FROM a_b WHERE flag = 1;"
        cur.execute(query_flag_is_1)
        sql_flag_is_1 = cur.fetchone()

        if sql_flag_is_1 is not None:

            # zmiana flagi z 1 na 2
            query_id = sql_flag_is_1[0]
            print(query_id)
            query_flag_to_2 = f"UPDATE a_b SET flag = 2 WHERE id = {query_id}"
            cur.execute(query_flag_to_2)
            conn.commit()

            # przeliczenie wyniku
            query_calculate = f"UPDATE a_b SET result = a + b WHERE id = {query_id}"
            cur.execute(query_calculate)
            time.sleep(10)
            conn.commit()

            # zmiana flagi z 2 na 3
            query_flag_to_3 = f"UPDATE a_b SET flag = 3 WHERE id = {query_id}"
            cur.execute(query_flag_to_3)

            # aktualizacja updated_at
            query_updated_at = f"UPDATE a_b SET updated_at = CURRENT_DATE WHERE id = {query_id}"
            cur.execute(query_updated_at)
            conn.commit()
        else:
            time.sleep(5)
            print("Base up to date")

    # print(sql_flag_is_1)
    conn.close()


from client import Client

if __name__ == "__main__":
    client = Client()
    print("#################### CONNECT ####################")
    with client.connect("postgres", host="localhost", port=5432, database="postgres", password="postgres") as conn:
        with conn.cursor() as cur:
            print("******************** CREATE TABLE ********************")
            cur.execute("CREATE TABLE book (id SERIAL, title TEXT)")

            print("==================== INSERT DATA ====================")
            cur.execute("INSERT INTO book (title) VALUES ('abcdef')")
            cur.execute("INSERT INTO book (title) VALUES ('あいうえお')")

            print("<<<<<<<<<<<<<<<<<<<< COMMIT >>>>>>>>>>>>>>>>>>>>")
            conn.commit()

            print("++++++++++++++++++++ FETCH ALL ++++++++++++++++++++")
            data = cur.execute("SELECT * FROM book").fetchall()
            # data = cur.execute("EXPLAIN ANALYZE SELECT * FROM book").fetchall()
            # data = cur.execute("SELECT count(id) FROM book").fetchall()

            print(data)

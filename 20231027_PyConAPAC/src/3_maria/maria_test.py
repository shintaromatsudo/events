import pymysql

with pymysql.connect(host="localhost", user="maria", password="maria", db="maria") as conn:
    with conn.cursor() as cur:
        # Execute a command: this creates a new table
        cur.execute(
            """
            CREATE TABLE test (
                id serial PRIMARY KEY,
                num integer,
                data text)
            """
        )

        # Pass data to fill a query placeholders and let Psycopg perform
        # the correct conversion (no SQL injections!)
        cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))

        print(cur.execute("SELECT * FROM test"))
        print(cur.fetchone())

        # Make the changes to the database persistent
        conn.commit()

import psycopg

# https://www.psycopg.org/psycopg3/docs/basic/usage.html
with psycopg.connect("host=localhost port=5432 dbname=postgres user=postgres password=postgres") as conn:
    # Open a cursor to perform database operations
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

        print(cur.execute("SELECT * FROM test").fetchone())

        # Make the changes to the database persistent
        conn.commit()

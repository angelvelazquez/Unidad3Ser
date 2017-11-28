import psycopg2


def create_tables():

    """Create tabless in the Postgresql database"""

    command = ("""CREATE TABLE chain_length(
                  id SERIAL PRIMARY KEY,
                  ts VARCHAR(35) NOT NULL,
                  chain VARCHAR(128) NOT NULL,
                  length INTEGER NOT NULL)""")

    connection = None
    try:
        # read the connection parameters
        dbconfg = {'host': '127.0.0.1',
                   'user': 'angel',
                   'password': '123',
                   'database': 'recuperacion', }
        connection = psycopg2.connect(**dbconfg)
        cursor = connection.cursor()
        # Create table one by one
        cursor.execute(command)
        # close communication with the PostgreSQLdatabase server
        cursor.close()
        #commit the changes
        connection.commit()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()


if __name__ == '__main__':
    create_tables()

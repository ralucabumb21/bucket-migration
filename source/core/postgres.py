import logging
import os
import psycopg2
from dotenv import load_dotenv
from psycopg2._psycopg import OperationalError

# Required to load the environment variables defined in .env
load_dotenv()

# Setup logger
logging.basicConfig(level=logging.INFO,
                    format="[%(asctime)s] [%(levelname)s] (%(filename)s:%(lineno)d): %(message)s",
                    datefmt='%Y.%m.%d-%H:%M:%S')
logger = logging.getLogger(__name__)


def connect_to_db():
    """
    Connects to a Postgres DB.
    """
    global cursor
    global connection
    try:
        connection = psycopg2.connect(host=os.environ.get('PG_HOST'),
                                      port=os.environ.get('PG_PORT'),
                                      user=os.environ.get('PG_USER'),
                                      password=os.environ.get('PG_PASSWORD'),
                                      dbname=os.environ.get('PG_DATABASE'))
        cursor = connection.cursor()
    except OperationalError as err:
        logger.error(err)


def close_db_connection():
    """
    Closes a DB connection
    """
    if connection:
        cursor.close()
        connection.close()
        logger.info("Closing PostgreSQL connection.")


def update_table(table_name, column_name):
    """
    Updates table DB

    Parameters
    ----------
    table_name : str, required
    column_name : str, required
    """
    connect_to_db()
    try:
        # Check if there are any records with image URL
        logger.info("Table Before updating record.")
        sql_select_query = 'select * from {} where {} LIKE \'image%\'' \
            .format(table_name, column_name)
        cursor.execute(sql_select_query)
        image_url_records = cursor.fetchall()

        # Update all rows in avatar_url column and replace image with avatar
        if image_url_records:
            logger.info("There were found %s avatar entry with image URL.\n Updating URLs...",
                        format(len(image_url_records)))
            sql_update_query = 'update {} set {} = replace({},\'image\',\'avatar\')' \
                .format(table_name, column_name, column_name)
            cursor.execute(sql_update_query)
            connection.commit()
            logger.info("Records Updated successfully.")
        else:
            logger.info("There are not avatar entry with image URL. Nothing to update.")

    except (Exception, psycopg2.Error) as error:
        logger.error("Error in update operation: %s", error)

    finally:
        # closing database connection.
        close_db_connection()
        return "Update query has finished."


def populate_db(min_range, max_range):
    """
    Populates the users and user_avatar table DB
    Set the range to create unique png files

    Parameters
    ----------
    min_range : int, required
    max_range : int, required
    """
    connect_to_db()
    # list of rows to be inserted
    db_user_avatar_entry_list = []
    for index in range(min_range, max_range):
        db_user_avatar_entry_list.append((index, "image/avatar-{}.png".format(str(index))))

    db_user_entry_list = []
    for index in range(min_range, max_range):
        db_user_entry_list.append((index, "user{}".format(str(index)), "user{}".format(str(index))))

    # cursor.mogrify() to insert multiple values
    users_args = ','.join(cursor.mogrify("(%s,%s,%s)", i).decode('utf-8')
                          for i in db_user_entry_list)

    # cursor.mogrify() to insert multiple values
    user_avatar_args = ','.join(cursor.mogrify("(%s,%s)", i).decode('utf-8')
                                for i in db_user_avatar_entry_list)

    # executing the sql statement
    cursor.execute("INSERT INTO users (user_id, username, password) VALUES " + users_args)

    cursor.execute("INSERT INTO user_avatar (user_id, avatar_url) VALUES " + user_avatar_args)

    # commiting changes
    connection.commit()

    # closing database connection.
    close_db_connection()

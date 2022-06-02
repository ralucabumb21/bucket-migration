import logging
import os
import psycopg2
from dotenv import load_dotenv

# Required to load the environment variables defined in .env
load_dotenv()

# Setup logger
logging.basicConfig(level=logging.INFO,
                    format="[%(asctime)s] [%(levelname)s] (%(filename)s:%(lineno)d): %(message)s",
                    datefmt='%Y.%m.%d-%H:%M:%S')
logger = logging.getLogger(__name__)


def update_table(table_name, column_name):
    try:
        connection = psycopg2.connect(host=os.environ.get('PG_HOST'),
                                      port=os.environ.get('PG_PORT'),
                                      user=os.environ.get('PG_USER'),
                                      password=os.environ.get('PG_PASSWORD'),
                                      dbname=os.environ.get('PG_DATABASE'))
        cursor = connection.cursor()

        # Check if there are any records with image URL
        logger.info("Table Before updating record.")
        sql_select_query = 'select * from {} where {} LIKE \'image%\''\
            .format(table_name, column_name)
        cursor.execute(sql_select_query)
        image_url_records = cursor.fetchall()

        # Update all rows in avatar_url column and replace image with avatar
        if image_url_records:
            logger.info("There were found avatar entry with image URL.\n Updating URLs...")
            sql_update_query = 'update {} set {} = replace({},\'image\',\'avatar\')'\
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
        if connection:
            cursor.close()
            connection.close()
            logger.info("Closing PostgreSQL connection.")

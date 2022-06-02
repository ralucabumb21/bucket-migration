from core import s3
from core import postgres
from utility import constans
from dotenv import load_dotenv

# Required to load the environment variables defined in .env
load_dotenv()

if __name__ == '__main__':
    s3.copy_object_from_a_bucket_to_another(constans.OLD_BUCKET, constans.OLD_BUCKET_PREFIX,
                                            constans.NEW_BUCKET, constans.NEW_BUCKET_PREFIX)
    postgres.update_table(constans.TABLE_NAME, constans.COLUMN_NAME)

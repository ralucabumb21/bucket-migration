from core import s3
from core import postgres
from utility import constans, util
from dotenv import load_dotenv

# Required to load the environment variables defined in .env
load_dotenv()

if __name__ == '__test_data_setup__':
    postgres.populate_db(8, 90)

    util.create_png_file_for_s3(constans.DATA_FILES_LOCATION, 8, 90)
    s3.upload_files_to_s3(constans.DATA_FILES_LOCATION, constans.FILE_NAME)

from core import s3
from core import postgres
from utility import constans, util
from dotenv import load_dotenv

# Required to load the environment variables defined in .env
load_dotenv()

util.create_png_file_for_s3(constans.DATA_FILES_LOCATION, constans.MIN_RANGE, constans.MAX_RANGE)

postgres.populate_db(constans.MIN_RANGE, constans.MAX_RANGE)
s3.upload_files_to_s3(constans.DATA_FILES_LOCATION, constans.FILE_NAME)

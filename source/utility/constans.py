# Setup source and destination bucket details
OLD_BUCKET = "legacy-s3-test"
OLD_BUCKET_PREFIX = "image"
NEW_BUCKET = "production-s3-test"
NEW_BUCKET_PREFIX = "avatar"
MIGRATION_FILE_NAME = "utility/png_keep_file.txt"

# Set up the test data
DATA_FILES_LOCATION = ""
FILE_NAME = "/avatar*.png"
# Minimum number to have the avatar.png file
MIN_RANGE = 1000
# Maximum number to have the avatar.png file
MAX_RANGE = 2000

# PG DB Table Details
TABLE_NAME = "user_avatar"
COLUMN_NAME = "avatar_url"

# bucket-migration
Bucket-migration is a repository that copies the content of a bucket to another.

## Instalation
### Setup prerequisites
1. Requirements files are files containing a list of items to be installed using [pip](https://pip.pypa.io/en/stable/cli/pip_install/#pip-install) install like so: <br />
```bash 
pip3 install -r requirements.txt
```
2. Set up AWS credentials (in e.g. ~/.aws/credentials):<br />
```bash
aws configure set aws_access_key_id "$aws_access_id" --profile $profile
aws configure set aws_secret_access_key "$aws_secret" --profile $profile 
aws configure set region "$aws_region" --profile $profile
export AWS_PROFILE=$profile
```
3. Create .env file in source folder and add the PG DB Connection details
```text
PG_HOST=<postgres hostname>
PG_PORT=<postgres port>
PG_USER=<postgres database user>
PG_PASSWORD=<postgres database password>
PG_DATABASE=<database>
```

## Usage
Set up the buckets details and PG table details in source/constants.py file.
```text
# Setup source and destination bucket details
OLD_BUCKET = "legacy-s3-test"
OLD_BUCKET_PREFIX = "image"
NEW_BUCKET = "production-s3-test"
NEW_BUCKET_PREFIX = "avatar"

# PG DB Table Details
TABLE_NAME = "user_avatar"
COLUMN_NAME = "avatar_url"
```
### Command to execute the main script
```bash
cd <PATH>/bucker-migration/source
python3 main.py
```

### Command to execute the unit tests
```bash
cd <PATH>/bucker-migration/source
pytest test
```

## Usage of test_data_setup script

1. Create a folder where you want to create/store the .png files

2. Add path and png file details in `util/constans.py`
```text
# Set up the test data
DATA_FILES_LOCATION = "/home/ec2-user/avatar"
FILE_NAME = "/avatar*.png"
# Minimum number to have the avatar.png file in its name
MIN_RANGE = 1000 
# Maximum number to have the avatar.png file in its name
MAX_RANGE = 2000
```

3. Execute commands:
```bash
cd <PATH>/bucker-migration/source
python3 test_data_setup.py
```
import logging
import os
import glob

import boto3
from utility import util
from utility import constans

from botocore.exceptions import ClientError

# Setup logger
logging.basicConfig(level=logging.INFO,
                    format="[%(asctime)s] [%(levelname)s] (%(filename)s:%(lineno)d): %(message)s",
                    datefmt='%Y.%m.%d-%H:%M:%S')
logger = logging.getLogger(__name__)

# Setup S3 related client and resource details
session = boto3.session.Session(profile_name=os.environ.get('AWS_PROFILE'))
s3_client = boto3.client("s3")
s3_resource = boto3.resource("s3")


def get_object_tags_set(bucket_name, object_key):
    get_object_tags_response = s3_client.get_object_tagging(
        Bucket=bucket_name,
        Key=object_key,
    )
    tag_set_response = get_object_tags_response['TagSet']
    for item in tag_set_response:
        return bool("MigrationStatus" in item['Key'] and "Done" in item['Value'])


def update_object_tag_as_migrated(bucket_name, object_key):
    put_migration_tag_response = s3_client.put_object_tagging(
        Bucket=bucket_name,
        Key=object_key,
        Tagging={
            'TagSet': [
                {
                    'Key': 'MigrationStatus',
                    'Value': 'Done'
                }
            ]
        }
    )
    logger.info("Migration successful status was set for object:  %s", object_key)
    return put_migration_tag_response


def get_all_s3_keys(bucket, prefix, suffix):
    """Get a list of all keys in an S3 bucket."""
    keys = []

    kwargs = {'Bucket': bucket, 'Prefix': prefix}

    while True:
        resp = s3_client.list_objects_v2(**kwargs)
        for obj in resp['Contents']:
            key = obj['Key']
            if key.startswith(prefix) and key.endswith(suffix):
                keys.append(obj['Key'])

        try:
            kwargs['ContinuationToken'] = resp['NextContinuationToken']
            print("was here")
        except KeyError:
            break
    print(keys)
    return keys


def copy_object_from_a_bucket_to_another(old_bucket_name, old_bucket_prefix, new_bucket_name,
                                         new_bucket_prefix):
    # Setup source and destination bucket details
    legacy_bucket = s3_resource.Bucket(old_bucket_name)
    production_bucket = s3_resource.Bucket(new_bucket_name)

    logger.info("Starting copy from bucket " + legacy_bucket.name + " to bucket "
                + production_bucket.name)
    if util.is_file_empty(constans.MIGRATION_FILE_NAME):
        migration_png_list = get_all_s3_keys(legacy_bucket.name, old_bucket_prefix, ".png")
        util.write_to_file(file_name=constans.MIGRATION_FILE_NAME, list_for_file=migration_png_list)
    migration_png_list = util.read_from_file(file_name=constans.MIGRATION_FILE_NAME)
    while migration_png_list:
        for png_file in migration_png_list:
            logger.info("PNG file: %s", png_file)
            logger.info("List in for: %s", str(migration_png_list))
            is_migration_tag = get_object_tags_set("legacy-s3-test", png_file)
            if is_migration_tag:
                logger.info('%s object was already migrated.', png_file)
            else:
                production_key = new_bucket_prefix + png_file[len(old_bucket_prefix):]
                source_bucket = {"Bucket": legacy_bucket.name, "Key": png_file}
                try:
                    logger.info("Initiating copy of the object: %s", png_file)
                    s3_client.copy_object(CopySource=source_bucket, Bucket=production_bucket.name,
                                          Key=production_key,
                                          TaggingDirective='COPY')
                except ClientError:
                    logger.error("Object: %s was not copied to %s bucket."
                                 , png_file, production_bucket)
                logger.info("%s object was successfully migrated to %s ", png_file, production_key)
                update_object_tag_as_migrated(legacy_bucket.name, png_file)
            migration_png_list.remove(png_file)
            logger.info("%s was removed from migration list.", png_file)
            util.write_to_file(file_name=constans.MIGRATION_FILE_NAME,
                               list_for_file=migration_png_list)


def upload_files_to_s3(path, file_name):
    # The list of files we're uploading to S3
    filenames = glob.glob(path + file_name)
    try:
        for my_file in filenames:
            s3_file = f"{constans.OLD_BUCKET_PREFIX}/{os.path.basename(my_file)}"
            s3_client.upload_file(my_file, constans.OLD_BUCKET, s3_file)
    except Exception as error:
        logger.error("Error in upload operation: %s", error)
    finally:
        logger.info("All .png files were uploaded successfully.")

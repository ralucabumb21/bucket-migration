import logging
import boto3

from botocore.exceptions import ClientError

# Setup logger
logging.basicConfig(level=logging.INFO,
                    format="[%(asctime)s] [%(levelname)s] (%(filename)s:%(lineno)d): %(message)s",
                    datefmt='%Y.%m.%d-%H:%M:%S')
logger = logging.getLogger(__name__)

# Setup S3 related client and resource details
session = boto3.session.Session(profile_name="raluca")
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


def copy_object_from_a_bucket_to_another(old_bucket_name, old_bucket_prefix, new_bucket_name,
                                         new_bucket_prefix):
    # Setup source and destination bucket details
    legacy_bucket = s3_resource.Bucket(old_bucket_name)
    legacy_bucket_prefix = old_bucket_prefix
    production_bucket = s3_resource.Bucket(new_bucket_name)
    production_bucket_prefix = new_bucket_prefix

    logger.info("Starting copy from bucket " + legacy_bucket.name + " to bucket "
                + production_bucket.name)
    for obj in legacy_bucket.objects.all():
        if obj.key.endswith('.png'):
            legacy_key = obj.key
            is_migration_tag = get_object_tags_set(legacy_bucket.name, legacy_key)
            if is_migration_tag:
                logger.info('%s object was already migrated.', legacy_key)
            else:
                production_key = production_bucket_prefix + legacy_key[len(legacy_bucket_prefix):]
                source_bucket = {"Bucket": legacy_bucket.name, "Key": legacy_key}
                try:
                    logger.info("Initiating copy of the object: %s", legacy_key)
                    s3_client.copy_object(CopySource=source_bucket, Bucket=production_bucket.name,
                                          Key=production_key,
                                          TaggingDirective='COPY')
                except ClientError:
                    logger.error("Object: %s was not copied to %s bucket."
                                 , legacy_key, production_bucket)
                logger.info(legacy_key + ' object was successfully migrated to ' + production_key)
                update_object_tag_as_migrated(legacy_bucket.name, legacy_key)

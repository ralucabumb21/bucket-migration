from source.core import s3
from source import constans

if __name__ == '__main__':
    s3.copy_object_from_a_bucket_to_another(constans.OLD_BUCKET, constans.OLD_BUCKET_PREFIX,
                                            constans.NEW_BUCKET, constans.NEW_BUCKET_PREFIX)

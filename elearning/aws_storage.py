from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    bucket_name = 'emeka-web-files'
    location = 'media/elearning'


class StaticStorage(S3Boto3Storage):
    bucket_name = 'emaka-web-files'
    location = 'Staticfiles'

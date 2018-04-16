# -*- coding: utf-8 -*-

from minio import Minio
from minio.error import ResponseError
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)
import os

# note: Minio genere un etag (md5) pour chaque image. Et permet de prevenir tout type de doublon
# (images). Le problème c'est qu'il le calcul après avoir uploadé l'image, or on en a besoin avant
# afin de nommer l'image par son checksum.
def md5(file):
    import hashlib
    hash_md5 = hashlib.md5()
    hex_digest = hashlib.md5(file.read()).hexdigest()
    file.seek(0)

    return hex_digest

def size(file):
    size = len(file.read())
    # repointe le curseur à 0 car minioClient va relire le stream à nouveau et lui ne connait pas la taille
    # du fichier
    file.seek(0)
    return size

print "imported"
minioClient = Minio('localhost:9000',
                  access_key='SVUSVOZDI3K0MG9USHCF',
                  secret_key='J5DvPQhqmL+u8Wm513ZlUlfsdqTSB+6ZkCzdTurh',
                  secure=False)


print "minio client **"


def upload_file(file, bucketName=""):
    file_size   = size(file)
    hex_name    = md5(file)

    try:
        ext        = os.path.splitext(file.filename)[1]
        full_name  = hex_name + ext

        tag = minioClient.put_object(bucketName, full_name, file,
            length          = file_size,
            content_type    = file.content_type)

        return full_name

    except ResponseError as err:
        raise

def setup():
        # Make a bucket with the make_bucket API call.
    try:
        minioClient.make_bucket("badges")
        print "make bucker"
    except BucketAlreadyOwnedByYou as err:
        print "BucketAlreadyOwnedByYou"
        pass
    except BucketAlreadyExists as err:
        print "BucketAlreadyExists"
        pass
    except ResponseError as err:
        raise

    try:
        print "try upload"
        file_stat = os.stat('static/img/logo.png')
        file_data = open('static/img/logo.png', 'rb')
        print "file_data", file_data
        print(minioClient.put_object('badges', 'myobject', file_data, file_stat.st_size))
        print "done"
    except ResponseError as err:
        print(err)

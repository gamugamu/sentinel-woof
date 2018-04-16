# -*- coding: utf-8 -*-
from flask import request
from minio import Minio
from minio.error import ResponseError
from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)
import os
from utils.error import *

BASE_URL    = "http://localhost:9000/"
minioClient = None
minioACCESS = "AKIAIOSFODNN7EXAMPLE"
minioSECRET = "SECRETSECRET"

MAX_BADGE_SIZE = 50000 # la taille de l'image max pour le badge. 50k max

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

def url_fromFileName(fileName, bucketName):
    return BASE_URL + bucketName + '/' + fileName

def upload_file(file, bucketName=""):
    from PIL import Image
    from io import BytesIO

    #TODO, type plutôt que bucketName
    #SWITCH
    img     = Image.open(file)
    byte_io = BytesIO()
    #TODO externalise size
    img.thumbnail((120, 120), Image.ANTIALIAS)
    img.save(byte_io, "JPEG")
    # rembobinage
    byte_io.seek(0)

    file_size = size(byte_io)
    hex_name  = md5(byte_io)

    try:
        ext        = os.path.splitext(file.filename)[1]
        full_name  = hex_name + ext

        tag = minioClient.put_object(bucketName, full_name, byte_io,
            length          = file_size,
            content_type    = file.content_type)

        return url_fromFileName(full_name, bucketName)

    except ResponseError as err:
        #TODO error
        raise

def bucket_setup(base_url):
    global BASE_URL, minioClient
    BASE_URL = base_url

    minioClient = Minio('localhost:9000',
                      access_key=minioACCESS,
                      secret_key=minioSECRET,
                      secure=False)

    # Make a bucket with the make_bucket API call.
    setup_bucket("badges")
    setup_bucket("feeds")


def setup_bucket(bucketName):
        # Make a bucket with the make_bucket API call.
    try:
        minioClient.make_bucket(bucketName)
        minioClient.set_bucket_policy(bucketName,
                              '*',
                              Policy.READ_WRITE)
    except BucketAlreadyOwnedByYou as err:
        pass
    except BucketAlreadyExists as err:
        pass

    except ResponseError as err:
        raise

# -*- coding: utf-8 -*-
import os
import redis
from captcha.image import ImageCaptcha

current_file_dir = os.path.dirname(os.path.abspath(__file__))
font_path        = os.path.join(current_file_dir, "../static/fonts/Traffolight.otf")

TIME_OUT_CAPTCHA = 60 * 60
image   = ImageCaptcha(fonts=[font_path])
r       = None

def setup(conf):
    print "conf ", conf
    global r
    if conf is None:
        r = redis.StrictRedis(host='localhost', port=6379, db=1)
    else:
        #TODO refactor avec app
        r = redis.StrictRedis(host='redisdb', port=6379, db=1)



def generate_captcha():
    import uuid
    import base64
    import petname

    #TODO refactor avec feed pour le safe uuid
    r_uuid = base64.urlsafe_b64encode(uuid.uuid4().bytes)
    verify = petname.Generate(1)

    r.setex(r_uuid, TIME_OUT_CAPTCHA, verify)
    return image.generate(verify), r_uuid

def is_captcha_valid(uuid, value):
    if r.get(uuid) == value:
        # on supprime le cache pour empecher quelqu'un d'utiliser le même
        # captcha
        r.delete(uuid)
        return True
    else:
        return False

#! /usr/bin/python

#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#

import os
import zipfile

import boto
from datetime import date
from boto.s3.key import Key
from PIL import Image, ImageOps
from django.conf import settings
from os.path import join, exists
from shinobi_api.services import Utils
import base64

__author__ = "tu"
__date__ = "$Mars 21, 2017 11:04:25 AM$"


# def crop_image(file_path, file_name, **kwargs):
#     """
#     Crop image to LOGO_CROP_SIZE and save as JPEG format
#     :param file_path:
#     :param file_name:
#     :return:
#     """
#     full_path = join(file_path, file_name)
#     extension = file_name[file_name.rfind('.'):]
#     new_file_name = file_name.replace(extension, '.resized.jpeg')
#     new_full_path = join(file_path, new_file_name)
#     im = Image.open(full_path)
#     im = ImageOps.fit(im, kwargs.get('crop_size'), Image.ANTIALIAS)
#     im.save(new_full_path, 'JPEG')
#     os.remove(full_path)
#     return new_file_name
#
#
# def upload(file_path, upload_dir, file_name, type):
#     extension = file_name[file_name.rfind('.'):]
#     new_file_name = file_name.replace(extension, '.'+type+'.jpeg')
#     full_path = join(file_path, file_name)
#     new_full_path = join(file_path, new_file_name)
#     img = Image.open(full_path)
#     if img.mode != "RGB":
#         img = img.convert("RGB")
#     img.save(new_full_path, "JPEG", quality=80, optimize=True, progressive=True)
#     # if settings.DEBUG == False:
#     #     sync_to_AWS3(new_full_path, upload_dir, new_file_name)
#
#
# def handle_upload(file_items, user_id, base_path='logo/%s', **kwargs):
#     full_screen = kwargs.pop('full_screen', False)
#     crop = kwargs.pop('crop', False)
#     unzip = kwargs.pop('unzip', False)
#     saved = dict()
#     upload_dir = date.today().strftime(base_path)
#     upload_full_path = join(settings.MEDIA_ROOT, upload_dir)
#
#     if not exists(upload_full_path):
#         os.makedirs(upload_full_path)
#
#     for key, file in file_items:
#         file_name = '{0}{1}_{2}'.format(Utils.id_generator(10), user_id, file.name)
#         dest = open(os.path.join(upload_full_path, file_name), 'wb')
#         for chunk in file.chunks():
#             dest.write(chunk)
#         dest.close()
#
#         if full_screen:
#             upload(upload_full_path, upload_dir, file_name, 'full_screen')
#         else:
#             upload(upload_full_path, upload_dir, file_name, 'test_screen')
#         if crop:
#             file_name = crop_image(upload_full_path, file_name, **kwargs)
#         file_dir = join(upload_dir, file_name)
#         local_file_path = join(upload_full_path, file_name)
#         if unzip:
#             extension = file_name[file_name.rfind('.'):]
#             if extension == '.zip':
#                 zip_ref = zipfile.ZipFile(local_file_path, 'r')
#                 zip_ref.extractall(join(upload_full_path, file_name[:-4]))
#                 zip_ref.close()
#                 os.remove(local_file_path)
#                 saved.update({'upload_dir': join(upload_dir, file_name[:-4])})
#         saved.update({key: file_dir})
#         # Sync uploaded file to S3
#
#         #if settings.DEBUG == False:
#         #    sync_to_AWS3(local_file_path, upload_dir, file_name)
#     return saved

def convertBase64toImg(encode_string, user_id, base_path='image/%s', **kwargs):
    full_screen = kwargs.pop('full_screen', False)
    saved = dict()
    upload_dir = date.today().strftime(base_path)
    upload_full_path = join(settings.MEDIA_ROOT, upload_dir)

    if not exists(upload_full_path):
        os.makedirs(upload_full_path)

    if full_screen:
        file_name = '{0}{1}_{2}'.format(Utils.id_generator(10), user_id, "fullscreen.png")
        key = "full_screen"
    else:
        file_name = '{0}{1}_{2}'.format(Utils.id_generator(10), user_id, "testscreen.png")
        key = "test_screen"

    file_dir = join(upload_dir, file_name)
    imgdata = base64.b64decode(encode_string)
    with open(os.path.join(upload_full_path, file_name), 'wb') as f:
        f.write(imgdata)

    saved.update({key:file_dir})
    return saved


# def sync_to_AWS3(local_file_path, sync_path, file_name):
#     try:
#         upload_to = join(settings.MEDIAFILES_LOCATION, sync_path)
#         bucket_name = settings.AWS_STATIC_BN
#         s3_conn = boto.connect_s3(settings.AWS_ID, settings.AWS_SECRET)
#         bucket = s3_conn.get_bucket(bucket_name)
#         bucket_key = Key(bucket)
#         bucket_key.key = join(upload_to, file_name)
#         bucket_key.set_contents_from_filename(local_file_path)
#         bucket_key.make_public()
#         return True
#     except Exception as e:
#         return False

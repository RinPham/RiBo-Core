#! /usr/bin/python
#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
from shinobi_api.services.base import BaseService
from django.conf import settings
import subprocess
import urllib.request
import re
from shinobi_api.services.utils import Utils
import os
from os.path import join
import boto
from boto.s3.key import Key
from shinobi_api.const import MMSType
from PIL import Image

__author__ = "hien"
__date__ = "$Jul 05, 2016 10:16:08 AM$"

class MediaError(TypeError): pass  # base exception class

class MediaService(BaseService):


    @classmethod
    def get_length(cls, file_url):
        result = subprocess.Popen(["ffprobe", file_url], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return [x for x in result.stdout.readlines() if "Duration" in x]

    
    @classmethod
    def s3_download(cls, media_id, file_url):
        result = {
            "file_url": file_url,
            "file_name": False,
            "file_path": False,
            "success": 0,
            "error": ""
        }
        try:
            req = urllib.request.Request(file_url, headers={'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"})
            u = urllib.request.urlopen(req)
            meta = u.info()
            mime_type = "image/png"
            file_name = "_tmp_{0}.png".format(media_id)
            base_path = settings.MEDIA_ROOT
            out_path = "{0}/{1}".format(base_path, file_name)
            result["mime_type"] = mime_type
            result["file_name"] = file_name
            result["file_path"] = out_path
            try:
                os.remove(out_path)
            except:
                pass
            f = open(out_path, 'wb')
            file_size_dl = 0
            block_sz = 8192
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break
                file_size_dl += len(buffer)
                f.write(buffer)
            f.close()
            result["file_size"] = file_size_dl
            result["success"] = 1
        except Exception as e:
            cls.log_exception(e)
            result['error'] = str(e)
        return result
    
    @classmethod
    def download(cls, media_id, file_url):
        result = {
            "file_size": 0,
            "file_size_dl": 0,
            "file_name": False,
            "out_path": False,
            "success": 0,
            "error": ""
        }
        try:
            req = urllib.request.Request(file_url, headers={'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"})
            u = urllib.request.urlopen(req)
            meta = u.info()
            mime_type = meta.getheaders("Content-Type")[0]
            file_size = int(meta.getheaders("Content-Length")[0])
            disposition = False
            file_name = False
            if meta.getheaders("Content-Disposition"):
                disposition = meta.getheaders("Content-Disposition")[0]
                file_name = re.findall("filename=(\S+)", disposition)[0]
                file_name = Utils.normalize_str(file_name)
                file_name = re.sub(r'^"|"$', '', file_name)
                file_name = file_name.replace("_", "-")
            if not file_name:
                extends = {
                    "video/3gpp": ".3gp",
                    "video/mp4": ".mp4",
                    'image/jpeg': ".jpg",
                    'image/png': ".png"
                }
                file_name = "media-{0}{1}".format(media_id, extends[mime_type])
            else:
                file_name = "media-{0}-{1}".format(media_id, file_name)
            base_path = settings.MEDIA_ROOT
            out_path = "{0}{1}".format(base_path, file_name)
            result["file_size"] = file_size
            result["mime_type"] = mime_type
            result["file_name"] = file_name
            result["out_path"] = out_path
            try:
                os.remove(out_path)
            except:
                pass
            f = open(out_path, 'wb')
            file_size_dl = 0
            block_sz = 8192
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break

                file_size_dl += len(buffer)
                f.write(buffer)
            f.close()
            success = (file_size_dl == file_size)
            result["file_size_dl"] = file_size_dl
            result["success"] = success
        except Exception as e:
            cls.log_exception(e)
            result['error'] = str(e)
        return result
    
    @classmethod
    def clean_s3(cls, uris):
        try:
            bucket_name = settings.AWS_STATIC_BN
            s3Conn = boto.connect_s3(settings.AWS_ID, settings.AWS_SECRET)
            bucket = s3Conn.get_bucket(bucket_name)
            s3keys = []
            for uri in uris:
                uri = uri.split('?')[0]
                uri = uri.split(settings.MEDIA_URL)[-1]
                s3keys.append(join(settings.MEDIAFILES_LOCATION, uri))
            bucket.delete_keys(s3keys)
        except Exception as e:
            cls.log_exception(e)

    @classmethod
    def resize(cls, file_path):
        filename = os.path.basename(file_path)
        result = {
            "file_name": filename,
            "thumb": "",
            "thumb_path": "",
            "error": "",
            "logs": "",
            "command": "",
            "size": (0, 0)
        }
        try:
            base_path = settings.MEDIA_ROOT
            name, ext = os.path.splitext(filename)
            thumb_name = "thumb-{}{}".format(name, ext)
            thumb_path = join(base_path, thumb_name)
            result["thumb"] = thumb_name
            result["thumb_path"] = thumb_path
            #if(gt(a,4/3),320:-1)':'if(gt(a,4/3),-1:240)
            os_command = "ffmpeg -i {0} -vf scale=\"'320:-1'\" {1}".format(file_path, thumb_path)
            result["command"] = os_command
            p_result = subprocess.Popen([os_command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            lines = p_result.stdout.readlines()
            result["logs"] = lines
            if lines and 'not found' in lines[0].decode(encoding='UTF-8'):
                raise Exception("ffmpeg has not been installed")
            thumb_info = Image.open(thumb_path)
            result['size'] = thumb_info.size
        except Exception as e:
            cls.log_exception(e)
            result['error'] = str(e)
        return result

    @classmethod
    def create_thumb(cls, file_path):
        filename = os.path.basename(file_path)
        result = {
            "file_name": filename,
            "thumb": "",
            "thumb_path": "",
            "error": "",
            "logs": "",
            "command": ""
        }
        try:
            base_path = settings.MEDIA_ROOT
            thumb_name = "thumb-{0}.png".format(os.path.splitext(filename)[0])
            thumb_path = "{0}{1}".format(base_path, thumb_name)
            result["thumb"] = thumb_name
            result["thumb_path"] = thumb_path
            os_command = "ffmpeg -itsoffset -1 -i {0} -vframes 1 -filter:v scale='min(320\, iw):-1' {1}".format(file_path, thumb_path)
            result["command"] = os_command
            p_result = subprocess.Popen([os_command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            lines = p_result.stdout.readlines()
            result["logs"] = lines
        except Exception as e:
            cls.log_exception(e)
            result['error'] = str(e)
        return result

    @classmethod
    def convert_to_mp4(cls, in_path="", mime_type="video/3gpp"):
        filename = os.path.basename(in_path)
        result = {
            "file_name": filename,
            "in_path": in_path,
            "out_path": "",
            "error": "",
            "logs": "",
            "command": ""
        }
        mime_types = {
            "video/3gpp": "ffmpeg -i {0} -c:v libx264 -crf:v 22 -preset:v veryfast -ac 2 -c:a libfdk_aac -vbr 3 {1}",
        }
        try:
            if mime_type in mime_types:
                base_path = settings.MEDIA_ROOT
                out_name = "{0}.mp4".format(os.path.splitext(filename)[0])
                out_path = "{0}{1}".format(base_path, out_name)
                result["out_path"] = out_path
                try:
                    #Clean converted file
                    os.remove(out_path)
                    pass
                except:
                    pass
                os_command = mime_types[mime_type].format(in_path, out_path)
                result["command"] = os_command
                p_result = subprocess.Popen([os_command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                lines = p_result.stdout.readlines()
                result["logs"] = lines
                result["file_name"] = out_name
                try:
                    #Clean origin file
                    os.remove(in_path)
                    pass
                except:
                    pass
            else:
                result["out_path"] = in_path
                result["logs"] = "No convert, keep origin"
        except Exception as e:
            cls.log_exception(e)
            result['error'] = str(e)
        return result

    @classmethod
    def media_type(cls, mimetype):
        image_mime_types = [
            'image/jpeg',
            'image/png'
        ]
        if mimetype in image_mime_types:
            return MMSType.IMAGE
        return MMSType.VIDEO
